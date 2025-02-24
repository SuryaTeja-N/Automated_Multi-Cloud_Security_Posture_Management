import logging
import azure.functions as func
import os
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

# Get Subscription ID from environment variables
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

# Authenticate with Azure
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)

def enforce_storage_encryption(resource_group, storage_account):
    try:
        logging.info(f"Checking encryption for {storage_account}...")
        account = storage_client.storage_accounts.get_properties(resource_group, storage_account)

        if not account.encryption.services.blob.enabled:
            logging.info(f"Enforcing encryption on {storage_account}...")
            storage_client.storage_accounts.update(
                resource_group,
                storage_account,
                {"encryption": {"services": {"blob": {"enabled": True}}}}
            )
            logging.info(f"✅ Encryption enabled for {storage_account}.")
        else:
            logging.info(f"✅ Storage account {storage_account} is already encrypted.")
    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")

# ✅ HTTP Trigger (Existing)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function Triggered")

    try:
        data = req.get_json()
        resource_group = data.get("resource_group")
        storage_account = data.get("storage_account")

        if not resource_group or not storage_account:
            return func.HttpResponse("❌ Missing parameters", status_code=400)

        enforce_storage_encryption(resource_group, storage_account)
        return func.HttpResponse(f"✅ Encryption enforced for {storage_account}.", status_code=200)
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("❌ Internal Server Error", status_code=500)

# ✅ New Queue Trigger to Process Defender Alerts
def queue_trigger(msg: func.QueueMessage) -> None:
    try:
        message_body = msg.get_body().decode('utf-8')
        alert = json.loads(message_body)

        title = alert.get("Title", "Unknown Alert")
        severity = alert.get("Severity", "Unknown Severity")
        description = alert.get("Description", "No description available")

        logging.info(f"🔔 Security Alert Received: {title}")
        logging.info(f"⚠️ Severity: {severity}")
        logging.info(f"📖 Description: {description}")

    except Exception as e:
        logging.error(f"❌ Error processing queue message: {str(e)}")
