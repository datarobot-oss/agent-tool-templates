# Copyright 2025 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
from formatter import PredictionFormatter
from logging import getLogger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import datarobot as dr
import pandas as pd
from data_types import extract_and_sanitize_json
from datarobot_predict.deployment import predict
from validate_and_fix import fix_columns_cases

from models import get_utility_client

logger = getLogger(__name__)


def make_datarobot_ml_predictions(
    deployment_id: str,
    columns_to_return_with_predictions: List[str],
    input_data_json_str: str = None,
    input_dataframe: pd.DataFrame = None,
) -> str:
    """Takes in either a Pandas Dataframe (via dataset cache_id) OR a JSON formatted Array and uses that to request a prediction from the specified DataRobot model.
    Prior to using this tool, verify that you have all the data needed by calling the `help` tool.

    Note the argument `columns_to_return_with_predictions` this will tell the tool to return columns from the input dataset if you want. Use this to make sure you can interpret the predictions. For example, you may want to return ID or other identifying columns so you can see which prediction is which. You can't just rely on the index or order of the predictions.

    Parameters
    ----------
    deployment_id: str
        the datarobot deployment to request predictions from.

    columns_to_return_with_predictions: List[str]
        a list of columns from the input data that will merged back onto the ouput data for reference. (Required)

    input_data_json_str: JSON String
        you may pass a JSON formatted array and will return predictions based on those to rows.

    input_dataframe: pd.DataFrame
        a pandas dataframe

    Returns
    -------
    str
        the predictions formatted as a pandas dataframe in a csv format.

    Source
    ______
    datarobot
    """
    if input_data_json_str is None and input_dataframe is None:
        raise ValueError(
            "You need to populate either input_data_json_str or input_dataframe to use this tool. "
        )
    if input_data_json_str:
        if isinstance(input_data_json_str, str):
            input_data = pd.read_json(input_data_json_str)
        else:
            input_data = pd.DataFrame.from_records(input_data_json_str)
    else:
        input_data = input_dataframe

    deployment = dr.models.Deployment.get(deployment_id=deployment_id)
    input_data_adjusted = get_adjusted_input_data(deployment, input_data, is_timeseries=False)
    expls_no = min(10, len(input_data_adjusted.columns))
    df, _ = predict(deployment, input_data_adjusted, max_explanations=expls_no)
    return format_predictions(
        df,
        input_data,
        input_data_adjusted,
        deployment,
        columns_to_return_with_predictions,
    )


def get_adjusted_input_data(
    deployment: dr.models.Deployment, input_data: pd.DataFrame, is_timeseries: bool
):
    features = [f["name"] for f in deployment.get_features()]
    if is_timeseries:
        features.append(deployment.model["target_name"].replace(" (actual)", ""))

    # Create case-insensitive mapping of input columns to model features
    input_cols_lower = {col.lower(): col for col in input_data.columns}

    # Create a copy of input data for column renaming
    input_data_adjusted = input_data.copy()

    # Track which features are actually missing (not just case mismatched)
    missing_features = []

    # Attempt to match and rename columns
    for feature in features:
        feature_lower = feature.lower()
        if feature_lower in input_cols_lower:
            # If there's a case mismatch, rename the column
            if input_cols_lower[feature_lower] != feature:
                input_data_adjusted.rename(
                    columns={input_cols_lower[feature_lower]: feature}, inplace=True
                )
        else:
            missing_features.append(feature)

    if len(missing_features) > 0:
        raise ValueError(
            f"""You missing the required input columns: {" , ".join(missing_features)} please supply values to these to make predictions"""
        )

    return input_data_adjusted


async def summarize_expls(in_df: pd.DataFrame, expl_features, deployment_desc: str):
    client = get_utility_client()
    if not client:
        return []
    if len(in_df) > 200:
        raise ValueError("too many rows")
    template = f"""
    The following markdown table includes a column, `prediction` generated from a
    machine learning model. all columns after prediction represent up to ten input features
    of the machine learning model. For each of these input features, the value in that cell represents
    the contribution of that feature to the prediction on a scale of -3, 3 where 0 is no contribution at all and 3 is the maximum
    poistive impact while -3 is the maximum negative impact.
    For each row in the table, create a concise 1-2 sentence summary of the contributing features to the prediction. Use you're intution
    about what each column means and create an understanding for a the lay person.
    Here is an example for a model predicting home prices
    |Home_ID|prediction|No_of_Bedrooms|No_of_Bathrooms|
    |    A  | 1,000,000|       3      |       3      |
    |    B  |250,000    | -3          |    0        |
    for this input you return a JSON array of that sumamrizes the contribtions. be careful not to refer directly to the value in the fields as it is only a way of presenting the scale.
    For the example above return:
    ```
    [
    "The size of this home determined by the bedrooms and bathrooms has lead to an increase in price",
    "such a small home. its a deal"
    ]
    ```
    reply only with a JSON array.
    Apply this logic to the following model:
    Model Desc: {deployment_desc}
    Data:
    {in_df.to_markdown(index=False)}
 """
    result = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": template}],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "sumamries",
                "schema": {
                    "type": "object",
                    "properties": {
                        "summaries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "An array of summary strings",
                        }
                    },
                    "required": ["summaries"],
                    "additionalProperties": False,
                },
            },
        },
    )
    content = result.choices[0].message.content
    content = extract_and_sanitize_json(content)
    return content["summaries"]


def return_formatted(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)


def format_predictions(
    df: pd.DataFrame,
    input_data: pd.DataFrame,
    input_data_adjusted: pd.DataFrame,
    deployment: dr.models.Deployment,
    columns_to_return_with_predictions: List[str] = None,
    pred_expl_limit: int = 50,
    model_info: Optional[Dict[str, Any]] = None,
) -> str:
    try:
        pf = PredictionFormatter(df, deployment, model_info=model_info)
        formatted_df = pf.format()
    except Exception as e:
        logger.error(e)
        return return_formatted(df)

    try:
        formatted_df = formatted_df.loc[formatted_df.prediction.notna()]
    except Exception as e:
        logger.error(e)

    if pred_expl_limit and len(formatted_df) <= pred_expl_limit:
        try:
            summaries = asyncio.run(summarize_expls(formatted_df, [], deployment.label))
            formatted_df["Explanations Summary"] = summaries
            # formatted_df.drop(columns=["EXPLANATION_1_FEATURE_NAME"], inplace=True)
        except Exception as e:
            logger.error(f"Error summarizing prediction explanations: {e}")

    try:
        if date_col := model_info.timeseries.get("datetime_column_name"):
            date_col = date_col.replace(" (actual)", "")
            date_cols = fix_columns_cases(date_col, list(input_data_adjusted.columns))
            date_col = date_cols[0]
            input_data_adjusted[date_col] = pd.to_datetime(input_data_adjusted[date_col])

        if series_col := model_info.timeseries.get("series_column_name"):
            series_col = fix_columns_cases(series_col, list(input_data_adjusted.columns))[0]
            input_data_adjusted[series_col] = input_data_adjusted[series_col].astype(str)

        if date_col and series_col:
            formatted_df.index = pd.MultiIndex.from_tuples(
                zip(formatted_df["timestamp"].dt.date, formatted_df["seriesId"]),
                names=["timestamp", "seriesId"],
            )
            input_data_adjusted.index = pd.MultiIndex.from_tuples(
                zip(
                    input_data_adjusted[date_col].dt.date,
                    input_data_adjusted[series_col],
                ),
                names=["timestamp", "seriesId"],
            )
        elif date_col:
            input_data_adjusted.index = pd.DatetimeIndex(input_data_adjusted[date_col].dt.date)
            date_col = fix_columns_cases(date_col, list(formatted_df.columns))[0]
            formatted_df.index = pd.DatetimeIndex(pd.to_datetime(formatted_df[date_col]).dt.date)

    except Exception as e:
        logger.error(e)

    for col in formatted_df.columns:
        if col in input_data_adjusted.columns:
            formatted_df.drop(columns=[col], inplace=True)

    columns_to_return_with_predictions = fix_columns_cases(
        columns_to_return_with_predictions, input_data_adjusted.columns
    )
    if columns_to_return_with_predictions:
        # Use the original column names for returning additional columns
        try:
            return_frame = formatted_df.join(
                input_data_adjusted[columns_to_return_with_predictions], how="left"
            )
        except Exception as e:
            logger.error(e)
            return_frame = formatted_df
        # return_frame = pd.concat(
        #     (formatted_df, input_data_adjusted[columns_to_return_with_predictions]),
        #     axis=1,
        # )
    else:
        return_frame = formatted_df

    return_frame = return_frame.applymap(lambda x: round(x, 2) if isinstance(x, float) else x)
    try:
        return_frame = return_frame.loc[return_frame.prediction.notna()]
    except Exception as e:
        logger.error(e)
    return return_formatted(return_frame)
