import unicodedata
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
import re
from pyrogram import Client, filters

app = Client(
    "zoney",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def get_admins(chat_id: int):
    return [
        member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

def load_blacklist():
    with open("blacklist.txt", "r") as file:
        return [normalize_text(line.strip()) for line in file]

def contains_blacklisted_word(text, blacklist):
    return any(word.lower() in text.lower() for word in blacklist)

def normalize_text(text):
    return unicodedata.normalize('NFKD', text)

def has_special_font(text):
    special_font_regex = re.compile(r'[\u0000-\u001F\u007F-\u009F\u00AD\u0600-\u0605\u061C\u06DD\u070F\u17B4\u17B5\u200B-\u200D\u2028-\u202F\u2060-\u206F\uFEFF\uFFF9-\uFFFB]')
    return bool(special_font_regex.search(text))

blacklist = load_blacklist()
delete_mode = True

@app.on_message(filters.group)
async def delete_blacklisted_messages(client, message):
    try:
        if message.text:
            regular_font_text = normalize_text(message.text)
            if contains_blacklisted_word(regular_font_text, blacklist) and delete_mode:
                await message.delete()
    except Exception as e:
        print(f"Error processing message: {e}")
print("fuck you")
app.run()
