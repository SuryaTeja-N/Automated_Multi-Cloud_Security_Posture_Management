provider "azurerm" {
  features {}

  subscription_id = var.AZURE_SUBSCRIPTION_ID
  tenant_id       = var.AZURE_TENANT_ID
  client_id       = var.AZURE_CLIENT_ID
  client_secret   = var.AZURE_CLIENT_SECRET

}

resource "azurerm_storage_account" "example" {
  name                     = "securestorageacct143"
  resource_group_name      = "myResourceGroup_surya"
  location                 = "East US"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Name = "MySecureStorage"
  }
}
