import os
import requests

API_URL = "https://threatfox-api.abuse.ch/api/v1/"


def fetch_recent_iocs():
    response = requests.post(
        API_URL,
        headers={"Auth-Key": os.environ["THREATFOX_AUTH_KEY"]},
        json={"query": "get_iocs", "days": 1},
        timeout=10,
    )
    if response.status_code == 403:
        print(response.text[:500])
    response.raise_for_status()

    return response.json()

def to_report_row(record):
    return {
        "date": record["first_seen"],
        "information": f"{record['ioc_type']}: {record['ioc']} | {record['malware_printable']}",
        "source": f"https://threatfox.abuse.ch/ioc/{record['id']}/"
    }


# Example ThreatFox input with all 17 fields seen in our get_iocs response.
# Values are illustrative. Python uses None for a JSON null.
# {
#     "id": "2015369",
#     "ioc": "https://example.invalid/",
#     "threat_type": "payload_delivery",
#     "threat_type_desc": "Endpoint that delivers a malware payload",
#     "ioc_type": "url",
#     "ioc_type_desc": "URL that delivers a malware payload",
#     "malware": "unknown",
#     "malware_printable": "Unknown malware",
#     "malware_alias": None,
#     "malware_malpedia": None,
#     "confidence_level": 75,
#     "is_compromised": False,
#     "first_seen": "2026-11-05 06:01:11 UTC",
#     "last_seen": None,
#     "reference": None,
#     "reporter": "example_reporter",
#     "tags": ["example"],
# }
#
# The same record as a report row:
# {
#     "date": "2026-11-05 06:01:11 UTC",
#     "information": "url: https://example.invalid/ | Unknown malware",
#     "source": "https://threatfox.abuse.ch/ioc/2015369/",
# }
#
# date         = when ThreatFox first saw the indicator, in UTC
# information  = indicator type, indicator value, and malware name
# source       = ThreatFox report URL built from the record ID
#
# To try a new format offline, copy the example input into a dictionary
# named record, then run to_report_row(record).
