import asyncio

from dotenv import load_dotenv
import os
load_dotenv()

from livekit.agents import AutoSubscribe, JobContext, cli, llm, WorkerOptions
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero



api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API Key loaded successfully.")
else:
    raise EnvironmentError("OPENAI_API_KEY not found. Please ensure it is set in your environment or .env file.")

# Set the OpenAI API key explicitly
openai.api_key = "key"

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role = "system",
        text = ("You are a voice assistant made by LiveKit and you will be interacting with voice"
                "You should use short and concise responses"
                ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt = openai.STT(),
        llm = openai.LLM(),
        tts = openai.TTS(),
        chat_ctx=initial_ctx
    )

    assistant.start(ctx.room)
    await asyncio.sleep(1)
    await assistant.say("Hola, it's the AI Adnan!", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))