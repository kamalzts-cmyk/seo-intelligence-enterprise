import csv, io

def issues_csv(report):
    output = io.StringIO()
    fields = ["severity","category","issue","url","detail","evidence","why","root","fix","developer","ai","best","reference"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for issue in report["issues"]:
        writer.writerow({field: issue.get(field, "") for field in fields})

    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    mem.seek(0)
    return mem
