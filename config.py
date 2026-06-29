#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration File - Credit Card Generator Bot
Author: @Murphythox
"""

# ========== TELEGRAM CONFIGURATION ==========
BOT_TOKEN = "8876482657:AAFcG8V-4dtHlIFjbBglpf-p9iiiFp5lJqM"
CHAT_ID = "-1004294180796"

# ========== DEVELOPER INFO ==========
DEV_USERNAME = "@Murphythox"
DEV_CHANNEL = "https://t.me/+Au7NgQAPKhVlN2Fh"
DEV_GITHUB = "https://github.com/sadikmahedi88"

# ========== FILE PATHS ==========
PHOTO_PATH = "dev/Murphy.jpg"

# ========== BOT SETTINGS ==========
TOTAL_CARDS = 1000          # Number of cards to generate
REQUEST_LIMIT = 1           # Cards per batch before pausing
PAUSE_DURATION = 3          # Pause duration in seconds
MAX_RETRIES = 2             # Retry attempts on failure

# ========== CARD GENERATION SETTINGS ==========
CARD_PREFIXES = {
    'Visa': ['4'],
    'Mastercard': ['5', '2'],
    'American Express': ['34', '37'],
    'Discover': ['6011', '65'],
    'JCB': ['35'],
    'Diners Club': ['30', '36', '38'],
    'UnionPay': ['62'],
    'Maestro': ['50', '56', '57', '58', '67']
}

# ========== TELEGRAM MESSAGE TEMPLATE ==========
MESSAGE_TEMPLATE = """
<blockquote>💳 Valid Credit Card</blockquote>
━━━━━━━━━━━━━━
<b>⌖ 𝗖𝗖 ⤳</b> <code>{card_details}</code>
⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿! ✅
⌖ 𝗕𝗶𝗻 ⤳ {bin}
━━━━━━━━━━━━━━
<b>⌮ 𝗜𝗻𝗳𝗼 ⤳ </b>  <code>{brand}-{type}-{level}</code>
<b>⌮ 𝘽𝘼𝙉𝙆 ⤳ </b>  <code>{bank}</code>
<b>⌮  𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ⤳ </b>  <code>{country_name} [{country_flag}]</code>
━━━━━━━━━━━━━━
<b>⌮ 𝐄𝐗𝐓𝐑𝐀 𝐁𝐈𝐍 ⤳ </b>  <code>{bin}xxxx|{month}|{year}|rnd</code>
<b>⌮ 𝗡𝗮𝗺𝗲 ⤳ </b>  <code>{full_name}</code>
━━━━━━━━━━━━━━
"""

# ========== BUTTONS (Inline Keyboard) ==========
BUTTONS = [
    {"text": "👤 DEV", "url": "https://t.me/Murphythox"},
    {"text": "📢 CHANNEL", "url": "https://t.me/+Au7NgQAPKhVlN2Fh"},
    {"text": "💬 CHAT", "url": "https://t.me/+uuaKK1cUwPw0NDZk"}
]