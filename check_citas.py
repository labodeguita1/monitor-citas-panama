import urllib.request
import urllib.parse
import ssl
import re
import os
import sys

URL = "https://visas.migracion.gob.pa/SIVA/verif_citas/"
ALWAYS_PRESENT = "citasconsulares/Reportes/indexcuba"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")

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


def notify(link):
    if not NTFY_TOPIC:
        print("ERROR: variable NTFY_TOPIC no configurada")
        sys.exit(1)
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
        print("Notificacion enviada, status:", r.status)


html = fetch()
links = disponible(html)

if links:
    print("CITAS DISPONIBLES:", links)
    notify(links[0])
else:
    print("Sin citas disponibles.")
