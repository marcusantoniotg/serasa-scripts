# Create a resource group
resource "azurerm_resource_group" "resourcegroup_aulas" {
  name     = "${local.tags["resourcegroup"]}"
  location = "${local.tags["azureregion"]}"
  tags = var.tags
}