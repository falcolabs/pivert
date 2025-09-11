from main import APP
import uvicorn
from subprocess import Popen

if __name__ == "__main__":
    Popen([".venv/bin/python3", "-m", "https_redirect"])
    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=443,
        ssl_certfile="/etc/letsencrypt/live/pivert.falcolabs.org/fullchain.pem",
        ssl_keyfile="etc/letsencrypt/live/pivert.falcolabs.org/privkey.pem",
    )
