from .csv_writer import write_report
from .discord_webhook import upload_report
from .sources.threatfox import fetch_recent_iocs, to_report_row

def main():
    result = fetch_recent_iocs()
    if result["query_status"] != "ok":
        print(f"ThreatFox returned{result['query_status']}, skipping")
        return

    rows = [to_report_row(record) for record in result["data"]]
    if not rows:
        print("No rows to write, skipping")
        return

    path = "threat_intel.csv"
    write_report(rows, path)
    filename = upload_report(path)
    print(f"uploaded {len(rows)} indicators as {filename} to Discord")


if __name__ == "__main__":
    main()