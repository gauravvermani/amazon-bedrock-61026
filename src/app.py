from bedrock_client import BedrockClient
from config import MODEL_ID


def main():
    bedrock = BedrockClient()

    output = bedrock.invoke(
        model_id=MODEL_ID,
        prompt="Explain AWS Bedrock in simple terms",
        max_tokens=200
    )

    print("\n=== RESPONSE ===\n")
    print(output)


if __name__ == "__main__":
    main()
