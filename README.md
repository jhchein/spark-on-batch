# spark_on_azure_batch_demo
This is a demo that shows how to run Spark jobs on Azure Batch.

**This code is NOT PRODUCTION READY!**

The original code is from https://medium.com/datamindedbe/run-spark-jobs-on-azure-batch-using-azure-container-registry-and-blob-storage-10a60bd78f90 and respectively https://github.com/datamindedbe/spark_on_azure_batch_demo -> All credits go to him :)

## Set-Up
Clone this repo.

### Azure Portal
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjhchein%2Fspark-on-batch-example%2Fadd-arm-template%2Fazuredeploy.json)

In your Azure Portal
* Create an azure batch account
* Create a container registry
* Create a storage account
* Create a container called 'titanic' in your blob storage. Upload data/train.csv to that container.


### Environment
* Create a python environment and install the requirements from requirements.txt ```pip install -r requirements.txt```
* Install jupyter in your environment (```conda install -y jupyter``` or ```pip install jupyter```)

### Editor / IDE
* Copy template.config.py to config.py and add your credetials and resource names
* Adjust the code in titanic_analytics.py (this is the code run in a node)
  * Update file and output to match your storage account (e.g. "wasbs://containername@YOURSTORAGEACCOUNTNAME.blob.core.windows.net/train.csv")
  * Adjust the spark query and logging however it suits you. 

### Build Docker Image
* Build your docker image and push to your registry (replace ```sparkonbatch``` with your ACR name)
  * ```docker build -t sparkonbatch/titanic_spark_on_batch_demo .```
  * ```docker tag sparkonbatch/titanic_spark_on_batch_demo:latest```
  * ```docker push sparkonbatch.azurecr.io/sparkonbatch/titanic_spark_on_batch_demo:latest```
* Add the image name (in this case: ```sparkonbatch.azurecr.io/sparkonbatch/titanic_spark_on_batch_demo```)

### Jupyter
* Run 'titanic-demo.ipynb' in jupyter notebook.
* (optional) Check the logs ('stderr.txt') of a Task in Azure Portal

### Scaling and teardown
When you're done, just scale the pool to zero (or delete). You can scale the pool via the Azure Portal manually or defining a function (autoscale). 

You can delete jobs and pools via the jupyter notebook (last two lines) or the Azure Portal.

You don't need to delete the Azure Resources in case you might need them later on.
