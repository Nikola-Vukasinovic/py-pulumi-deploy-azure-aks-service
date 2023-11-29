# py-pulumi-deploy-azure-aks-service

Deploy Azure AKS service using Python and Pulumi

First we need to setup Pulumi, at the time of the writing current version is v3.94.2.

## Heads up

I do recommend using venv with each project so project dependecies can be kept tight. For more information visit [venv](https://docs.python.org/3/tutorial/venv.html).

Following example uses virtual enviroment with Python version 3.8.10.

## Install Pulumi

First we need to setup Pulumi, at the time of the writing current version is v3.94.2.

```
pip install pulumi
```

Additional modules needed are *pulumi_azure:*

```
pip install pulumi_azure
```

And azure plugin version at the time of writing v5.57.0:

```
pulumi plugin install resource azure
```

New azure-python project

```
pulumi new azure-python
```

When you have everything setup just spin

```
pulumi up
```

When done with the resource it can be deleted with

```
pulumi destroy
```

## Multiple stacks

Pulumi supports multiple stacks (dev, stage, prod etc.)

You can see stacks with

```
pulumi stack ls
```

For more information plese see [stacks](https://www.pulumi.com/docs/concepts/stack/)

## Pulumi Authentication

In order to enable Pulumi to interact with you're Azure subscription there are multiple options to register you're py-pulumi app with Azure.

For fast setup you can use **Azure CLI** but preffered way is to use authentication with **Service Principal.**

### **Azure CLI**

How to install Azure CLI please follow [link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

On you're terminal just use

```
az login
```

You will be redirected to browser to enter user authentication. Once logged-in you can quit browser and return to console where hopefully you will find information about Azure CLI connection in form:

```
{
    "cloudName": "AzureCloud",
    "homeTenantId": "xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
    "id": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx",
    "isDefault": true,
    "managedByTenants": [
      {
        "tenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx"
      }
    ],
    "name": "Visual Studio Enterprisek",
    "state": "Enabled",
    "tenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx",
    "user": {
      "name": "user@company.com",
      "type": "user"
    }
  }
```

When logged in you need to configure pulumi to use azure cli with:

```
pulumi config set cloud:useAzureCli true
```

### Service Principal

There are multiple resources on this topic so you can follow this to find out more about Service Principal authentication of the apps [link](https://learn.microsoft.com/en-us/cli/azure/azure-cli-sp-tutorial-1?tabs=bash)

Create new application

1. In the left navigation pane, click on "Azure Active Directory."
2. Under "App registrations," click on "New registration."
3. Provide a name for your application, select the appropriate account type, and enter a redirect URI if required. Click "Register."
4. Note down the "Application (client) ID" and "Directory (tenant) ID" from the overview page. These will be needed for configuring Pulumi.

Add client secret

1. In the left navigation pane, click on "Certificates & Secrets."
2. Under "Client secrets," click on "New client secret." Enter a description, choose an expiry period, and click "Add."
3. Note down the value of the client secret immediately. This will be needed for configuring Pulumi.

Adjust permissions

1. In the left navigation pane, click on "API permissions."
2. Ensure that your application has the necessary permissions to manage Azure resources. If needed, click on "Add a permission" and grant the required permissions.

### Configure Pulumi with Azure Credentials

```
pulumi config set azure:clientId <Application (client) ID>
pulumi config set azure:clientSecret <Client Secret>
pulumi config set azure:tenantId <Directory (tenant) ID>
pulumi config set azure:subscriptionId <Your Azure Subscription ID>
```

On the end of the configuration confirm settings with

```
pulumi up
```

## **Pulumi Secrets**

Another great aspect of Pulumi is built-in secret manger. You can store and retrieve secrets with:

Store/set

```
pulumi config set myApiKey <your-secret-api-key>
```

In you're program to retrieve the secret you can do:

```python
import pulumi

config = pulumi.Config()

# Access the secret
api_key = config.require_secret("myApiKey")

# Use the secret in your infrastructure definition
# (Replace this with the actual resource where the secret is needed)
my_resource = SomeResource(name="example", api_key=api_key)
```

## Set service resource info

There are couple parameters that can be changed using Pulumi config or default will be used:

```
location = config.get("location") or "West Europe"
res_group = config.get("resource_group") or "test_group"
vm_size = config.get("vm_size") or "Standard_D2_v2"
node_count = config.get("node_count") or 2
env = config.get("environment") or "Development"
```

To set each of the config params use:

```
pulumi config set location <location_name>
```

In case you wan't to use already existing resource group please advise [link](https://www.pulumi.com/ai/answers/vL7zWqGtZqQHwJBLd4MnUC/accessing-existing-azure-resource-group). It is recommended to use new resource group or use GET function to fetch already existing resource group.

## Results

On end of pulumi up command depending on the time but it can take up to 10 minutes the resources are ready to use.

Notice that on end of the pulumi create/deploy process there are **export** commands that will enable you to access information from resource creation.

This is important in order to setup you're **kubectl** config.

To see pulumi output use:

```
pulumi stack output kubeConfig
pulumi stack output clientCertificate
```

To confirm successfull operation you can navigate to Azure Portal and under specified resource group you should find newly created service and as first step you can use:

```
pulumi stack output kubeConfig --show-secrets
```

or you can output it to yaml file:

```
pulumi stack output kubeConfig --show-secrets > kubeConfig.yaml
```

This should look something like this:

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: 
    server: https://hcp.westeurope..io:443
  name: testAKSCluster156d878
contexts:
- context:
    cluster: testAKSCluster156d878
    user: clusterUser_test-group_testAKSCluster156d878
  name: testAKSCluster156d878
current-context: testAKSCluster156d878
kind: Config
preferences: {}
users:
- name: clusterUser_test-group_testAKSCluster156d878
  user:
    client-certificate-data: 
    client-key-data: 
    token: 
```



## Update kubectl info

When you have you're yaml file ready you can use it to connect kubectl

```
export KUBECONFIG=./kubeconfig.yaml
```

In order to run kubectl (install kubectl from [here](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)) make sure to install suitable distribution.

All is left is to run

```
kubectl get pods
```

Output should be something like:

```
NAME                              STATUS   ROLES   AGE   VERSION
aks-default-27290676-vmss000000   Ready    agent   37m   v1.26.6
aks-default-27290676-vmss000001   Ready    agent   37m   v1.26.6
```

You have already running two running pods which are AKS cluster internal components and part of the infrastructure. You can read more [here](https://learn.microsoft.com/en-us/azure/aks/concepts-clusters-workloads).

## Destroy

On the end you can use

```
pulumi destroy
```

to delete the created resources under the current stack. Please note that you will be prompted for confirmation. Additionally please take care when deleting resouce groups if some other resources are deployed under the resource group this could result in pulumi destroy failure. Then it will be for the best for leftover resources and delete them manually.

and to completely remove the created stack

```
pulumi stack rm <stack_name>
```

Destroy process can take up to couple of minutes.
