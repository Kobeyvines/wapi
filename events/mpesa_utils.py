import requests
import base64
from datetime import datetime
from django.conf import settings
from requests.auth import HTTPBasicAuth

class MpesaHandler:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.base_url = "https://sandbox.safaricom.co.ke"
        
    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        return response.json().get('access_token')
    
    def trigger_stk_push(self, phone_number, amount, callback_url, reference):
        token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPaybillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": reference,
            "TransactionDesc": f"Payment for {reference}"
        }

        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.base_url}/mpesa/stkpush/v1/query" # Use the processrequest endpoint for actual push
        # Correction: The sandbox process URL is:
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json()