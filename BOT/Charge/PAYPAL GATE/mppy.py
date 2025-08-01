import json
import time
import threading
import asyncio
import httpx
from pyrogram import Client, filters
from datetime import timedelta
from FUNC.usersdb_func import *
from FUNC.defs import *
from .gate import create_paypal_charge
from .response import *
from TOOLS.check_all_func import *
from TOOLS.getcc_for_mass import *


async def paypal_mchkfunc(fullcc, user_id):
    retries = 3
    for attempt in range(retries):
        try:

            session = httpx.AsyncClient(
                timeout=30, follow_redirects=True)
            result = await create_paypal_charge(fullcc, session)
            getresp = await get_charge_resp(result, user_id, fullcc)
            response = getresp["response"]
            status = getresp["status"]

            await session.aclose()
            return f"Card↯ <code>{fullcc}</code>\n<b>Status - {status}</b>\n<b>Result -⤿ {response} ⤾</b>\n\n"

        except Exception as e:
            import traceback
            await error_log(traceback.format_exc())
            if attempt < retries - 1:
                await asyncio.sleep(0.5)
                continue
            else:
                return f"<code>{fullcc}</code>\n<b>Result - DECLINED ❌</b>\n"


@Client.on_message(filters.command("mpp", [".", "/"]))
def paypal_multi(Client, message):
    t1 = threading.Thread(target=paypal_bcall, args=(Client, message))
    t1.start()


def paypal_bcall(Client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(paypal_mass_auth_cmd(Client, message))
    loop.close()


async def paypal_mass_auth_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        first_name = str(message.from_user.first_name)
        checkall = await check_all_thing(Client, message)

        if not checkall[0]:
            return

        role = checkall[1]
        getcc = await getcc_for_mass(message, role)
        if not getcc[0]:
            await message.reply_text(getcc[1])
            return

        ccs = getcc[1]
        resp = f"""
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  PayPal Charge 
- 𝐂𝐂 𝐀𝐦𝐨𝐮𝐧𝐭 - {len(ccs)}
- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - Checking CC For {first_name}
- 𝐒𝐭𝐚𝐭𝐮𝐬 - Processing...⌛️
        """
        nov = await message.reply_text(resp)

        text = f"""
<b>↯ MASS PayPal Charge [/mpp]

Number Of CC Check : [{len(ccs)}]
</b>\n"""
        amt = 0
        start = time.perf_counter()

        works = [paypal_mchkfunc(i, user_id) for i in ccs]
        worker_num = int(json.loads(
            open("FILES/config.json", "r", encoding="utf-8").read())["THREADS"])

        while works:
            batch = works[:worker_num]
            results = await asyncio.gather(*batch)
            for result in results:
                amt += 1
                text += result
                if amt % 5 == 0:
                    try:
                        await Client.edit_message_text(message.chat.id, nov.id, text)
                    except:
                        pass
            await asyncio.sleep(1)
            works = works[worker_num:]

        taken = str(timedelta(seconds=time.perf_counter() - start))
        hours, minutes, seconds = map(float, taken.split(":"))
        text += f"""
╚━━━━━━━━━━━━
[ϟ] T/t : {time.perf_counter() - start:0.2f}s
[ϟ] 𝗖𝗵𝗲𝗸𝗲𝗱 𝗯𝘆: <a href='tg://user?id={message.from_user.id}'> {message.from_user.first_name}</a> [ {role} ]
[ϟ] 𝗢𝘄𝗻𝗲𝗿: <a href="tg://user?id=6622603977">𝑵𝒂𝒊𝒓𝒐𝒃𝒊𝒂𝒏𝒈𝒐𝒐𝒏</a>
╚━━━━━━「𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐇𝐄𝐂𝐊𝐄𝐑」━━━━━━╝
'''''

        await Client.edit_message_text(message.chat.id, nov.id, text)
        await massdeductcredit(user_id, len(ccs))
        await setantispamtime(user_id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        
