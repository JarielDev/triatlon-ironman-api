import httpx

url = "https://www.strava.com/api/v3/oauth/token"
data = {
    "client_id": "239240",
    "client_secret": "2b5a1c1215fec92ab3606215fc37f0e68c915160",
    "code": "50f82ca4f0e6a57938f7b7f155b3b8fdf127bfb1", # <--- Nuevo código
    "grant_type": "authorization_code"
}

response = httpx.post(url, data=data)
print(response.json())