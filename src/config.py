# ============================================================
# config.py — This is our "settings file."
# Instead of hard-coding values like region and model names
# all over the code, we store them HERE in one place.
# If you need to change a setting, you only change it once.
# Think of it like your phone's Settings app.
# ============================================================

# os lets Python interact with your computer's operating system.
# We use it here to READ environment variables.
# Environment variables are like secret sticky notes your
# computer keeps hidden from your code files.
import os

# python-dotenv reads a file called ".env" and loads those
# secret sticky notes into memory so os.getenv() can find them.
# Without this, Python wouldn't know about your .env file.
from dotenv import load_dotenv

# Actually load the .env file right now.
# After this line runs, all the key=value pairs in .env
# are available as environment variables.
load_dotenv()

# -------------------------------------------------------
# AWS_REGION — tells boto3 which Amazon data center to use.
#
# os.getenv("AWS_REGION", "us-east-1") means:
#   "Look for a variable called AWS_REGION in the environment.
#    If you can't find it, use 'us-east-1' as the default."
#
# us-east-1 = Northern Virginia, USA (Amazon's main region)
# -------------------------------------------------------
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# -------------------------------------------------------
# MODEL_ID — the exact name of the AI model we want to use.
#
# This comes ONLY from the .env file — there's no default.
# If it's missing from .env, MODEL_ID will be None,
# and the program will crash with a helpful AWS error.
#
# Current active model (as of June 2026):
#   us.anthropic.claude-haiku-4-5-20251001-v1:0
# -------------------------------------------------------
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")
