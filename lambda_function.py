import json
from supabase_client import get_supabase
from utils import get_files_by_project, update_scan_status, scan_files

supabase = get_supabase()


def lambda_handler(event, context):
    # Get message from the queue event
    # For example, if using SQS, the message would be in event['Records'][0]['body']
    message = event.get("Records", [{}])[0].get("body", {})

    if "scan_id" not in message:
        return {"statusCode": 400, "body": json.dumps("Missing scan_id in message")}

    if "project_id" not in message:
        return {"statusCode": 400, "body": json.dumps("Missing project_id in message")}

    # Process the message
    scan_id = message["scan_id"]
    project_id = message["project_id"]
    print(f"Received Scan ID: {scan_id}")
    print(f"Received Project ID: {project_id}")

    # Check if scan is valid
    scan = (
        supabase.table("scans")
        .select("*")
        .eq("id", scan_id)
        .eq("project_id", project_id)
        .execute()
    )

    if not scan.data:
        print(f"Scan not found for ID: {scan_id} and Project: {project_id}")
        return {"statusCode": 404, "body": json.dumps("Scan not found")}

    # Check if scan is already in progress
    if scan.data[0]["status"] != 0:
        print(f"Scan already processed for ID: {scan_id}")
        return {"statusCode": 400, "body": json.dumps("Scan already processed")}

    # Update scan status to in progress
    update_scan_status(
        scan_id=scan_id,
        status=1,
    )

    files = get_files_by_project(project_id)

    if not files:
        update_scan_status(
            scan_id=scan_id,
            status=-1,
        )
        return {"statusCode": 404, "body": json.dumps("No files found")}

    scan_files(scan_id=scan_id, project_id=project_id, files=files)

    print(f"Scan completed for ID: {scan_id}")

    return {"statusCode": 200, "body": json.dumps("Scan is completed!")}


def test_lambda_handler():
    event = {
        "Records": [
            {
                "messageId": "11d6ee51-4cc7-4302-9e22-7cd8afdaadf5",
                "receiptHandle": "AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...",
                "body": {
                    "scan_id": "312f7035-42ff-4ff4-8c89-620562bf7e62",
                    "project_id": "288732f8-56b7-473c-ba3f-b7194d3ff4d5",
                },
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1573251510774",
                    "SequenceNumber": "18849496460467696128",
                    "MessageGroupId": "1",
                    "SenderId": "AIDAIO23YVJENQZJOL4VO",
                    "MessageDeduplicationId": "1",
                    "ApproximateFirstReceiveTimestamp": "1573251510774",
                },
                "messageAttributes": {},
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:fifo.fifo",
                "awsRegion": "us-east-2",
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    # Run the test


if __name__ == "__main__":
    test_lambda_handler()
    print("All tests passed!")
