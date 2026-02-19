from asyncio import sleep
from os import remove
from telethon.errors import BadRequestError, ChatAdminRequiredError, ImageProcessFailedError, PhotoCropSizeSmallError, UserAdminInvalidError
from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest, InviteToChannelRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, AddChatUserRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, InputPeerChat)
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot, WARN_MODE, WARN_LIMIT, WHITELIST, ALIVE_NAME
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from userbot.cmdhelp import CmdHelp
import datetime, telethon

from userbot.language import get_value
LANG = get_value("admin")

PP_TOO_SMOL = LANG['PP_TOO_SMOL']
PP_ERROR = LANG['PP_ERROR']
NO_ADMIN = LANG['NO_ADMIN']
NO_PERM = LANG['NO_PERM']
NO_SQL = LANG['NO_SQL']

CHAT_PP_CHANGED = LANG['CHAT_PP_CHANGED']
CHAT_PP_ERROR = LANG['CHAT_PP_ERROR']
INVALID_MEDIA = LANG['INVALID_MEDIA']

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


async def elcjn(brend):
    args = brend.pattern_match.group(1).split(':', 1)
    extra = None
    if brend.reply_to_msg_id and not len(args) == 2:
        previous_message = await brend.get_reply_message()
        user_obj = await brend.client.get_entity(previous_message.from_id)
        extra = brend.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await brend.edit(f"`{ALIVE_NAME}`: **İstifadəçi adı,id yazın və ya istifadəçiyə cavab verin!**")
            return
        if brend.message.entities is not None:
            probable_user_mention_entity = brend.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await brend.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await brend.client.get_entity(user)
        except Exception as err:
            return await brend.edit("Uğursuzluq \n **XƏTA❌**\n", str(err))
    return user_obj, extra


async def get_user_from_id(user, brend):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await brend.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await brend.edit(str(err))
        return None
    return user_obj

try:
    from userbot import client2, client3
except BaseException:
    client2 = client3 = None


@register(outgoing=True, pattern=r"^\.gkick(?: |$)(.*)")
async def elcjn(brend):
    lazy = brend
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`Qruplar axtarılır...`")
    else:
        rkp = await lazy.edit("`Prosses başladı...`")
    me = await brend.client.get_me()
    await rkp.edit(f"**İstifadəçi qruplardan atılır..**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await brend.get_chat()
    a = b = 0
    if brend.is_private:
        user = brend.chat
        reason = brend.pattern_match.group(1)
    else:
        brend.chat.title
    try:
        user, reason = await get_user_from_brend(brend)
    except BaseException:
        pass
    try:
        if not reason:
            reason = 'Private'
    except BaseException:
        return await rkp.edit("**XƏTA❌! Naməlum istifadəçi.**")
    if user:
        if user.id == WHITELIST:
            return await rkp.edit(LANG['BRAIN'])
        try:
            await brend.client(BlockRequest(user))
            await brend.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [d.entity.id for d in await brend.client.get_dialogs() if (d.is_group or d.is_channel)]
        for i in testrk:
            try:
                await brend.client.edit_permissions(i, user, view_messages=False)
                await brend.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await rkp.edit(f"**İstifadəçi qruplardan atılır!\nÇıxarıldı {a} qrupdan.....**")

            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**İstifadəçiyə cavab ver!**")

    return await rkp.edit(f"**İstifadəçi : [{user.first_name}](tg://user?id={user.id}) {a} qrupdan çıxarıldı**")

@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gbanspider(gspdr):

    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    await gspdr.edit(LANG['BANNING'])
    if gban(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GBANNED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GBANNED_REASON']} {reason}")
        else:
            await gspdr.edit(LANG['GBANNED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(incoming=True)
async def gbanmsg(moot):
                            
    try:
        from userbot.modules.sql_helper.gban_sql import is_gbanned
    except:
        return

    gbanned = is_gbanned(str(moot.sender_id))
    if gbanned == str(moot.sender_id):
        try:
            chat = await moot.get_chat()
        except:
            return
            
        if (type(chat) == User):
            return 

        admin = chat.admin_rights
        creator = chat.creator

        if not admin and not creator:
            return

        try:
            await moot.client(EditBannedRequest(moot.chat_id, moot.sender_id,
                                            BANNED_RIGHTS))
            await moot.reply(LANG['GBAN_TEXT'])
        except:
            return

@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(un_gban):

    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gban.edit(LANG['UNGBANNING'])

    if ungban(user.id) is False:
        await un_gban.edit(LANG['NO_BANNED'])
    else:

        await un_gban.edit(LANG['UNGBANNED'])

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID, "#UNGBAN\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gban.chat.title}(`{un_gban.chat_id}`)")


@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
                             
    if not gpic.is_group:
        await gpic.edit(LANG['PRIVATE'])
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)

@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
                             
    chat = await promt.get_chat()

    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(invite_users=True,
                                 change_info=True,
                                 delete_messages=True,
                                 pin_messages=True,)
    try:
        await promt.edit(LANG['PROMOTING'])
    except:
        await promt.reply(LANG['PROMOTING'])
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "İdarəçi"
    if user:
        pass
    else:
        return
                             
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit(LANG['SUCCESS_PROMOTE'])

    except:
        await promt.edit(NO_PERM)
        return

    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#NORMAL_İDARƏÇİ_ETMƏK\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {promt.chat.title}(`{promt.chat_id}`)")

@register(outgoing=True, pattern="^.propromote(?: |$)(.*)")
async def promote(ppromt):
    chat = await ppromt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await ppromt.edit(NO_ADMIN)
        return
    new_rights = ChatAdminRights(add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True,
                                 manage_call=True)
    try:
        await ppromt.edit(LANG['PROMOTING'])
    except:
        await ppromt.reply(LANG['PROMOTING'])
    user, rank = await get_user_from_event(ppromt)
    if not rank:
        rank = "PRO İdarəçi"
    if user:
        pass
    else:
        return                   
    try:
        await ppromt.client(EditAdminRequest(ppromt.chat_id, user.id, new_rights, rank))
        await ppromt.edit(LANG['SUCCESS_PROPROMOTE'])
    except:
        await ppromt.edit(NO_PERM)
        return
    if BOTLOG:
        await ppromt.client.send_message(
            BOTLOG_CHATID, "#PRO_İDARƏÇİ_ETMƏK\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\nQRUP: {ppromt.chat.title}(`{ppromt.chat_id}`)")

@register(outgoing=True, pattern="^.spromote(?: |$)(.*)")
async def spampromote(spromt):
    chat = await spromt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await spromt.edit(NO_ADMIN)
        return
    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=False,
                                 change_info=False,
                                 ban_users=False,
                                 delete_messages=False,
                                 pin_messages=False,
                                 manage_call=False)
    try:
        await spromt.edit(LANG['PROMOTING'])
    except:
        await spromt.reply(LANG['PROMOTING'])
    user, rank = await get_user_from_event(spromt)
    if not rank:
        rank = "Spam icazəsi"
    if user:
        pass
    else:
        return                   
    try:
        await spromt.client(EditAdminRequest(ppromt.chat_id, user.id, new_rights, rank))
        await spromt.edit(LANG['SUCCESS_SPAMPROMOTE'])
    except:
        await spromt.edit(NO_PERM)
        return
    if BOTLOG:
        await spromt.client.send_message(
            BOTLOG_CHATID, "#SPAM_İCAZƏSİ_VERMƏK\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\nQRUP: {ppromt.chat.title}(`{ppromt.chat_id}`)")

@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return
    try:
        await dmod.edit(LANG['UNPROMOTING'])
    except:
        await dmod.reply(LANG['UNPROMOTING'])
    rank = "brend"
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
                             
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit(LANG['UNPROMOTE'])
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ADMİNLİK-ALINMASI\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {dmod.chat.title}(`{dmod.chat_id}`)")

@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
async def ban(bon):

    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await bon.edit(
            LANG['BRAIN']
        )
        return

    await bon.edit(LANG['BANNING'])

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except:
        await bon.edit(NO_PERM)
        return
                             
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except:
        await bon.edit(
            LANG['NO_PERM_BUT_BANNED'])
        return
                             
    SONMESAJ = PLUGIN_MESAJLAR['ban'].format(
        id = user.id,
        username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
        first_name = user.first_name,
        last_name = '' if not user.last_name else user.last_name,
        mention = f"[{user.first_name}](tg://user?id={user.id})",
        date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
        count = (chat.participants_count - 1) if chat.participants_count else 'Bilinmiyor'
    )
    
    if reason:
        await bon.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await bon.edit(SONMESAJ)
                       
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):

    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    await unbon.edit(LANG['UNBANNING'])

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit(LANG['UNBANNED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmir'
        ))

        if BOTLOG:
            await unban.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except:
        await unbon.edit(LANG['EXCUSE_ME_WTF'])


@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
                       
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except:
        await spdr.edit(NO_SQL)
        return

    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await spdr.edit(
            LANG['BRAIN']
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            LANG['NO_MUTE_ME'])
        return

    await spdr.edit(LANG['MUTING'])
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit(LANG['ALREADY_MUTED'])
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason, chat)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason, chat)
        except:
            return await spdr.edit(LANG['WTF_MUTE'])

async def mutmsg(spdr, user, reason, chat):
    SONMESAJ = PLUGIN_MESAJLAR['mute'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        )

    if reason:
        await spdr.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await spdr.edit(f"{SONMESAJ}")

    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):

    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit(LANG['UNMUTING'])
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit(LANG['ALREADY_UNMUTED'])
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmir'
        ))
        except UserAdminInvalidError:
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmir'
        ))
        except:
            await unmot.edit(LANG['WTF_MUTE'])
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"İSTİFADƏCİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
                        
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights))
                except:
                    pass
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                await moot.delete()

@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):

    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gmute.edit(LANG['GUNMUTING'])

    if ungmute(user.id) is False:
        await un_gmute.edit(LANG['NO_GMUTE'])
    else:

        await un_gmute.edit(LANG['UNMUTED'])

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):

    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    await gspdr.edit(LANG['GMUTING'])
    if gmute(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GMUTED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GMUTED']} {LANG['REASON']}: {reason}")
        else:
            await gspdr.edit(LANG['GMUTED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {gspdr.chat.title}(`{gspdr.chat_id}`)")

@register(outgoing=True, pattern="^.check(?: |$)(.*)", groups_only=False)
@register(outgoing=True, pattern="^.qrupuyoxla(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = LANG['NO_ZOMBIE']

    if con != "sil":
        await show.edit(LANG['ZOMBIE'])
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = LANG['ZOMBIES'].format(del_u)
        await show.edit(del_status)
        return

    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await show.edit(LANG['NO_ADMIN'])
        return

    await show.edit(LANG['CLEANING'])
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            except:
                await show.edit(LANG['NO_BAN_YT'])
                return
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"**{del_u}** {LANG['DELETED']}"

    if del_a > 0:
        del_status = f"**{del_u}** {LANG['DELETED']} \
        \n**{del_a}** ədəd silinən admin hesabını çıxara bilmədim"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#TEMIZLIK\n"
            f"**{del_u}** ədəd silinmiş hesab çıxardıldı !!\
            \nQRUP: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^.admin$")
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>{title} {LANG["ADMINS"]}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinən Hesab <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
async def pin(msg):

    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit(LANG['NEED_MSG'])
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except:
        await msg.edit(NO_PERM)
        return

    await msg.edit(LANG['PINNED'])

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#SABITLƏMƏ\n"
            f"ADMİN: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"SƏSLİ: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
                             
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit(LANG['NOT_FOUND'])
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await usr.edit(
            LANG['BRAIN']
        )
        return

    await usr.edit(LANG['KICKING'])

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`\n{LANG['REASON']}: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {usr.chat.title}(`{usr.chat_id}`)\n")




async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`İstifadəçinin istifadəçi adını, İD və ya mesajını verin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj

@register(outgoing=True, pattern="^.unwarn ?(.*)")
async def unwarn(event):
          
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    await event.edit(LANG['UNWARNING'])
    silme = warn.sil_warn(user.id)
    if silme == False:
        await event.edit(LANG['UNWARNED'])
        return

    warnsayi = warn.getir_warn(user.id)
    
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {LANG['UNWARN']} {warnsayi}/{WARN_LIMIT}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"İstifadəçi: [{user.first_name}](tg://user?id={user.id})\n"
            f"Qrup: {event.chat.title}(`{event.chat_id}`)")

@register(outgoing=True, pattern="^.warn ?(.*)")
async def warn(event):
                     
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return
                     
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await event.edit(LANG['BRAIN'])
        return
                     
    await event.edit(LANG['WARNING'])
    warn.elave_warn(user.id)
    warnsayi = warn.getir_warn(user.id)
    if warnsayi >= WARN_LIMIT:
        if WARN_MODE == "gban":
            await Warn_Gban(event, warn, user)
        else:
            await Warn_Gmute(event, warn, user)
        return
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {warnsayi}/{WARN_LIMIT} {LANG['WARN']}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {event.chat.title}(`{event.chat_id}`)")

async def Warn_Gmute(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Sənə bəs qədər xəbərdarlıq etdim!` [{user.first_name}](tg://user?id={user.id})`, indi isə qlobal olaraq səssizə alındın!`")

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Səssizə alınır...`")
        
    if gmute(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuzda dünya səviyyəsində səssizdir.`')
    else:
        if reason != None:
            await yeni2.edit(f"🤐İstifadəçi qlobal olaraq səssizləşdirildi!\n📝Səbəbi: {reason}")
        else:
            await yeni2.edit("🙃İstifadəçi qlobal olaraq səssizdir!")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

async def Warn_Gban(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"😡Sənə bəs qədər xəbərdarlıq etdim [{user.first_name}](tg://user?id={user.id}), indi isə qlobal olaraq qadağan olundun!`")

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("⚠️Qadağan olunur...")
        
    if gban(user.id) == False:
        await yeni2.edit(
            '❌Xəta! İstifadəçi onsuzda qlobal olaraq qadağan edilmişdir.')
    else:
        if reason != None:
            await yeni2.edit(f"👤İstifadəçi artıq qlobal olaraq qadağan edilmişdir!\n📝Səbəbi: `{reason}`")
        else:
            await yeni2.edit("👤İstifadəçi artıq qlobal olaraq qadağan edilmişdir!")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"İSTİFADƏÇİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

@register(outgoing=True, pattern="^.bots$", groups_only=True)
async def get_bots(show):
                     
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} qrupunda tapılan botlar:</b>\n'
    try:

        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmiş bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Uyda! Burada çox bot var. Botların siyahısını bir fayl olaraq göndərirəm.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} qrupunda tapılan botlar:'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")

CmdHelp('admin').add_command(
        'promote', '<istifadəçi adı/cavəblama> <xüsusi ad (istəyə bağlı)>', 'Seçdiyiniz istifadəçiyə qrupu idarə icazəsi verir.'
    ).add_command(
        'propromote', '<istifadəçi adı/cavəblama> <xüsusi ad (istəyə bağlı)>', 'Seçdiyiniz istifadəçiyə qrupu idarə üçün pro icazə verir.'
    ).add_command(
        'demote', '<istifadəçi adı/cavablama>', 'Seçdiyiniz userin idarəçilik icazəsini alar.'
    ).add_command(
        'ban', '<istifadəçi adı/cavablama> <səbəb (istəyə bağlı)>', 'Seçdiyiniz istifadəçinin mesaj yazmasını dayandırar, idarəçilərdədə də işləyir.'
    ).add_command(
        'unban', '<istifadəçi adı/cavablama>', 'Verilən qadağanı(ban) qaldırır.'
    ).add_command(
        'kick', '<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>', 'Qrupdan göstərdiyiniz istifadəçini çıxardar.'
    ).add_command(
        'gmute', '<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>', 'İstifadəçi idarə etdiyiniz bütün qruplarda səssizə alınır.'
    ).add_command(
        'ungmute', '<istifadəçi adı/cavablama>', 'İstifadəçini qlobal olaraq səssizə alınanlar siyahısından silər.'
    ).add_command(
        'check', None, 'Bir qrupdakı silinmiş hesabları axtarır. Qrupdakı silinən hesabları çıxarmaq üçün `.ckeck sil` əmrini istifadə edin.'
    ).add_command(
        'admin', None, 'Söhbət idarəçilərinin siyahısını alır.'
    ).add_command(
        'bots', None, 'Qrupda olan botları göstərir.'
    ).add_command(
        'warn', '<istifadəçi adı/cavablama> <səbəb (istəkdən aslı>', 'Göstərdiyiniz istifadəçiyə xəbərdarlıq edər.'
    ).add_command(
        'unwarn', '<istifadəçi adı/cavablama> <sebep (isteğe bağlı>', 'Göstərdiyiniz istifadəçinin xəbərdarlığını silər.'
    ).add_command(
        'warn', '<istifadəçi adı/cavablama> <səbəb (istəyə bağlı>', 'Göstərdiyiniz istifadəçiyə xəbərdarlıq edər.'
    ).add_command(
        'gban', '<istifadəçi adı/cavablama>', 'İstifadəçini qlobal olaraq qadağan edin.'
    ).add_command(
        'ungban', '<istifadəçi adı/cavablama>', 'İstifadəçinin qlobal qadağasını qaldırır.'
    ).add_command(
        'gkick', '<id,isifadəçi adı,yanıt>', 'İstifadəçini bütün ortaq qruplarınızdan çıxarar..'
    ).add_command(
        'pin', '<cavablama>', 'Cavab verdiyiniz mesajı sabitləyər.'
    ).add_command(
        'setgpic', '<cavablama>', 'Qrup fotosunu dəyişdirir.'
    ).add()




