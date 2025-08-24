# ==============================================================================
#  Portia AI in Action (V7 - Final Corrected Version)
#
#  This version fixes the InvalidConfigError by:
#  1. Requiring a valid GOOGLE_API_KEY.
#  2. Cleaning up the configuration to a single, clear definition.
#  3. Using a standard, valid model name.
# ==============================================================================

# 1. First, install the necessary libraries
# pip install portia-ai google-generativeai python-dotenv
import os
from portia import Portia, Config
from dotenv import load_dotenv

# --- 2. Load and Set the API Key ---
print("🔧 Loading environment variables...")
load_dotenv() # Loads variables from a .env file first, if it exists

# CRITICAL FIX: Replace the placeholder with your actual Google API Key.
# The previous error was because this was an empty string.
api_key = "AIzaSyCkEOhVhFpPbkXE93OIDsf-0CGGI7b30xM"
os.environ["GOOGLE_API_KEY"] = api_key

# --- 3. Initialize the Portia Client with Correct Configuration ---
print("\n🤖 Initializing the Portia client...")
try:
    # We define the configuration in one clean step.
    # The provider is inferred from the model name prefix "gemini/".
    config = Config.from_default(default_model="google/gemini-2.0-flash")
    
    portia_client = Portia(config=config)
    print("✅ Portia client initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize Portia client: {e}")
    exit()

# --- 4. Define the Task as a Natural Language Query ---
# (This section is correct and remains unchanged)
transcripts = [
    "AI is transforming industries. Machine learning helps in healthcare...",
    "The future of technology looks bright with new breakthroughs...",
    "We need to consider ethics in AI development..."
]
host_name = "Sarah Tech"
video_duration = "10 min"
channel_name = "Future Insights"
signature_lines = ["Stay curious!", "Don't forget to subscribe!"]
additional_instructions = "Make it conversational, include questions for the audience, and keep the spoken script under a 5-minute read time."

query = f"""
Generate a complete and engaging YouTube video script based on the following detailed requirements:

**Host and Channel:**
- The host's name is "{host_name}".
- The channel is called "{channel_name}".

**Core Content to Synthesize:**
- The script must smoothly integrate these topics:
  1. "{transcripts[0]}"
  2. "{transcripts[1]}"
  3. "{transcripts[2]}"

**Style and Format Instructions:**
- Adhere strictly to these creative guidelines: "{additional_instructions}".

**Mandatory Outro:**
- The script must end *exactly* with the following lines, in this order:
  - "{signature_lines[0]}"
  - "{signature_lines[1]}"

Execute this task and provide only the final, complete script as your output.
"""

# --- 5. Create and Run the Plan ---
print("\n🚀 Commanding Portia client to create and run the plan...")

if not api_key or api_key == "YOUR_GOOGLE_API_KEY_HERE":
    print("❌ ERROR: Please set your GOOGLE_API_KEY in the script before running.")
else:
    try:
        print("  - Step 1: Generating the plan...")
        plan = portia_client.plan(query=query)
        print("  - Plan generated successfully.")
        
        print("  - Step 2: Executing the plan...")
        plan_run = portia_client.run_plan(plan=plan)
        print("  - Plan executed successfully.")

        # --- 6. Present the Final Result ---
        # final_script = plan_run.state.output
        final_script = plan_run.outputs
        
        print("\n" + "="*50)
        print("🎬 PORTIA'S EXECUTED PLAN: FINAL SCRIPT 🎬")
        print("="*50 + "\n")
        print(final_script)

    except Exception as e:
        print(f"❌ Portia's mission failed during plan creation or execution: {e}")