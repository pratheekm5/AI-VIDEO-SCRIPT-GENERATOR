# app/services/agent_service.py

import asyncio
import os
from typing import List
from fastapi import HTTPException
from portia import Portia, Config
from dotenv import load_dotenv

# We only need settings for the GOOGLE_API_KEY
from app.core.config import settings

def _generate_script_sync(
    transcripts: List[str],
    host_name: str,
    channel_name: str,
    signature_lines: List[str],
    additional_instructions: str
) -> str:
    """
    This function is a direct implementation of your working script.
    """
    try:
        # --- YOUR EXACT LOGIC STARTS HERE ---

        # 1. Load and Set the API Key
        print("🔧 Loading environment variables...")
        load_dotenv()

        # CHANGED: Get GOOGLE_API_KEY from our secure settings object
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the .env file.")
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # 2. Initialize the Portia Client with Correct Configuration
        print("\n🤖 Initializing the Portia client...")
        config = Config.from_default(default_model="google/gemini-1.5-flash") # Using a more recent model
        portia_client = Portia(config=config)
        print("✅ Portia client initialized successfully.")

        # 3. Define the Task as a Natural Language Query
        # CHANGED: Uses parameters from the API request instead of hardcoded variables.
        query = f"""
        Generate a complete and engaging YouTube video script based on the following detailed requirements:

        **Host and Channel:**
        - The host's name is "{host_name}".
        - The channel is called "{channel_name}".

        **Core Content to Synthesize:**
        - The script must smoothly integrate these topics: {transcripts}

        **Style and Format Instructions:**
        - Adhere strictly to these creative guidelines: "{additional_instructions}".

        **Mandatory Outro:**
        - The script must end *exactly* with the following lines, in this order: {signature_lines}

        Execute this task and provide only the final, complete script as your output.
        """

        # 4. Create and Run the Plan
        print("\n🚀 Commanding Portia client to create and run the plan...")
        print("  - Step 1: Generating the plan...")
        plan = portia_client.plan(query=query)
        print("  - Plan generated successfully.")
        
        print("  - Step 2: Executing the plan...")
        plan_run = portia_client.run_plan(plan=plan)
        print("  - Plan executed successfully.")

        final_script = plan_run.outputs
        
        # 5. Return the final result
        # CHANGED: Returns the script to the API instead of printing.
        if isinstance(final_script, dict) and 'output' in final_script:
            return final_script['output']
        elif isinstance(final_script, str):
            return final_script
        else:
            return str(final_script)

    except Exception as e:
        # CHANGED: Raise an error for the API to catch.
        print(f"❌ Portia's mission failed: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred with the AI agent: {str(e)}")


async def generate_portia_script(request_data: dict) -> str:
    """
    Async wrapper to run your synchronous code in a thread.
    """
    # This check now ONLY checks for the Google key, as you requested.
    if not settings.GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY must be set in the .env file.")

    return await asyncio.to_thread(_generate_script_sync, **request_data)