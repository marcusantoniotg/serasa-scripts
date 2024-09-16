# Criando uma rede virtual para acessar a máquina remotamente
resource "azurerm_virtual_network" "network-aulas" {
  name                = "${local.tags["vnet"]}"
  address_space       = ["10.0.0.0/16"]
  location            = "${local.tags["azureregion"]}"
  resource_group_name = "${local.tags["resourcegroup"]}"
  tags = var.tags
  depends_on = [azurerm_resource_group.resourcegroup_aulas]
}

# Criando uma subnet
resource "azurerm_subnet" "subrede-aulas" {
  name                 = "${local.tags["subnet"]}"
  resource_group_name  = "${local.tags["resourcegroup"]}"
  virtual_network_name = azurerm_virtual_network.network-aulas.name
  address_prefixes     = ["10.0.0.0/24"]
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_virtual_network.network-aulas
  ]
}

# Criando um IP público (permitir conexão fora da rede Azure)
resource "azurerm_public_ip" "ippublico-dremio" {
  name                = "ippublico-dremio"
  location            = "${local.tags["azureregion"]}"
  resource_group_name = "${local.tags["resourcegroup"]}"
  allocation_method   = "${local.tags["vm_ip_allocated"]}"
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_virtual_network.network-aulas,
    azurerm_subnet.subrede-aulas
  ]
}

# Criando um IP público (permitir conexão fora da rede Azure)
resource "azurerm_public_ip" "ippublico-kafka" {
  name                = "ippublico-kafka"
  location            = "${local.tags["azureregion"]}"
  resource_group_name = "${local.tags["resourcegroup"]}"
  allocation_method   = "${local.tags["vm_ip_allocated"]}"
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_virtual_network.network-aulas,
    azurerm_subnet.subrede-aulas
  ]
}

# Criando um IP público (permitir conexão fora da rede Azure)
resource "azurerm_public_ip" "ippublico-airflow" {
  name                = "ippublico-airflow"
  location            = "${local.tags["azureregion"]}"
  resource_group_name = "${local.tags["resourcegroup"]}"
  allocation_method   = "${local.tags["vm_ip_allocated"]}"
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_virtual_network.network-aulas,
    azurerm_subnet.subrede-aulas
  ]
}