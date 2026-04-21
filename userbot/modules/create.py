# Kopyalama Peysərin Balası
# Tam olaraq sıfırdan yığılması Brend Userbot-a məxsusdur!

from telethon.tl import functions
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.yarat (g|c)(?: |$)(.*)")
@register(outgoing=True, pattern="^.create (g|c)(?: |$)(.*)")
async def creategc(yarat):
    if yarat.fwd_from:
        return
    tip = yarat.pattern_match.group(1)
    ad = yarat.pattern_match.group(2)
    if tip == "g":
        try:
            result = await yarat.client(functions.messages.CreateChatRequest(users=["@BrendRobot"], title=ad))
            qrup_id = result.chat.id
            await yarat.client(functions.messages.DeleteChatUserRequest(chat_id=qrup_id, user_id="@BrendRobot"))
            invite = await yarat.client(functions.messages.ExportChatInviteRequest(peer=qrup_id))
            link = invite.link
            await yarat.edit(f"[⚡ ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ](https://t.me/brenduserbot) {ad} qrupunu yaratdı.\n\n🔘 [{ad}]({link}) qrupuna qoşul.")
        except Exception as e:
             await yarat.edit(f"❌ Xəta baş verdi: {e}")
    elif tip == "c":
        try:
            link = await yarat.client(functions.channels.CreateChannelRequest(title=ad, about="⚡ Brend Userbot tərəfindən yaradıldı"))
            kanal_id = link.chats[0].id
            link = await yarat.client(functions.messages.ExportChatInviteRequest(peer=kanal_id))
            await yarat.edit(f"[⚡ ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ](https://t.me/brenduserbot) {ad} kanalını yaratdı.\n\n🔘 [{ad}]({link.link}) kanalına keçid et.")
        except Exception as e:
            await yarat.edit(f"❌ Xəta baş verdi: {e}")
    else:
        await yarat.edit("Bu modulu işlətmə qaydasını bilmək üçün `.brend create` yazın")

CmdHelp('create').add_command('yarat', '<g/c> <ad>', 'Cəmi bir əmrlə qrup və ya kanal yaradın qrup yaratmaq üçün .yarat g <ad> , kanal yaratmaq üçün .yarat c <ad> yazın.').add()
