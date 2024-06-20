import requests
import json
import uuid

from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

created_time = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc).isoformat()

class figgs:
    def __init__(self, url="https://www.figgs.ai/", auth=None):
        self.url = url 
        self.auth = auth
        self.payload = self.load_payload()

    def load_payload(self):
        try:
            with open('payload.json', 'r') as file:
                try:
                    payload_data = json.load(file)
                except json.JSONDecodeError:
                    payload_data = {
                        "botId": None,
                        "roomId": None,
                        "previousMessagesVersion": [],
                        "messages": []
                    }
        except FileNotFoundError:
            payload_data = {
                "botId": None,
                "roomId": None,
                "previousMessagesVersion": [],
                "messages": []
            }
        return payload_data

    def save_payload(self):
        with open('payload.json', 'w') as file:
            json.dump(self.payload, file)

    def fetch_page(self):
        response = requests.get(self.url, verify=False)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def change_user_name(self,username: str):
        soup = self.fetch_page()
        if soup:
            headers ={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Content-Type": "application/json",
            }    
            cookies = {
                'figs-auth-prod': self.auth
            }
            payload = {
                "name": username,
 
            }
            edit_url = f"https://www.figgs.ai/api/proxy/users/me"
            requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
            print("Your Username Changed To: ", username)
        else:
            print("ded")

    def change_bio(self,bio: str):
            soup = self.fetch_page()
            if soup:
                headers ={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                }    
                cookies = {
                    'figs-auth-prod': self.auth
                }
                payload = {
                    "description": bio
    
                }
                edit_url = f"https://www.figgs.ai/api/proxy/users/me"
                response = requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
                return response
            else:
                print("ded")

    def change_suggistives(self,hide_suggestive: bool, hide_suggestive_avatar:bool):
            soup = self.fetch_page()
            if soup:
                headers ={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                }    
                cookies = {
                    'figs-auth-prod': self.auth
                }
                payload = {
                    "hide_suggestive": hide_suggestive,
                    "hide_suggestive_avatar": hide_suggestive_avatar
    
                }
                edit_url = f"https://www.figgs.ai/api/proxy/users/me"
                requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
                print("hide Suggestive: ", hide_suggestive, "Hide Suggestive Avatar: ", hide_suggestive_avatar)
            else:
                print("ded")

    def send_message(self, messages: str, room_id: str, bot_id: str):
        soup = self.fetch_page()
        full_text = ""
        
        if soup:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Content-Type": "application/json",
            }
            cookies = {
                'figs-auth-prod': self.auth
            }
            self.payload["botId"] = bot_id
            self.payload["roomId"] = room_id
            self.payload["messages"].append({
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": messages,
                "created": created_time
            })


            try:
                api_url = "https://api.figgs.ai/chat_completion"
                response = requests.post(api_url, headers=headers, json=self.payload, cookies=cookies, verify=False)

                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith("data: "):
                            json_str = line_str.split("data: ", 1)[1]
                            try:
                                if json_str.strip():
                                    data = json.loads(json_str)
                                    if isinstance(data, dict) and "content" in data:
                                        full_text += data["content"]

                            except json.JSONDecodeError as e:
                                print("JSON decode error:", e)
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
        self.save_payload()
        return full_text.strip()
