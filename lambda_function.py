import json
import requests
from supabase_client import get_supabase
from utils import get_files_by_project, update_scan_status, scan_files
from config import API_GATEWAY_URL


supabase = get_supabase()


def lambda_handler(event, context):
    # Get message from the queue event
    # For example, if using SQS, the message would be in event['Records'][0]['body']
    message = event.get("Records", [{}])[0].get("body", {})

    data = json.loads(message)

    if "scan_id" not in data:
        return {"statusCode": 400, "body": json.dumps("Missing scan_id in message")}

    if "project_id" not in data:
        return {"statusCode": 400, "body": json.dumps("Missing project_id in message")}

    # Process the message
    scan_id = data["scan_id"]
    project_id = data["project_id"]
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

    # files = get_files_by_project(project_id)

    # if not files:
    #     update_scan_status(
    #         scan_id=scan_id,
    #         status=-1,
    #     )
    #     return {"statusCode": 404, "body": json.dumps("No files found")}

    # scan_files(scan_id=scan_id, project_id=project_id, files=files)

    res = requests.post(
        f"{API_GATEWAY_URL}/bandit/",
        json={"scan_id": scan_id, "project_id": project_id},
    )

    if res.status_code != 200:
        print(f"Error in scan.")
        update_scan_status(
            scan_id=scan_id,
            status=-1,
        )
        return {"statusCode": 500, "body": json.dumps("Scan failed")}

    print(f"Scan completed for ID: {scan_id}")

    return {"statusCode": 200, "body": json.dumps("Scan is completed!")}


def test_lambda_handler():
    event = {
        "Records": [
            {
                "messageId": "72b69545-c131-4aae-830b-81bbedbb832f",
                "receiptHandle": "AQEBOurZ/kYC+Fxt0c8OtWW98REetWV/2Pd2fgJSZAlkWHSfCjvbXAeQ8YplIAFcBOUbNBjzwfGLQSJUVOI2Knk68AM+njQ65h6dMFuMWTCBirtpeuq7Y8SPUgRZW131pcH4oN+GRTGXWi/8x2BMdwzL6t5lvljsh/mZ4px6pdnn7Q5jGnPDjiEwBVVWeiG/EgZwqyoNzivNehSjSsq5oQ2C0Vc6iA6+/a/eHY0jiXXfQVC88Tn83Kdl4G25WUZ8Rk2urxIeVzMw07Ng9D+AF3HbAJc9WirIXhSf5AhC0PQCZf2L0pTZYcfPbTMdr6sHSxTWOFCuGvwpUe/j1ZfjKgvXD3+B1UOOFr6lZyM9oXFblhHgqhZlY686ABXtVsiIT81koQAfz5hoW790Lm90/Njc8w==",
                "body": '{"scan_id": "fcd30681-f90c-4ebc-bbfb-92f17c9d65d4", "project_id": "a2724a5f-5e7f-4c62-9252-4f8ff8ea912c"}',
                "attributes": {
                    "ApproximateReceiveCount": "3",
                    "SentTimestamp": "1746736446997",
                    "SenderId": "AIDA2FXADWYB3CEHXCZ7R",
                    "ApproximateFirstReceiveTimestamp": "1746736447006",
                },
                "messageAttributes": {},
                "md5OfBody": "5fe3cbaf4ad8dfa80ef9216d5d209d9d",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:699475932675:vulnscan-scans-queue",
                "awsRegion": "us-east-1",
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    # Run the test


if __name__ == "__main__":
    test_lambda_handler()
    print("All tests passed!")
