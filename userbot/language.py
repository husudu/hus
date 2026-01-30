# © Copyright Brend Userbot 
# t.me/BrendOwner tərəfindən xəta düzəldilmişdir
# Safety + stability fix by audit

from . import LANGUAGE, LOGS, bot, PLUGIN_ID
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_ID)
LANGUAGE_JSON = None


def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return loads(f.read())
    except JSONDecodeError:
        raise
    except Exception as e:
        LOGS.error(f"Language file read error: {e}")
        return None


for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):

    if ((len(dil.file.name.split(".")) >= 2) and (dil.file.name.split(".")[1] == "brendjson")):

        local_path = f"./userbot/language/{dil.file.name}"

        # Local varsa
        if path.isfile(local_path):
            try:
                LANGUAGE_JSON = load_json_file(local_path)

            except JSONDecodeError:
                dil.delete()
                remove(local_path)

                if path.isfile("./userbot/language/DEFAULT.brendjson"):
                    LOGS.warning("Defolt dil faylı istifadə olunur...")
                    LANGUAGE_JSON = load_json_file("./userbot/language/DEFAULT.brendjson")
                else:
                    raise Exception("Your language file is invalid")

        # Local yoxdursa telegramdan yüklə
        else:
            try:
                DOSYA = dil.download_media(file="./userbot/language/")
                LANGUAGE_JSON = load_json_file(DOSYA)

            except JSONDecodeError:
                dil.delete()

                if path.isfile("./userbot/language/DEFAULT.brendjson"):
                    LOGS.warning("Defolt dil faylı istifadə olunur...")
                    LANGUAGE_JSON = load_json_file("./userbot/language/DEFAULT.brendjson")
                else:
                    raise Exception("Your language file is invalid")

        break


# Heç biri tapılmadısa
if LANGUAGE_JSON is None:

    lang_file = f"./userbot/language/{LANGUAGE}.brendjson"

    if path.isfile(lang_file):
        try:
            LANGUAGE_JSON = load_json_file(lang_file)
        except JSONDecodeError:
            raise Exception("Invalid json file")

    else:
        if path.isfile("./userbot/language/DEFAULT.brendjson"):
            LOGS.warning("Default dil faylı istifadə olunur...")
            LANGUAGE_JSON = load_json_file("./userbot/language/DEFAULT.brendjson")
        else:
            raise Exception(f"Didn't find {LANGUAGE} file")


def get_value(plugin=None, value=None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON is None:
        raise Exception("Please load language file first")

    if plugin is None or value is None:
        raise Exception("Invalid plugin or string")

    Plugin = LANGUAGE_JSON.get("STRINGS", {}).get(plugin)

    if Plugin is None:
        raise Exception("Invalid plugin")

    String = Plugin.get(value)

    if String is None:
        return Plugin
    else:
        return String
