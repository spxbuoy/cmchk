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


async def get_proxy_format():
    return await asyncio.to_thread(_get_proxy_format)


def _get_proxy_format():
    import random
    getproxy = random.choice(open("FILES/proxy.txt", "r", encoding="utf-8").read().splitlines())
    proxy_ip, proxy_port, proxy_user, proxy_password = getproxy.split(":")
    proxies = {
        "https://": f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}",
        "http://": f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}",
    }
    return proxies


async def check_proxy_status(proxies):
    # Placeholder: replace with real check if needed
    return True


@Client.on_message(filters.command("so", [".", "/"]))
async def so_auth_cmd(client: Client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(client, message)

        gateway = "Shopify [9.53$]"
        cmd = "/so"

        if not checkall[0]:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if not getcc:
            resp = f"""<b>
Gate Name: {gateway} ♻️
CMD: {cmd}

Message: No CC Found in your input ❌

Usage: {cmd} cc|month|year|cvv</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""
↯ Custom Shopify.

- [そ] 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""
↯ Custom Shopify..

- [そ] 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■□□
"""
        await asyncio.sleep(0.5)
        secondchk = await client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        proxies = await get_proxy_format()
        session = httpx.AsyncClient(timeout=30, proxies=proxies, follow_redirects=True)
        result = await create_shopify_charge(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)
        status = getresp["status"]
        response = getresp["response"]

        thirdresp = f"""
↯ Custom Shopify...

- [そ] 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- [ヸ] 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- [仝] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■■
"""
        await asyncio.sleep(0.5)
        thirdcheck = await client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        brand = getbin[0]
        card_type = getbin[1]
        level = getbin[2]
        bank = getbin[3]
        country = getbin[4]
        flag = getbin[5]
        currency = getbin[6]

        proxy_status = "𝑷𝒓𝒐𝒙𝒚 𝑳𝒊𝒗𝒆✅" if await check_proxy_status(proxies) else "𝑷𝒓𝒐𝒙𝒚 𝑫𝒆𝒂𝒅❌"

        finalresp = f"""
{status}
{status}
━━━━━━━━━━━━━━━
[ﾒ] Card ➺ <code>{fullcc}</code>
[ﾒ] Gateway ➺ <i>{gateway}</i>
[ﾒ] Response ➺ ⤿ {response} ⤾
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
[ﾒ] Bin ➺ {bin_code}
[ﾒ] Info ➺ {brand} - {card_type} - {level}
[ﾒ] Bank ➺ {bank}
[ﾒ] Country ➺ {country} - {flag} - {currency}
[ﾒ] VBV ➺ {vbv_status}
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
[ﾒ] Checked By ➺ <a href='tg://user?id={message.from_user.id}'> {message.from_user.first_name}</a> [ {role} ]
[ﾒ] Dev ➺ ⏤‌‌‌‌ <a href="tg://user?id=7941175119">ᶻⒺ𝓡𝐎</a>
━━━━━━━━━━━━━━━
[ﾒ] T/t ➺ [{time.perf_counter() - start:0.2f} seconds] | P/x ➺ [{proxy_status}]
"""
        await asyncio.sleep(0.5)
        await client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)
        if status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅":
            await sendcc(finalresp, session)
        await session.aclose()

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
        
