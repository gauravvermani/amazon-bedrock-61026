# ============================================================
# app.py — This is the STARTING POINT of our program.
# When you run this file, it kicks everything else off.
# Think of it like the "Play" button on a video game.
# ============================================================

# We're bringing in our custom BedrockClient "tool" from another file.
# BedrockClient is like a remote control for talking to Amazon's AI.
from bedrock_client import BedrockClient

# We're also bringing in the MODEL_ID from our config file.
# MODEL_ID tells Amazon WHICH AI brain we want to use.
from config import MODEL_ID


def main():
    # -----------------------------------------------------------
    # Step 1: Create our AI remote control (BedrockClient).
    # This sets up the connection to Amazon's servers.
    # It's like turning on your TV before you can change channels.
    # -----------------------------------------------------------
    bedrock = BedrockClient()

    # -----------------------------------------------------------
    # Step 2: Send a question to the AI and wait for an answer.
    # - model_id  → which AI model to use (like picking a teacher)
    # - prompt    → the question we're asking the AI
    # - max_tokens → how long the answer can be (like a word limit)
    #   Note: 1 token ≈ 1 word, so 200 tokens ≈ 200 words max
    # -----------------------------------------------------------
    output = bedrock.invoke(
        model_id=MODEL_ID,
        prompt="Explain AWS Bedrock in simple terms",
        max_tokens=200
    )

    # -----------------------------------------------------------
    # Step 3: Print the AI's answer to the terminal screen.
    # The "\n" just means "start a new line" — like pressing Enter.
    # -----------------------------------------------------------
    print("\n=== RESPONSE ===\n")
    print(output)


# -----------------------------------------------------------
# This is a Python safety check.
# It means: "Only run main() if YOU directly ran this file."
# If another file imports this one, main() won't auto-run.
# Think of it like a door that only opens when YOU knock.
# -----------------------------------------------------------
if __name__ == "__main__":
    main()
