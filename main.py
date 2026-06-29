#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Credit Card Generator Bot
Generates valid credit cards (Luhn algorithm), checks BIN, sends to Telegram
Author: @Murphythox
GitHub: https://github.com/sadikmahedi88
"""

import requests
import random
import time
import json
import sys
from faker import Faker
from config import *

fake = Faker()

# =====================================================================
# CARD GENERATION
# =====================================================================

def generate_card_number(card_type):
    """Generate a valid credit card number using Luhn algorithm"""
    if card_type not in CARD_PREFIXES:
        card_type = random.choice(list(CARD_PREFIXES.keys()))
    
    prefix = random.choice(CARD_PREFIXES[card_type])
    
    # Determine card length
    if card_type == 'American Express':
        length = 15
    elif card_type == 'Diners Club':
        length = 14
    else:
        length = 16
    
    # Generate the main part of the number
    body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    # Calculate check digit using Luhn algorithm
    digits = [int(d) for d in body]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    return body + str(check_digit), card_type

def generate_card_details():
    """Generate complete credit card details"""
    card_number, card_type = generate_card_number(random.choice(list(CARD_PREFIXES.keys())))
    
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(25, 32)).zfill(2)
    
    if card_type == 'American Express':
        cvv = str(random.randint(1000, 9999)).zfill(4)
    else:
        cvv = str(random.randint(100, 999)).zfill(3)
    
    return f"{card_number}|{month}|{year}|{cvv}", card_type

def luhn_algorithm(card_number):
    """Validate credit card using Luhn algorithm"""
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

# =====================================================================
# BIN LOOKUP
# =====================================================================

def get_bin_info(bin_number):
    """Fetch BIN information from API"""
    try:
        response = requests.get(
            f"https://bins.antipublic.cc/bins/{bin_number}",
            timeout=10
        )
        if response.status_code == 200 and response.json().get('brand'):
            data = response.json()
            return {
                'brand': data.get('brand', 'UNKNOWN'),
                'country': data.get('country', 'US'),
                'country_name': data.get('country_name', 'United States'),
                'country_flag': data.get('country_flag', '🇺🇸'),
                'bank': data.get('bank', 'Unknown Bank'),
                'level': data.get('level', 'Standard'),
                'type': data.get('type', 'Credit')
            }
    except Exception as e:
        print(f"⚠️ BIN API error: {e}")
    
    return {
        'brand': 'UNKNOWN',
        'country': 'US',
        'country_name': 'United States',
        'country_flag': '🇺🇸',
        'bank': 'Unknown Bank',
        'level': 'Standard',
        'type': 'Credit'
    }

# =====================================================================
# TELEGRAM SENDER
# =====================================================================

def send_to_telegram(card_details, bin_info, full_name):
    """Send credit card details to Telegram"""
    card_number = card_details.split('|')[0]
    bin_number = card_number[:6]
    month, year, cvv = card_details.split('|')[1], card_details.split('|')[2], card_details.split('|')[3]
    
    # Format message
    message = MESSAGE_TEMPLATE.format(
        card_details=card_details,
        bin=bin_number,
        brand=bin_info['brand'].upper(),
        type=bin_info['type'],
        level=bin_info['level'],
        bank=bin_info['bank'],
        country_name=bin_info['country_name'],
        country_flag=bin_info['country_flag'],
        month=month,
        year=year,
        full_name=full_name
    )
    
    # Create inline keyboard
    reply_markup = {
        "inline_keyboard": [[
            {"text": btn['text'], "url": btn['url']} for btn in BUTTONS
        ]]
    }
    
    # Send with photo
    try:
        with open(PHOTO_PATH, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': CHAT_ID,
                'caption': message,
                'parse_mode': 'HTML',
                'reply_markup': json.dumps(reply_markup)
            }
            response = requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
                files=files,
                data=data,
                timeout=30
            )
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Telegram error: {response.text}")
                return False
    except FileNotFoundError:
        print(f"⚠️ Photo not found: {PHOTO_PATH}")
        print("   Sending without photo...")
        # Fallback: send without photo
        return send_text_to_telegram(message, reply_markup)
    except Exception as e:
        print(f"❌ Error sending: {e}")
        return False

def send_text_to_telegram(message, reply_markup):
    """Send message without photo (fallback)"""
    try:
        data = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps(reply_markup)
        }
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            data=data,
            timeout=30
        )
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error sending text: {e}")
        return False

# =====================================================================
# MAIN
# =====================================================================

def main():
    print("="*60)
    print("   💳 Credit Card Generator Bot")
    print(f"   👤 {DEV_USERNAME}")
    print(f"   📢 {DEV_CHANNEL}")
    print("="*60)
    print(f"📊 Total Cards: {TOTAL_CARDS}")
    print(f"📁 Photo: {PHOTO_PATH}")
    print("="*60)
    
    # Check if photo exists
    try:
        with open(PHOTO_PATH, 'rb'):
            print("✅ Photo found\n")
    except FileNotFoundError:
        print("⚠️ Photo not found - sending without photo\n")
    
    print("🚀 Starting generation...\n")
    
    success_count = 0
    fail_count = 0
    
    for i in range(1, TOTAL_CARDS + 1):
        # Generate card
        card_details, card_type = generate_card_details()
        card_number = card_details.split('|')[0]
        
        # Validate card
        if not luhn_algorithm(card_number):
            print(f"❌ [{i}] Invalid card, regenerating...")
            continue
        
        # Get BIN info
        bin_number = card_number[:6]
        bin_info = get_bin_info(bin_number)
        full_name = fake.name()
        
        # Send to Telegram
        success = send_to_telegram(card_details, bin_info, full_name)
        
        if success:
            print(f"✅ [{i}/{TOTAL_CARDS}] {card_type}: {card_details}")
            success_count += 1
        else:
            print(f"❌ [{i}/{TOTAL_CARDS}] Failed: {card_details}")
            fail_count += 1
        
        # Rate limiting
        if i % REQUEST_LIMIT == 0 and i != TOTAL_CARDS:
            print(f"⏳ Pausing for {PAUSE_DURATION} seconds...")
            time.sleep(PAUSE_DURATION)
    
    print("\n" + "="*60)
    print("📊 FINAL STATISTICS")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📦 Total: {TOTAL_CARDS}")
    print("="*60)

# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user.")
        sys.exit(0)