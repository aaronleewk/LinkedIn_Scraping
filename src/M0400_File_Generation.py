"""
Convert json to csv format
"""
import json
import csv
import datetime

date = str(datetime.date.today())

with open('Data/%s/M0300_profile_insights.json' % date,  encoding="UTF-8") as file:
    summary = json.load(file)
    file.close()

summary_full = summary

#Generate headings
headings = list(summary_full[0].keys())

with open('Data/%s/M0400_report.csv' % date, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headings)

    for each in summary_full:
        writer.writerow(each.values())

    file.close