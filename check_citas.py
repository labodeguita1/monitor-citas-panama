import urllib.request, urllib.parse, ssl, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")
msg = urllib.parse.urlencode({
    "title": "PRUEBA GITHUB ACTIONS - Monitor Citas",
    "message": "El monitor en la nube funciona! Recibiras alertas cuando abran las citas.",
    "priority": "urgent",
    "tags": "rocket",
}).encode()
req = urllib.request.Request(
    f"https://ntfy.sh/{NTFY_TOPIC}",
    data=msg, headers={"User-Agent": "Mozilla/5.0"}, method="POST"
)
with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
    print("Notificacion enviada, status:", r.status)
