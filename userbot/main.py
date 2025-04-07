import userbot.cmdhelp, importlib, os, requests, re, asyncio
from importlib import import_module
from sqlite3 import connect
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_ID, BREND_VERSION, BOT_TOKEN, BOTLOG_CHATID
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
from userbot.helpers import brendautobot, autopilot
from random import choice

AFKSTR = [
    "`Mən indi tələsirəm, daha sonra bir mesaj göndərə bilməzsən?😬\nOnsuz da yenə gələcəm.`",
    "`Yazdığınız şəxs hal-hazırda mesajınıza cavab vermir.\nXaiş edirik biraz sonra mesaj yazın!`",
    "`Bir neçə dəqiqədən sonra gələcəm. Ancaq gəlməsəm ...\ndaha çox gözləyin.`",
    "`Mən indi burada deyiləm, yəqin ki, başqa bir yerdəyəm`.\n",
    "`Getsən gedirsənsə sevgili yar amma unutma.\nBirazdan gələcəm`",
    "`Bəzən həyatda ən yaxşı şeylər gözləməyə dəyər…\nSəndə mənim gəlməyimi gözlə.`",
    "`Dərsə gedən bir uşaq yıxıldı buz üstə. Sonrada durub yoluna davam elədi.\nSahibim burda deyil amma istəsən mən səninlə söhbət edə bilərəm.`",
    "`Sahibim burda yoxdu mənə dediki sevgilisinnən bezib və yeni bir sevgili tapmağa gedir`",
    "`Xahiş edirəm bir mesaj yazın və o mesaj məni indi olduğumdan daha dəyərli hiss etdirsin.`",
    "`Burda olsaydım,\nSizə harada olduğumu deyərdim.\n\nAmma mən deyiləm,\nqayıdanda məndən soruş...`",
    "`Həyat çox qısadır, edilə bilinəcək çox şey var...\nOnlardan birini edirəm...`",
    "`Sahibim hazırda burda deyil mən isə onun mükəmməl olan @BrendUserbot -uyam\nMəncə sahibimdən sənə də belə bir bot qurmasını istməlisən`",
]

UNAPPROVED_MSG = ("🗣️ Hey {mention}, Mən @BrendUserBot -am.\n\n"
                  "✍🏻 Sizin Sahibimə yazmaq icazəniz yoxdur\n"
                  "✅ Sahibimin sizə icazə verməsini gözləyin\n"
                  "🙃 Yazmağa davam etsəniz əngəllənəcəksiniz\n"
                  "✨ Gözlədiyiniz üçün təşəkkürlər\n"
                  "⚡ İmza: @BrendUserbot")

DB = connect("brend.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXƏTA: Daxil edilən telefon nömrəsi yanlışdır' \
             '\n Kömək: Nömrəni ölkə kodu ilə daxil edin.' \
             '\n    Telefon nömrənizi təkrar yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("brend.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read() 
    if '/' in file:
        file = file.split('/')[-1]
    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Əmrler = []
    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        fayladi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(fayladi, False)
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Əmr = re.findall("(^.*[a-zA-Z0-9şğüöçıə]\w)", Command)
            if (len(Əmr) >= 1) and (not Əmr[0] == ''):
                Əmr = Əmr[0]
                if Əmr[0] == '^':
                    ƏmrStr = Əmr[1:]
                    if ƏmrStr[0] == '.':
                        ƏmrStr = ƏmrStr[1:]
                    Əmrler.append(ƏmrStr)
                else:
                    if Command[0] == '^':
                        ƏmrStr = Command[1:]
                        if ƏmrStr[0] == '.':
                            ƏmrStr = ƏmrStr[1:]
                        else:
                            ƏmrStr = Command
                        Əmrler.append(ƏmrStr)
            #Brend
            Brendpy = re.search('\"\"\"BRENDPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Brendpy == None:
                Brendpy = Brendpy.group(0)
                for Satir in Brendpy.splitlines():
                    if (not '""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Ad = Satir[0]
                        Deyer = Satir[1][1:]
                                
                        if Ad == 'INFO':
                            CmdHelp.add_info(Deyer)
                        elif Ad == 'WARN':
                            CmdHelp.add_warning(Deyer)
                        else:
                            CmdHelp.set_file_info(Ad, Deyer)
            for Əmr in Əmrler:
                CmdHelp.add_command(Əmr, None, 'Bu plugin Brend Userbot məhsulu deyil. Hərhansısa bir açıqlama tapılmadı.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    brendbl = requests.get('https://gitlab.com/husudu/userbot/-/raw/master/brendblacklist.json').json()
    if idim in brendbl:
        bot.disconnect()

    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`⚡️ 𝙱​𝚛彡𝚗𝚍​ UserBot online...`", "alives": f"https://telegra.ph/file/d61b9172fc143fdfc86a2.gif", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Özünüzdən muğayat olun mən gedirəm🤠`", "pm": UNAPPROVED_MSG, "dızcı": "Stiket Brend Paketinə əlavə olunur", "ban": "**{mention}** `qadağan edildi!`", "mute": "**{mention}** `səssizə alındı`", "approve": "**{mention}** `mənə mesaj göndərə bilərsən!`", "tagsleep": "3", "disapprove": "{mention} **Bundan sonra mənə mesaj göndərə bilməzsən!**", "block": "**{mention}** `əngəlləndin!`"}

    PLUGIN_MESAJLAR_NOVLER = ["alive", "alives", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "tagsleep", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_NOVLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_ID, ids=medya)
                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
                
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(f"Brend Userbot online! Support => @BrendSUP | Brend Version: {BREND_VERSION}")
"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
loop = asyncio.get_event_loop()
 if not BOTLOG_CHATID:
     loop.run_until_complete(autopilot())
 if not BOT_TOKEN:
     loop.run_until_complete(brendautobot())
bot.run_until_disconnected()
