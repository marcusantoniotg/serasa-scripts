resource "azurerm_storage_account" "storageaccount_aulas" {
  name                     = "${local.tags["storageaccount"]}"
  resource_group_name      = "${local.tags["resourcegroup"]}"
  location                 = "${local.tags["azureregion"]}"
  account_tier             = "Standard"
  account_replication_type = "GRS"
  tags = var.tags
  
  depends_on = [
    azurerm_resource_group.resourcegroup_aulas
  ]
}