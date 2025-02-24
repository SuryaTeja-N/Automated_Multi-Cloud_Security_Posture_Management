import json
import boto3
import requests
import os

# Initialize AWS Security Hub client
SECURITY_HUB = boto3.client('securityhub')
SLACK_WEBHOOK_URL = os.getenv("SLACK_API_TOKEN")

def lambda_handler(event, context):
    findings = SECURITY_HUB.get_findings(
        Filters={
            'SeverityLabel': [{'Value': 'CRITICAL', 'Comparison': 'EQUALS'}]
        }
    )

    if findings['Findings']:
        for finding in findings['Findings']:
            alert_message = f"🚨 *Security Alert* 🚨\n*Title:* {finding['Title']}\n*Severity:* {finding['Severity']['Label']}\n*Resource:* {finding['Resources'][0]['Id']}"
            requests.post(SLACK_WEBHOOK_URL, json={"text": alert_message})

    return {"statusCode": 200, "body": "Alerts processed"}
