# ============================================================
# bedrock_client.py — This file is our "translator."
# It knows HOW to talk to Amazon Bedrock's AI service.
# It packages up our question, sends it, and reads the reply.
# ============================================================

# boto3 is Amazon's official Python library.
# It lets Python programs talk to AWS services like Bedrock, S3, etc.
# Think of it like an app on your phone that connects to a website.
import boto3

# json lets us convert Python data (like dictionaries) into a format
# called JSON that computers and web services understand.
# JSON looks like: {"key": "value"} — similar to a Python dictionary.
import json

# ClientError is a special error type from AWS.
# It fires when something goes wrong with an AWS service call —
# like wrong permissions, wrong model name, or no internet.
from botocore.exceptions import ClientError

# We pull in the AWS region setting from our config file.
# A "region" is a physical Amazon data center location.
# "us-east-1" = Northern Virginia, USA.
from config import AWS_REGION


# ============================================================
# BedrockClient is a "class" — think of it as a blueprint.
# From this blueprint, we build one object (our remote control)
# that knows how to send questions to the AI and get answers back.
# ============================================================
class BedrockClient:

    def __init__(self):
        # -------------------------------------------------------
        # __init__ runs automatically when you create a BedrockClient.
        # It's like the setup screen when you first open a new app.
        #
        # Here we create an AWS "client" — a live connection
        # to the Bedrock Runtime service (the part that runs AI models).
        #
        # "bedrock-runtime" = the AWS service that actually runs the AI.
        # region_name       = which Amazon data center to use.
        # -------------------------------------------------------
        self.client = boto3.client(
            "bedrock-runtime",      # Service name on AWS
            region_name=AWS_REGION  # Location of the data center
        )

    def invoke(self, model_id: str, prompt: str, max_tokens: int = 200):
        # -------------------------------------------------------
        # invoke() is the main action — it sends a question to the AI.
        #
        # Parameters (inputs to this function):
        #   model_id   → which AI model to use (like picking a subject tutor)
        #   prompt     → the actual question or instruction for the AI
        #   max_tokens → max length of the AI's answer (default: 200 words-ish)
        # -------------------------------------------------------

        # -------------------------------------------------------
        # Build the "body" — this is the message package we send to AWS.
        # It's like filling out a form before submitting it.
        #
        # anthropic_version → tells AWS which version of the message
        #                     format we're using (required by Anthropic/Claude)
        # max_tokens        → the answer length limit we set
        # messages          → a list of chat messages (like a text thread)
        #   role: "user"    → means WE are the ones asking
        #   content         → the actual question text
        # -------------------------------------------------------
        body = {
            "anthropic_version": "bedrock-2023-05-31",  # Required format version
            "max_tokens": max_tokens,                    # Cap the response length
            "messages": [
                {
                    "role": "user",      # We are the "user" in this conversation
                    "content": prompt    # Our actual question goes here
                }
            ]
        }

        # -------------------------------------------------------
        # Try to call the AI. If something goes wrong (wrong key,
        # wrong model name, no internet), we catch the error and
        # print a helpful message instead of crashing the whole program.
        # This is like a safety net under a tightrope walker.
        # -------------------------------------------------------
        try:
            # Send the question to AWS Bedrock and wait for a reply.
            # invoke_model() is the actual API call to Amazon's servers.
            #
            # modelId       → which AI brain to use
            # body          → our question package (converted to JSON text)
            # contentType   → tells AWS our package is in JSON format
            # accept        → tells AWS we want the reply in JSON format
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),           # Convert dict → JSON string
                contentType="application/json",  # We're sending JSON
                accept="application/json"        # We want JSON back
            )

        except ClientError as e:
            # -------------------------------------------------------
            # If AWS returns an error, we land here instead of crashing.
            #
            # e.response["Error"]["Code"] → the short error name from AWS
            #   e.g. "AccessDeniedException" = you don't have permission
            #        "ValidationException"   = bad model ID or bad input
            #        "ThrottlingException"   = too many requests, slow down
            # -------------------------------------------------------
            error_code = e.response["Error"]["Code"]
            print(f"[ERROR] Bedrock call failed [{error_code}]: {e}")
            return None  # Return nothing so the program doesn't crash

        # -------------------------------------------------------
        # Parse the response.
        # AWS sends back raw bytes (computer-speak), so we:
        #   1. .read()       → convert bytes into a text string
        #   2. json.loads()  → convert JSON text into a Python dictionary
        # -------------------------------------------------------
        result = json.loads(response["body"].read())

        # -------------------------------------------------------
        # Dig into the response to find the actual text answer.
        # The structure looks like:
        #   result
        #   └── "content"        (a list of response blocks)
        #       └── [0]          (first block — usually the only one)
        #           └── "text"   (the actual words the AI wrote)
        # -------------------------------------------------------
        return result["content"][0]["text"]


# ============================================================
# If someone accidentally runs THIS file directly instead of main.py,
# this message tells them what to do instead.
# (Running this file alone won't do anything useful.)
# ============================================================
if __name__ == "__main__":
    print("This is a module — not the entry point.")
    print("Run the program with: python src/main.py")
