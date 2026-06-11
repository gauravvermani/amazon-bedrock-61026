import boto3
import json
from botocore.exceptions import ClientError
from config import AWS_REGION


class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION
        )

    def invoke(self, model_id: str, prompt: str, max_tokens: int = 200):
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            print(f"[ERROR] Bedrock call failed [{error_code}]: {e}")
            return None

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]


if __name__ == "__main__":
    print("This is a module. Run main.py instead: python src/main.py")
