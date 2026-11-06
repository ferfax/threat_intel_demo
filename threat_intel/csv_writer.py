import csv

def write_report(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "information", "source"])
        writer.writeheader()
        writer.writerows(rows)
