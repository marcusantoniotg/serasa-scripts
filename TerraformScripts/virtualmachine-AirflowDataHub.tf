# Configurando uma interface de rede
resource "azurerm_network_interface" "interfaceredevm-airflow" {
  name                = "cardinterface-airflow"
  location            = "${local.tags["azureregion"]}"
  resource_group_name = "${local.tags["resourcegroup"]}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subrede-aulas.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = local.tags["change_ip"] == 0 ? azurerm_public_ip.ippublico-airflow.id : null
  }
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_subnet.subrede-aulas,
    azurerm_public_ip.ippublico-airflow
  ]
}

resource "azurerm_virtual_machine" "vm-linux-airflow" {
  name                  = "${local.tags["virtualmachineAirflowDataHub"]}"
  location              = "${local.tags["azureregion"]}"
  resource_group_name   = "${local.tags["resourcegroup"]}"
  network_interface_ids = [azurerm_network_interface.interfaceredevm-airflow.id]
  vm_size               = "${local.tags["instancetype1"]}"

   delete_os_disk_on_termination = true
   delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  storage_os_disk {
    name              = "discosistemaAirflow"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "ubuntu-airflow"
    admin_username = "${local.tags["nomeusuariovm"]}"
    admin_password = "${local.tags["senhausuariovm"]}"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }

  provisioner "remote-exec" {
    connection {
      type = "ssh"
      host = azurerm_public_ip.ippublico-airflow.ip_address
      user = "${local.tags["nomeusuariovm"]}"
      password = "${local.tags["senhausuariovm"]}"
    }

    inline = "${local.install_docker}"
  }

  tags = var.tags
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_network_interface.interfaceredevm-airflow,
    azurerm_public_ip.ippublico-airflow
  ]
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "desligar-vm-airflow-automatico" {
  virtual_machine_id = azurerm_virtual_machine.vm-linux-airflow.id
  location           = azurerm_resource_group.resourcegroup_aulas.location
  enabled            = true

  daily_recurrence_time = "0200" # Coloque o horário desejável (padrao, 02h00min)
  timezone              = "E. South America Standard Time"

  notification_settings {
    enabled         = true
    time_in_minutes = "60"
    email = var.tags.Email
  }
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_network_interface.interfaceredevm-airflow,
    azurerm_virtual_machine.vm-linux-airflow
  ]
}

resource "azurerm_network_interface_security_group_association" "associa-grupo-recursos-vm-airflow" {
  network_interface_id      = azurerm_network_interface.interfaceredevm-airflow.id
  network_security_group_id = azurerm_network_security_group.securitygroup-aulas.id
  
  depends_on = [azurerm_resource_group.resourcegroup_aulas,
    azurerm_network_interface.interfaceredevm-airflow,
    azurerm_virtual_machine.vm-linux-airflow
  ]
}