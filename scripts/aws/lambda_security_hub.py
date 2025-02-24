import json
import boto3

# AWS Clients
securityhub = boto3.client('securityhub')
sqs = boto3.client('sqs')

# Your SQS Queue URL
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/034362029668/SecurityHub-Findings-Queue"

def lambda_handler(event, context):
    try:
        # Get security findings
        response = securityhub.get_findings(
            Filters={
                'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}],
                'SeverityLabel': [{'Value': 'CRITICAL', 'Comparison': 'EQUALS'}]
            },
            MaxResults=10
        )

        findings = response.get("Findings", [])

        if not findings:
            print("No critical findings found.")
            return {"statusCode": 200, "body": "No findings to process"}

        for finding in findings:
            message_body = json.dumps({
                "Title": finding.get("Title"),
                "Severity": finding.get("Severity", {}).get("Label"),
                "Resource": finding.get("Resources")[0].get("Id") if finding.get("Resources") else "N/A",
                "Description": finding.get("Description"),
                "Remediation": finding.get("Remediation", {}).get("Recommendation", {}).get("Text", "N/A"),
            })

            # Send to SQS
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=message_body
            )

        return {"statusCode": 200, "body": "Findings sent to SQS"}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
