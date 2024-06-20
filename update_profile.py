import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

BANNER_IMAGE_URL = "https://giffiles.alphacoders.com/906/90670.gif" # Your Gif
banner_image_response = requests.get(BANNER_IMAGE_URL)

if banner_image_response.status_code == 200:
    banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
    payload = {
        "banner": f"data:image/gif;base64,{banner_image_base64}"
    }
    headers = {
        'Authorization': f'Bot {os.getenv("BOT_TOKEN")}',
        'Content-Type': 'application/json'
    }
    response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)
    if response.status_code == 200:
        print('Profile picture and banner changed successfully!')
    else:
        print('Failed to change profile picture and banner:', response.text)
else:
    print('Failed to download profile picture or banner')