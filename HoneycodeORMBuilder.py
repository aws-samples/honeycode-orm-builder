#  Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
#  with the License. A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
#  and limitations under the License.
import os

import boto3
import jinja2
import sys
from pathlib import Path
import re

class HoneycodeORMBuilder:
    def __init__(self, workbookid) -> object:
        self.workbookid = workbookid
        self.pythonvarnameregex = re.compile('[^a-zA-Z0-9]')
        self.honeycode_client = boto3.client('honeycode')
        Path("orm").mkdir(parents=True, exist_ok=True)
        dir = os.getcwd() + '/orm'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    def buildORM(self):
        honeycodetabledec = self.honeycode_client.list_tables(
            workbookId=self.workbookid)
        for table in honeycodetabledec['tables']:
            tableName = table["tableName"]
            tableId = table["tableId"]
            templateLoader = jinja2.FileSystemLoader(searchpath="./")
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template("HoneyCodeORM.template")

            honeycodecolumndec = self.honeycode_client.list_table_columns(
                workbookId=self.workbookid, tableId=tableId)
            printstatement = self.buildPrintStatement(honeycodecolumndec)
            outputText = template.render(classNameEditor=tableName + "BatchOperations",
                                         tableID=tableId,
                                         workbookID=self.workbookid,
                                         tableName=tableName,
                                         findDataFromColumn=self.buildConvert(honeycodecolumndec),
                                         classnameRow=tableName,
                                         printstatment = printstatement,
                                         variableNamesParams=self.buildParamsForTable(honeycodecolumndec),
                                         variableNamesAlloc=self.buildVarAllocForTable(honeycodecolumndec),
                                         honeyCodeRowDefs=self.buildInsertForTable(honeycodecolumndec) )
            text_file = open("orm/" + tableName + ".py", "w")
            text_file.write(outputText)
            text_file.close()


    def buildInsertForTable(self, response):
        tableDescript = response["tableColumns"]
        buildstuff = ""
        for tableColumn in tableDescript:
            buildstuff += '        ' + "if self." + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + ":\n"
            buildstuff += '            dictToAdd[operation][' + '"' + tableColumn["tableColumnId"] + '"' + '] = {"fact": self.' + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + "}\n"
        return buildstuff

    def buildPrintStatement(self, response):
        tableDescript = response["tableColumns"]
        buildstuff = ""
        for tableColumn in tableDescript:
            buildstuff += ' "' + tableColumn["tableColumnName"] + '=" + str(self.' + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + ') + "," +'
        return buildstuff[:len(buildstuff)-8]

    def buildVarAllocForTable(self, response):
        tableDescript = response["tableColumns"]
        buildstuff = ""
        for tableColumn in tableDescript:
            buildstuff += '        self.' + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + " = " + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + '\n'
        return buildstuff

    def buildConvert(self, response):
        tableDescript = response["tableColumns"]
        i = 0
        retVal = ""
        while i < len(tableDescript):
            retVal += 'row["cells"]['+str(i)+'].get("formattedValue"), '
            i+=1
        return retVal[:-2]

    def buildParamsForTable(self, response):
        tableDescript = response["tableColumns"]
        params = ""
        for tableColumn in tableDescript:
            params = params + "," + self.pythonvarnameregex.sub('', tableColumn["tableColumnName"]).lower() + "=None"
        return params

    def getTableIdByName(self, name):
        response = self.honeycode_client.list_tables(
            workbookId=self.workbookid)
        for table in response['tables']:
            if table["tableName"] == name:
                return table["tableId"]
        return ""

def main(workbookid):
    hcb = HoneycodeORMBuilder(workbookid)
    hcb.buildORM()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass in workbook id")
    else:
        main(sys.argv[1])
