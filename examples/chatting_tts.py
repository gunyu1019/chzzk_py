import io
import gtts
import pydub
import pydub.playback
from chzzkpy.chat import ChatClient, ChatMessage


# Configuration
channel_id = "21a85ed3ac126f622a05cd670c1be535"


client = ChatClient(channel_id)


@client.event
async def on_connect():
    print("Ready bot.")


@client.event
async def on_chat(message: ChatMessage):
    tts = gtts.gTTS(text=message.content, lang="ko", slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    # WIP


client.run()
