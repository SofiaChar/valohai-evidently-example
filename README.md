# Valohai Evidently Example Project

Welcome to the Valohai Evidently Example Project! This project demonstrates how to use the Evidently library with Valohai to monitor and report on data drift. Follow the instructions below to configure and run the project.

## Project Overview
This project is based on the Evidently blog tutorial and the example notebook from Evidently. It includes two versions of the example:

- bicycle_demand_monitoring.py: A Python script for monitoring bicycle demand. This script monitors bicycle demand and generates an HTML report. The report is saved to a path that Valohai can pick up. Here are the changes made to save the report:

```python
import os

save_path = os.getenv('VH_OUTPUTS_DIR') + '/' + file_name
report.save(save_path)
```

- bicycle_demand_monitoring.ipynb: A Jupyter notebook version of the same example. This Jupyter notebook version of the example introduces `live uploads`, allowing you to upload files to Valohai during the execution. Here's how to save and upload the report:

```python

import os
import valohai

save_path = os.getenv('VH_OUTPUTS_DIR') + '/' + 'data_drift_dashboard_after_week1.html'
data_drift.save(save_path)
# Request for an immediate upload
valohai.outputs().live_upload("data_drift_dashboard_after_week1.html")
```

!!! note
    Live uploads are also available for normal executions

Before running the project, you need to have Valohai CLI and utilities installed on your machine. Follow these steps to get started:

### Install Valohai CLI and Utilities

```bash 
pip install valohai-cli valohai-utils
```

### Log in to Valohai
Log in to your Valohai account from the terminal:

```bash 
vh login
```

### Create a Project Directory
Create a directory for your Valohai project:

```bash 
mkdir valohai-evidently-example
cd valohai-evidently-example
```

### Create Valohai Project
Initialize a new Valohai project:

```bash 
vh project create
```

### Clone the Repository
Clone the Evidently example repository to your local machine:

```bash 
git clone https://github.com/valohai/evidently-example.git .
```

### Running bicycle_demand_monitoring.py
To run the script, use the following command:

```bash 
vh execution run run_example --adhoc
```

### Running bicycle_demand_monitoring.ipynb
To run the notebook, follow these steps:

1. Go to your project in the Valohai UI. 
2. Navigate to Project Settings -> Repository. 
3. Add the repository URL: https://github.com/valohai/evidently-example.git. 
4. Press Save Changes. 
5. Go to the Notebooks tab. 
6. Click Create Notebook Execution. 
7. Choose the environment and Docker image. 
8. Press Create Notebook Execution.

After a few minutes, you will see the Open Notebook tab in the execution.


## Conclusion
You are now ready to use Evidently with Valohai! Modify the examples as needed and run your data monitoring tasks seamlessly. If you encounter any issues, refer to the Valohai documentation or reach out to us at `support@valohai.com`. Happy coding!