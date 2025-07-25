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
from logging import getLogger

import datarobot as dr
import pandas as pd
from datarobot_predict.deployment import predict

logger = getLogger(__name__)


def make_datarobot_text_gen_predictions(input_message: str, deployment_id: str) -> dict[str, str]:
    """Takes in a string and requests a prediction from the specified DataRobot text generation model (LLM).

    This tool should ONLY be used for TextGeneration deployments and not for regression, classification or other.

    Parameters
    ----------
    input_message : string of text or messages to send to the deployment

    deployment_id: str
        the datarobot deployment to request predictions from.

    Returns
    -------
    str
        the prediction.

    Source
    ______
    datarobot
    """
    deployment = dr.models.Deployment.get(deployment_id=deployment_id)
    c = dr.client.Client()
    resp = c.get(f"modelPackages/{deployment.model_package['id']}").json()
    target_column = deployment.model.get("target_name", "")
    if prompt := resp["textGeneration"].get("prompt", False):
        prompt_column = prompt
    else:
        prompt_column = "promptText"

    df, _ = predict(deployment, pd.DataFrame([{prompt_column: input_message}]))
    result = {
        "LLM_Generated_Response": df.iloc[0][f"{target_column}_PREDICTION"],
    }

    if "CITATION_SIMILARITY_SCORE_0_OUTPUT" in df.columns:
        context = []
        for i in range(0, 10):
            try:
                similarity = df.iloc[0][f"CITATION_SIMILARITY_SCORE_{i}_OUTPUT"]
                if similarity < 100:
                    context.append(
                        {
                            "citation_source": df.iloc[0][f"CITATION_SOURCE_{i}_OUTPUT"],
                            "citation_output": df.iloc[0][f"CITATION_CONTENT_{i}_OUTPUT"],
                        }
                    )
            except Exception as e:
                logger.error(e)

        result["Citation_Context"] = context

    return result
