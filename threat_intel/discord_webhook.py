import os
from pathlib import Path

import requests

def upload_report(path):
    report = Path(path)
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    with report.open("rb") as file:
        response = requests.post(
            webhook_url,
            params={"wait": "true"},
            files={"files[0]": (report.name, file, "text/csv")},
            timeout=30,
        )

    if response.status_code != 200:
        raise RuntimeError(f"Discord uplaod failed(http status: {response.status_code})")
    return response.json()["attachments"][0]["filename"]