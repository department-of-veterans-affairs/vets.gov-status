import datetime
import os
import re
import textwrap
import time
import pdb
import json

import github3

MARKDOWN_DIR = "Communications/OLD_Status Reports/Sample-Status-Reports"
IGNORE_LIST = ["readme.md",
               "project status template.md",
               "link to launch guide.md",
               "use this template.md",
              ]

def createDashboardCSV(repo, markdown_files):
    output_file = os.path.join(os.environ['DATA_DIR'], 'migration_status.csv')
    with open(output_file, 'w') as migration_status:
        migration_status.write('name,lead,business_owner,definition,discovery,prototype,preflight,go_live,launch_date\n')
        product_rows = []
        for md in markdown_files:
            if md.lower() not in IGNORE_LIST:
                full_path = MARKDOWN_DIR + '/' + md
                document = repo.file_contents(full_path).decoded.decode('utf-8')
                product_rows.append(docToRow(document))
        product_rows.sort()
        for row in product_rows:
            migration_status.write(row[8:] + "\n")

def docToRow(document):
    lines = document.splitlines()
    lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
    product_name = lines[0].split(":")[1].strip()
    product_lead = lines[1].split(":")[1].strip()
    business_owner = lines[2].split(":")[1].strip()
    launch_date = lines[3].split(":")[1].strip()

    if "/" in launch_date:
        year = launch_date.split("/")[1].strip()
        month = launch_date.split("/")[0].strip()
    else:
        year = "2020"
        month = "12"

    if len(month) < 2:
        month = "0" + month

    for line in lines:
        if "COMPLETE ALL PRODUCT DEFINITION TASKS" in line:
            product_definition = get_status(line)
        elif "COMPLETE ALL DISCOVERY TASKS " in line:
            discovery = get_status(line)
        elif "COMPLETE ALL DESIGN TASKS" in line:
            prototype = get_status(line)
        elif "COMPLETE ALL PRE FLIGHT TASKS" in line:
            preflight = get_status(line)
        elif "COMPLETE ALL GO LIVE TASKS" in line:
            go_live = get_status(line)

    return ",".join((year, month, product_name, product_lead, business_owner, product_definition,
                     discovery, prototype, preflight, go_live, launch_date))

def get_status(string):
    """remove everything before first | and after last |"""
    return string.split("|")[1].title().strip()

def main():
    gh_client = github3.GitHub(os.environ["GH_USER"],
                               token=os.environ["GH_TOKEN"])
    repo = gh_client.repository("department-of-veterans-affairs", "vets.gov-team")
    markdown_files = repo.directory_contents(MARKDOWN_DIR, return_as=dict)

    createDashboardCSV(repo, markdown_files)


if __name__ == "__main__":
    main()