# Kopyalama Peysərin Balası
# Tam olaraq sıfırdan yığılması Brend Userbot-a məxsusdur!

from telethon.tl import functions, types
from userbot.events import register
from userbot.cmdhelp import CmdHelp



@register(outgoing=True, pattern="^.yarat (g|c)(?: |$)(.*)")
@register(outgoing=True, pattern="^.create (g|c)(?: |$)(.*)")
async def creategc(event):
    if event.fwd_from:
        return

    tip = event.pattern_match.group(1)
    ad = event.pattern_match.group(2)

    if not ad:
        return await event.edit("❌ Ad daxil etməlisən.")

    if tip == "g":
        try:
            bot = await event.client.get_entity("@BrendRobot")
            result = await event.client(functions.messages.CreateChatRequest(users=[bot], title=ad))
            chat_id = None
            for update in result.updates:
                if isinstance(update, types.UpdateNewMessage):
                    chat_id = update.message.peer_id.chat_id
            if not chat_id:
                return await event.edit("❌ Qrup ID tapılmadı.")
            invite = await event.client(functions.messages.ExportChatInviteRequest(peer=chat_id))
            await event.edit(f"[⚡ ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ](https://t.me/brenduserbot) vasitəsilə **{ad}** qrupu yaradıldı.\n\n", f"🔘 [{ad}]({invite.link}) qrupuna qoşul.")
        except Exception as e:
            await event.edit(f"❌ Xəta:\n`{e}`")
    elif tip == "c":
        try:
            result = await event.client(
                functions.channels.CreateChannelRequest(title=ad, about="⚡ Brend Userbot tərəfindən yaradıldı"))
            channel = result.chats[0]
            invite = await event.client(functions.messages.ExportChatInviteRequest(peer=channel))
            await event.edit(f"[⚡ ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ](https://t.me/brenduserbot) vasitəsilə **{ad}** kanalı yaradıldı.\n\n", f"🔘 [{ad}]({invite.link}) kanalına keç.")
        except Exception as e:
            await event.edit(f"❌ Xəta:\n`{e}`")

CmdHelp('create').add_command('create', '<g/c> <ad>', 'Cəmi bir əmrlə qrup və ya kanal yaradın qrup yaratmaq üçün .yarat q <ad> , kanal yaratmaq üçün .yarat k <ad> yazın.').add()
