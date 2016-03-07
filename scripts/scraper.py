from __future__ import print_function

import datetime
import os
import re
import textwrap
import time
import pdb
import json

import github3

def github_client():
    return github3.login(
        os.environ["GITHUB_USERNAME"],
        os.environ["GITHUB_PASSWORD"],
    )

def get_status(str):
    #remove everything before first | and after last |
    return str.split("|")[1].title().strip()
    
def addProductToArray(document, array):
    splitByLine = document.splitlines()
    splitByLine = filter(lambda x: not re.match(r'^\s*$', x), splitByLine)
    productName = splitByLine[0].split(":")[1].strip()
    productLead = splitByLine[1].split(":")[1].strip()
    businessOwner = splitByLine[2].split(":")[1].strip()
    launchDateString = splitByLine[3].split(":")[1].strip()
    
    productName = "<a href=/jekyll/update/2016/01/27/product-dashboard.html?" + productName.replace(" ", "_") + ">" + productName + "</a>"

    if "/" in launchDateString:
        year = launchDateString.split("/")[1].strip()
        month = launchDateString.split("/")[0].strip()
    else:
        year = "2020"
        month = "12"
        
    if(len(month) < 2):
        month = "0" + month
    
    for line in splitByLine:
        if "COMPLETE ALL PRODUCT DEFINITION TASKS" in line:
            productDefinition = get_status(line)
        if "COMPLETE ALL DISCOVERY TASKS " in line:
            discovery = get_status(line)
        if "COMPLETE ALL DESIGN TASKS" in line:
            prototype = get_status(line)
        if "COMPLETE ALL PRE FLIGHT TASKS" in line:
            preFlight = get_status(line)
        if "COMPLETE ALL GO LIVE TASKS" in line:
            goLive = get_status(line) 
    #create new object with this data
    # save the object to an array
    #return
    comma = ","
    sequence = (year,month,productName,productLead,businessOwner,productDefinition,
                               discovery,prototype,preFlight,goLive,launchDateString)
    productString = comma.join(sequence)
    array.append(productString)
    return
  
def writeExecutiveSummary(array, outputFile):
    array.sort()
    for product in array:
        outputFile.write(product[8:] + "\n")
    return
      
def writeProductStatusReport(document):
    splitByLine = document.splitlines()
    splitByLine = filter(lambda x: not re.match(r'^\s*$', x), splitByLine)
    productName = splitByLine[0].split(":")[1].strip()
    productLead = splitByLine[1].split(":")[1].strip()
    businessOwner = splitByLine[2].split(":")[1].strip()
    launchDateString = splitByLine[3].split(":")[1].strip()
    
    directory = "product_csv_files/" + productName.replace(" ", "_")
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    i = 7
    i = writeSection(directory + "/product_definition.csv", i, splitByLine)  
    i = writeSection(directory + "/discovery.csv", i, splitByLine)  
    i = writeSection(directory + "/prototype.csv", i, splitByLine) 
    i = writeSection(directory + "/pre_flight.csv", i, splitByLine) 
    i = writeSection(directory + "/go_live.csv", i, splitByLine)  
        
    return


def writeSection(fileName, i, array):
    fileToWrite = open(fileName, 'w')
    writeHeader(fileToWrite)
    while "COMPLETE" not in array[i]:
        toWrite = ",".join(map(str.strip, array[i].split("|")))
        if("Conduct technical discovery (security, systems, data, etc.)" in toWrite):
            toWrite = toWrite.replace("Conduct technical discovery (security, systems, data, etc.)", "\"Conduct technical discovery (security, systems, data, etc.)\"")
        if("Conduct pre-launch tasks (per the [launch guide](https://github.com/department-of-veterans-affairs/vets.gov-team/blob/master/Project%20Management/Launch%20Guide.md))" in toWrite):
            toWrite = toWrite.replace("Conduct pre-launch tasks (per the [launch guide](https://github.com/department-of-veterans-affairs/vets.gov-team/blob/master/Project%20Management/Launch%20Guide.md))",
                                      "Conduct pre-launch tasks (per the <a target=blank href=https://github.com/department-of-veterans-affairs/vets.gov-team/blob/master/Project%20Management/Launch%20Guide.md>Launch Guide</a>)")
        fileToWrite.write(toWrite)
        fileToWrite.write("\n")
        i += 1
    fileToWrite.write(",".join(map(str.strip, array[i].split("|"))))
    fileToWrite.write("\n")
    i += 4    
    fileToWrite.close()
    return i
    
def writeHeader(fileName):
    fileName.write('Task,Status,Comments (only if Yellow or Red\n')
    
def writeDetailedDashboard(document, outputFile):
    return
    
def readEachFile(repo, directory):
    executiveDashboard = open('executiveDashboard.csv','w')
    executiveDashboard.write('Product,Vets.gov Lead,VA Business Owner,Product Definition,Discovery,Prototype,Pre Flight,Go Live,Launch Date\n')
    #detailedDashboard = open('detailedDashboard.csv','w')
    #TODO write first line of detailed dashboard
    executiveDashboardArray = []
    for docName in directory:
        if docName.lower() != "readme.md" and docName.lower() != "link to launch guide.md" and docName.lower() != "use this template.md":    
            fullPath = "Status Reports and Roadmaps/Sample-Status-Reports/" + docName
            document = repo.contents(fullPath).decoded
            addProductToArray(document, executiveDashboardArray)
            #writeDetailedDashboard(document, detailedDashboard)
            writeProductStatusReport(document)
    writeExecutiveSummary(executiveDashboardArray, executiveDashboard)
    executiveDashboard.close()
    #detailedDashboard.close()

def main():
    gh_client = github_client()

    directory = "product_csv_files"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    repo = gh_client.repository("department-of-veterans-affairs", "vets.gov-team")
    directory = repo.contents("Status Reports and Roadmaps/Sample-Status-Reports")
    readEachFile(repo, directory)
    

if __name__ == "__main__":
    main()