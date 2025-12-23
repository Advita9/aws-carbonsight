import json
import boto3
import os

bedrock = boto3.client("bedrock-runtime")


# ---------------------------
#  TITAN EMBEDDING FUNCTION
# ---------------------------
def embed_text(text: str):
    model_id = os.getenv("EMBED_MODEL_ID")  # e.g. amazon.titan-embed-text-v2:0

    body = {
        "inputText": text
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    data = json.loads(response["body"].read())
    return data["embedding"]


# ---------------------------
#  NOVA CHAT COMPLETION (Converse API)
# ---------------------------
def invoke_nova(model_id: str, prompt: str, max_tokens: int = 200):
    """
    Calls Amazon Nova using the Converse API.
    """

    messages = [
        {
            "role": "user",
            "content": [
                { "text": prompt }
            ]
        }
    ]

    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={
            "maxTokens": max_tokens,
            "temperature": 0.5,
            "topP": 0.9
        }
    )

    # Extract assistant text response
    return response["output"]["message"]["content"][0]["text"]
