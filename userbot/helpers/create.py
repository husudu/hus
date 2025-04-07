import asyncio, sys, os
from random import randint
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from userbot import BOT_TOKEN, HEROKU_APIKEY, HEROKU_APPNAME, bot, me as b

async def autopilot():
    desc = "⚡ Brend Userbot Botlog."
    try:
        qrup = await bot(CreateChannelRequest(title="⚡ Brend Botlog", about=desc, megagroup=True))
        qrup_id = qrup.chats[0].id
    except Exception as e:
        LOGS.error(str(e))
    if not str(qrup_id).startswith("-100"):
        qrup_id = int(f"-100{str(qrup_id)}")
        bura = os.path.abspath(__file__)
        husu = os.path.abspath(os.path.join(bura, "..", "..", "..", "husu.env"))
        b = BOTLOG_CHATID = int(qrup_id)
        with open(husu, "a", encoding="utf-8") as f:
            f.write(b)
        #Oğrama ay peysər oğramaa

async def brendautobot():
    if BOT_TOKEN:
        return
    await bot.start()
    await asyncio.sleep(15)
    await bot.send_message(b, "**@BotFather-də sizin üçün Telegram Assistant bot alınır**")
    brend = await bot.get_me()
    adi = f"{brend.first_name}"
    if brend.username:
        username = f"{brend.username}_{randint(1, 1000)}_bot"
    else:
        username = f"brend{(str(brend.id))[5:]}bot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        await bot.send_message(b, "@BotFather dən bot yaradıb tokenini herokuda BOT_TOKEN-ə əlavə edin")
        sys.exit(1)
    await bot.send_message(bf, f"{adi} Assistant")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            await bot.send_message("Lütfən, @BotFather-dən Bot yaradın və onun işarəsini BOT_TOKEN-ə əlavə edin")
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"brend{(str(brend.id))[6:]}{str(ran)}bot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"☕️ {adi} üçün yaradılmışam")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"✨ Sahib ~ {adi} ✨\n\n⚡ Powered By ~ @BrendUserbot ⚡")
            await bot.send_message(b, f"**İstifadəçi Adı @{username} olan telegram botu uğurla tamamlandı**",)
            bura = os.path.abspath(__file__)
            husu = os.path.abspath(os.path.join(bura, "..", "..", "..", "husu.env"))
            u = BOT_USERNAME = str(username)
            t = BOT_TOKEN = str(token)
            with open(husu, "a", encoding="utf-8") as f:
                f.write(u)
                f.write(t)
            #Oğrama ay peysər oğramaa
        else:
            await bot.send_message("Lütfən, @Botfather ünvanında Telegram Botlarınızdan bəzilərini silin və ya bot nişanları ilə Var BOT_TOKEN təyin edin")
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"☕️ {adi} üçün yaradılmışam")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"👑 Sahib ~ {adi} 👑\n\n⚡ Powered By ~ @BrendUserbot ⚡")
        bura = os.path.abspath(__file__)
        husu = os.path.abspath(os.path.join(bura, "..", "..", "..", "husu.env"))
        u = BOT_USERNAME = str(username)
        t = BOT_TOKEN = str(token)
        with open(husu, "a", encoding="utf-8") as f:
            f.write(u)
            f.write(t)
        #Oğrama ay peysər oğramaa
    else:
        await bot.send_message(b, "Lütfən, @Botfather ünvanında Telegram Botlarınızdan bəzilərini silin və ya bot nişanları ilə Var BOT_TOKEN təyin edin")
        sys.exit(1)
    
