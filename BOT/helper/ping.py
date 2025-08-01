from FUNC.defs import *
from pyrogram import Client, filters
import time


@Client.on_message(filters.command("ping", [".", "/"]))
async def cmd_ping(client, message):
    try:
        start = time.perf_counter()
        resp  = """<b>
🤖 Checking 𝐂𝐇𝐀𝐑𝐆𝐄 𝐌𝐀𝐒𝐓𝐄𝐑 𝗣𝗶𝗻𝗴...
        </b>"""
        edit  = await message.reply_text(resp, quote=True)
        end   = time.perf_counter()
        
        textb = f"""<b>
🤖 𝗕𝗼𝘁 𝗡𝗮𝗺𝗲: 𝐂𝐇𝐀𝐑𝐆𝐄 𝐌𝐀𝐒𝐓𝐄𝐑
✅ 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗥𝘂𝗻𝗻𝗶𝗻𝗴
📶 𝗣𝗶𝗻𝗴: {(end-start)*1000:.2f} 𝗺𝘀
        </b>"""
        await client.edit_message_text(message.chat.id, edit.id, textb)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
