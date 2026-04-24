import urllib.request, json, ssl, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

GREEN_INSTANCE = os.environ.get("GREEN_INSTANCE", "")
GREEN_TOKEN = os.environ.get("GREEN_TOKEN", "")
WHATSAPP_TO = os.environ.get("WHATSAPP_TO", "")

body = json.dumps({
    "chatId": f"{WHATSAPP_TO}@c.us",
    "message": "PRUEBA GITHUB ACTIONS - El monitor esta funcionando en la nube! Te avisare cuando abran las citas de Panama en Cuba."
}).encode()

url = f"https://7107.api.greenapi.com/waInstance{GREEN_INSTANCE}/sendMessage/{GREEN_TOKEN}"
req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
    print("WhatsApp enviado, status:", r.status, r.read().decode())
