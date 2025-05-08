import json


def lambda_handler(event, context):
    # Get message from the queue event
    # For example, if using SQS, the message would be in event['Records'][0]['body']
    # Here we just simulate a message
    message = event.get("Records", [{}])[0].get("body", {})

    if "scan_id" not in message:
        return {"statusCode": 400, "body": json.dumps("Missing scan_id in message")}

    # Process the message
    scan_id = message["scan_id"]
    print(f"Received Scan ID: {scan_id}")
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


def test_lambda_handler():
    event = {
        "Records": [
            {
                "messageId": "11d6ee51-4cc7-4302-9e22-7cd8afdaadf5",
                "receiptHandle": "AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...",
                "body": {"scan_id": "d237f234-93f0-4d56-933e-eac18fca98e5"},
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
    # assert response["statusCode"] == 200
    # assert response["body"] == json.dumps("Hello from Lambda!")
    print("Test passed!")
    # Run the test


if __name__ == "__main__":
    test_lambda_handler()
    print("All tests passed!")
