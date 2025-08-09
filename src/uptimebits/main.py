import json
import boto3
import uuid
import os
# train_assistant/main.py
# Run this script from the parent directory: python -m train_assistant.main

from agent.agent_executor import agent_executor
from context.conversation import context

# if __name__ == "__main__":
def lambda_handler(event, context):
    user_input = json.loads(event["body"])["question"]
    response = agent_executor.invoke({"input": user_input})

    # Extract HTML text from LangChain output
    answer_html = ""
    if isinstance(response.get("output"), list) and len(response["output"]) > 0:
        answer_html = response["output"][0].get("text", "")
    elif isinstance(response.get("output"), str):
        answer_html = response["output"]

    # Build frontend-compatible payload
    frontend_payload = {
        "status_code": 200,
        "status": True,
        "message": "Message sent",
        "data": {
            "conversation": [
                {
                    "messageid": str(uuid.uuid4()),  # Generate a unique ID
                    "session_id": None,
                    "question": user_input,
                    "answer": answer_html,
                    "errormsg": None,
                    "quickReplies": None
                }
            ]
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps(frontend_payload),
    }
