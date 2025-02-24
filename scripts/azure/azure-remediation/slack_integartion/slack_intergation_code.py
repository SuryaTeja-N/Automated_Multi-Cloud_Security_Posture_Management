import logging
import requests
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.security import SecurityCenter

SLACK_WEBHOOK_URL = os.getenv("SLACK_API_TOKEN")

def main(req):
    logging.info("Azure Defender Security Alert Function Triggered")

    try:
        # Authenticate with Azure
        credential = DefaultAzureCredential()
        security_client = SecurityCenter(credential)

        # Fetch security alerts
        alerts = security_client.alerts.list()

        for alert in alerts:
            if alert.severity == "High":
                alert_message = f"🚨 *Azure Security Alert* 🚨\n*Title:* {alert.display_name}\n*Severity:* {alert.severity}\n*Description:* {alert.description}"
                requests.post(SLACK_WEBHOOK_URL, json={"text": alert_message})

    except Exception as e:
        logging.error(f"Error fetching security alerts: {e}")

    return {"status": 200, "message": "Alerts processed"}
