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

There are couple parameters that can be changed using Pulumi config
