import pulumi
from pulumi import Config
import pulumi_azure_native as azure_native
import pulumi_azure as azure

# Retrieve Azure configuration
config = Config()
location = config.get("location") or "West Europe"
res_group = config.get("resource_group") or "test-group"
vm_size = config.get("vm_size") or "Standard_D2_v2"
node_count = config.get("node_count") or 2
env = config.get("environment") or "Development"
dns_prefix = config.get("dns_prefix") or "testAKSCluster"
dns_prefix_private_cluster = config.get("dns_prefix_private_cluster") or None

# Create an Azure Resource Group
resource_group = azure_native.resources.ResourceGroup("resourceGroup",
    location=location,
    resource_group_name=res_group)

# Create an AKS cluster
aks_cluster = azure.containerservice.KubernetesCluster("testAKSCluster",
    location=resource_group.location,
    resource_group_name=resource_group.name,
    dns_prefix=dns_prefix,
    dns_prefix_private_cluster=dns_prefix_private_cluster,
    default_node_pool=azure.containerservice.KubernetesClusterDefaultNodePoolArgs(
        name="default",
        node_count=node_count,
        vm_size=vm_size,
    ),
    identity=azure.containerservice.KubernetesClusterIdentityArgs(
        type="SystemAssigned",
    ),
    tags={
        "Environment": "Development",
    })
pulumi.export("clientCertificate", aks_cluster.kube_configs[0].client_certificate)
pulumi.export("kubeConfig", aks_cluster.kube_config_raw)