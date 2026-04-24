import urllib.request, urllib.parse, ssl, os, re, json

URL = "https://visas.migracion.gob.pa/SIVA/verif_citas/"
ALWAYS_PRESENT = "citasconsulares/Reportes/indexcuba"

NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")
GREEN_INSTANCE = os.environ.get("GREEN_INSTANCE", "")
GREEN_TOKEN = os.environ.get("GREEN_TOKEN", "")
WHATSAPP_TO = os.environ.get("WHATSAPP_TO", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def disponible(html):
    hrefs = re.findall(r"href=[\"'](https?://[^\"'>]+)[\"']", html, re.IGNORECASE)
    nuevos = [h for h in hrefs if ALWAYS_PRESENT.lower() not in h.lower()]
    return nuevos


def send_ntfy(link):
    msg = urllib.parse.urlencode({
        "title": "CITAS DISPONIBLES - Panama en Cuba",
        "message": "El formulario esta abierto. Entra ahora!",
        "click": link,
        "priority": "urgent",
        "tags": "passport,rotating_light",
    }).encode()
    req = urllib.request.Request(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=msg,
        headers={"User-Agent": "Mozilla/5.0"},
        method="POST"
    )
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        print("ntfy enviado, status:", r.status)


def send_whatsapp(link):
    body = json.dumps({
        "chatId": f"{WHATSAPP_TO}@c.us",
        "message": f"CITAS DISPONIBLES - Consulado Panama en Cuba\nEntra ahora: {link}"
    }).encode()
    url = f"https://7107.api.greenapi.com/waInstance{GREEN_INSTANCE}/sendMessage/{GREEN_TOKEN}"
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        print("WhatsApp enviado, status:", r.status)


html = fetch()
links = disponible(html)

if links:
    print("CITAS DISPONIBLES:", links[0])
    send_ntfy(links[0])
    send_whatsapp(links[0])
else:
    print("Sin citas disponibles.")
