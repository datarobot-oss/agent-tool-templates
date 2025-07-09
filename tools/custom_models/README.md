# Custom Model Tools

## Overview

Custom Model Tools are integrations available through this repository. The different from the global models is that these tools allow for extra configuration via custom model Runtime Parameters. 

## Repository Structure

Each subdirectory contains a standalone custom model implementation for a tool. The source code is provided (in the custom_model subdirectory) and can be modified or extended to create custom models tailored to specific use cases.

List of available Tools:

| **Tool Name**                                                  | **Description**                                                                                                                                                                                                                                                                               |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [upload_file_to_data_registry](./upload_file_to_data_registry) | Uploads a file to the Data Registry. The file can be either a Pandas DataFrame or a file path on the storage backend configured via Runtime Parameters. |
