#Enforce Encryption on Storage Accounts

import os
from azure.mgmt.storage import StorageManagementClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
storage_client = StorageManagementClient(credential, subscription_id)

def enforce_storage_encryption(resource_group_name, account_name):
    account = storage_client.storage_accounts.get_properties(resource_group_name, account_name)
    if not account.encryption.services.blob.enabled:
        print(f"Enforcing encryption on {account_name}...")
        storage_client.storage_accounts.update(
            resource_group_name,
            account_name,
            {"encryption": {"services": {"blob": {"enabled": True}}}}
        )
        print(f"Encryption enabled for {account_name}.")

# Run the script for a sample storage account
enforce_storage_encryption("myResourceGroup_surya", "securestorageacct143")
