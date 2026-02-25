from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import yt_dlp

API_ID = 30672858
API_HASH = "d14a1569149738de4c08f20d6233fa5f"
BOT_TOKEN = "8297448324:AAGsQJPL6UluNTNFP5xwKUmTvlL_BxvCVyA"

app = Client("vc_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

def get_audio(query):
    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True,
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info['entries'][0]['url']

@app.on_message(filters.command("play"))
async def play(_, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    await message.reply("🔎 Searching...")

    audio_url = get_audio(query)

    await call_py.join_group_call(
        chat_id,
        AudioPiped(
            audio_url,
            HighQualityAudio(),
        ),
    )

    await message.reply("🎶 Playing now in VC!")

app.start()
call_py.start()
import idle
idle()



