import sys, io, os, asyncio, pybase64
from os import execl
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
from subprocess import PIPE, run as runapp
from getpass import getuser
from os import remove
LANG = get_value("misc")


@register(outgoing=True, pattern="^.list ?(gmute|gban)?")
async def liste(event):
    liste = event.pattern_match.group(1)
    try:
        if len(liste) < 1:
            await event.edit(LANG['WRONG_INPUT'])
            return
    except:
        await event.edit(LANG['WRONG_INPUT'])
        return
    
    if liste == "gban":
        try:
            from userbot.modules.sql_helper.gban_sql import gbanlist
        except:
            await event.edit(LANG['NEED_SQL_MODE'])
            return
        await event.edit(LANG['GBANNED_USERS'])
        mesaj = ""
        for user in gbanlist():
            mesaj += f"**🆔: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG['TOO_MANY_GBANNED'])
            open("gban_list.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG['GBAN_TXT'], file="gban_list.txt")
            os.remove("gban_list.txt")
        else:
            await event.edit(LANG['GBAN_LIST'] % mesaj)
    elif liste == "gmute":
        try:
            from userbot.modules.sql_helper.gmute_sql import gmutelist
        except:
            await event.edit(LANG['NEED_SQL_MODE'])
            return
        await event.edit(LANG['GMUTE_DATA'])
        mesaj = ""
        for user in gmutelist():
            mesaj += f"**🆔: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG['TOO_MANY_GMUTED'])
            open("gmute_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG['GMUTE_TXT'], file="gmute_liste.txt")
            os.remove("gmute_siyahı.txt")
        else:
            await event.edit(LANG['GMUTE_LIST'] % mesaj)

@register(outgoing=True, pattern="^.term(?: |$)(.*)")
async def terminal_runner(term):
    curruser = getuser()
    command = term.pattern_match.group(1)
    try:
        from os import geteuid
        uid = geteuid()
    except ImportError:
        uid = "Bu deyil rəis!"
    if term.is_channel and not term.is_group:
        await term.edit(LANG['FORBIDDEN_IN_CHANNEL'])
        return
    if not command:
        await term.edit(LANG['NEED_CODE'])
        return
    if command in ("userbot.session", "config.env", "env"):
        await term.edit(LANG['WARNING'])
        return
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) \
        + str(stderr.decode().strip())
    if len(result) > 4096:
        output = open("BrendTerminal.txt", "w+")
        output.write(result)
        output.close()
        await term.client.send_file(term.chat_id, "BrendTerminal.txt", reply_to=term.id, caption=LANG['BIG_FILE'])
        remove("Brend-Terminal.txt")
        return
    if uid == 0:
        await term.edit("`" f"{curruser}:~# {command}" f"\n{result}" "`")
    else:
        await term.edit("`" f"{curruser}:~$ {command}" f"\n{result}" "`")
    if BOTLOG:
        await term.client.send_message(BOTLOG_CHATID, "Terminalda " + command + " əmri müvəffəqiyyətlə başa çatdırıldı",)


@register(outgoing=True, pattern="^.base64 (en|de) (.*)")
async def basekodlama(base):
    if base.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(base.pattern_match.group(2), "utf-8")))[2:]
        await base.reply("Encoded: `" + lething[:-1] + "`")
    else:
        lething = str(pybase64.b64decode(bytes(base.pattern_match.group(2), "utf-8"), validate=True))[2:]
        await base.reply("Decoded: `" + lething[:-1] + "`")


@register(outgoing=True, pattern="^.çevir ?(foto|mp3)? ?(.*)")
async def cevir(event):
    islem = event.pattern_match.group(1)
    try:
        if len(islem) < 1:
            await event.edit(LANG['INVALID_COMMAND'])
            return
    except:
        await event.edit(LANG['INVALID_COMMAND'])
        return
    if islem == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            await event.edit(LANG['NEED_VIDEO'])
            return
        await event.edit('`Səsə çevrilir...`')
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(f"ffmpeg -y -i '{video}' -vn -b:a 128k -c:a libmp3lame brend.mp3")
        await gif.communicate()
        await event.edit('`Səs yüklənir...`')       
        try:
            await event.client.send_file(event.chat_id, "brend.mp3", reply_to=rep_msg, caption='@BrendUserBot ilə səsə çevrildi.')
        except:
            os.remove(video)
            return await event.edit('`Səsə çevrilmədi!`')
        await event.delete()
        os.remove("brend.mp3")
        os.remove(video)
    else:
        await event.edit(LANG['INVALID_COMMAND'])
        return


@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    await event.delete()
    await event.client.send_file(event.chat_id, 'https://www.winhistory.de/more/winstart/mp3/winxpshutdown.mp3', caption=LANG['GOODBYE_MFRS'], voice_note=True)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#Shut_Down\nBot Söndü.")
    try:
        await bot.disconnect()
    except:
        pass

@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit(LANG['RESTARTING'])
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART\nBot Yənidən Başlandı.")
    try:
        await bot.disconnect()
    except:
        pass
    execl(sys.executable, sys.executable, *sys.argv)

@register(support=True, pattern="^.brestart$")
async def balive(event):
    if event.is_reply:
        cavab = await event.get_reply_message()
        brend = await event.client.get_entity(cavab.from_id)
        if brend.id == SAHIB:
            if SAHIB not in WHITELIST:
                await event.reply(LANG['RESTARTING'])
                try:
                    await event.client.disconnect()
                except:
                    pass
                execl(sys.executable, sys.executable, *sys.argv)

@register(support=True, pattern="^.srestart$")
async def dalive(event):
    if SAHIB not in WHITELIST:
        await event.edit(LANG['RESTARTING'])
        try:
            await event.client.disconnect()
        except:
            pass
        execl(sys.executable, sys.executable, *sys.argv)
                  


@register(outgoing=True, pattern="^.repo$")
async def repo(repo):
    await repo.edit(LANG['REPO'])

@register(outgoing=True, pattern="^.sahib$|.creator$|.owner$")
async def sahib(e):
    await e.edit(LANG['CREATOR'])


CmdHelp('misc').add_command(
    'shutdown', None, 'Nostaljik bir şekildə botunuzu söndürün.'
).add_command(
    'repo', None, 'Brend UserBotunun GitHub Reposuna yönəldər.'
).add_command(
    'sahib', None, 'Bu gözəl botun sahibinin kim olduğunu deyir.'
).add_command(
    'creator', None, 'Bu gözəl botu kimin yaratdığını öyrənin :-)'
).add_command(
    'restart', None, 'Botu yenidən başladır.'
).add_command(
    'base64', '<en/de>', 'Base 64 Kodlaması açar və ya kodlayar'
).add_command(
    'term', None, 'Terminalda müəyyən skriptləri yerinə yetirmək üçün'
).add_command(
    'çevir foto', '<cavab>', 'Stikeri fotoya çevirir.'
).add_command(
    'çevir mp3', '<cavab>', 'Cavab verdiyiniz videonu mp3 formatına çevirir.'
).add_command(
    'list', '<gmute/gban>', 'Gban və ya da Gmute elədiyiniz adamları göstərər.'
).add()

