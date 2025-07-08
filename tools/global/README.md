# Global Tools

## Overview

Global Tools are pre-built integrations available through the [Model Registry](https://docs.datarobot.com/en/docs/mlops/deployment/registry/reg-create.html). They can be deployed and used within agents without additional configuration.

## Model type
Global tools are unstructured custom models in DataRobot. You can read more [here](https://docs.datarobot.com/en/docs/mlops/deployment/custom-models/custom-model-assembly/unstructured-custom-models.html#assemble-unstructured-custom-models) about structure of these models.

## Repository Structure

Each subdirectory contains a standalone custom model implementation for a global tool. The source code is provided (in the custom_model subdirectory) for transparency and can be modified or extended to create custom models tailored to specific use cases.

List of Global Tools:

| **Tool Name**                                                  | **Description**                                                                                                   |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| [get_ai_catalog_dataset](./get_ai_catalog_dataset)             | Retrieves datasets from the DataRobot AI Catalog using a `dataset_id`. Returns the dataset in CSV format as raw bytes. |
| [make_ml_predictions](./make_ml_predictions)                   | Performs machine learning predictions using a specified model. Accepts input data and returns prediction results. |
| [make_textgen_predictions](./make_textgen_predictions)         | Generates text predictions based on input data using a text generation model. Suitable for tasks like summarization or text completion. |
| [make_time_series_predictions](./make_time_series_predictions) | Produces time series predictions using a specified model. Useful for forecasting and trend analysis.              |
| [render_chart_plotly](./render_chart_plotly)                   | Creates interactive charts using Plotly based on input data and configuration. Returns a rendered chart object.   |
| [render_chart_vegalight](./render_chart_vegalight)             | Generates a chart from a Vega-Lite specification and returns a JSON with a base64-encoded image of the chart.     |
| [search_ai_catalog](./search_ai_catalog)                       | Searches for datasets in the DataRobot AI Catalog using search terms. Returns matching datasets as a DataFrame.   |
| [summarize_dataframe](./summarize_dataframe)                   | Provides a detailed summary of a pandas DataFrame in Markdown format, including statistics and data insights.     |

## Using tools
To make use of the tool, you need to deploy it in DataRobot instance and then invoke it using the prediction API.

## Making predictions
Below are instructions on how to make predictions after the tool has been deployed in DataRobot.

- **Using python prediction code snippet**
    
    After deployment, invoke the tool by making unstructured prediction requests to DataRobot. 
    Use the [prediction API code snippet](https://docs.datarobot.com/en/docs/predictions/realtime/code-py.html) with the specified request format. An auto-generated code snippet is also available in the `Predictions` tab of the model deployment in the DataRobot UI. 
    For further details, refer to the [documentation on unstructured model predictions](https://docs.datarobot.com/en/docs/api/reference/predapi/pred-ref/dep-pred-unstructured.html). 


- **Using `curl`**

    First prepare variables related to our deployment and datarobot instance:

    ```bash
    export API_KEY='<your-datarobot-api-key>'
    export DR_KEY='<datarobot-key>' 
    export DEPLOYMENT_ID='<tool-deployment-id>'
    ```
  
    For more information about deployment prediction headers, see [the documentation](https://docs.datarobot.com/en/docs/api/reference/predapi/pred-ref/dep-pred.html#headers).  
    Once your variables are set, you can make a prediction request using the following `curl` command. The `request.json` file should contain the input data specific to the tool you are using. 
    For details on the required input structure, refer to the tool's README file.
    
    ```bash
    curl -i -X POST "https://example.datarobot.com/predApi/v1.0/deployments/${DEPLOYMENT_ID}/predictionsUnstructured" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "DataRobot-Key: ${DR_KEY}" \
        --data @/path/to/request.json
    ```

    