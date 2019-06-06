##// CURRENT:
##// list of topics by {TOPIC:[["TITLE", "URL"]]}
##
##// FUTURE:
##////list of topics by {TOPIC:[["TITLE", "URL", "TAGS"],
##////                          ["TITLE", "URL", "TAGS"]]}
from itertools import chain
from glob import glob
import json

def Content():
	TOPIC_DICT = {"Catalog":[["ABS - Census Data","/abs_census/"],["Weather (TBD)","/weather/"]]} 
	return TOPIC_DICT

	
def TableList():
    with open('tables/ABS_Table_names.txt','r') as f:
        ABSTableslist = json.load(f)
        TABLE_DICT = {"ABS":ABSTableslist}
        return TABLE_DICT

def ColumnList(myList = [], *args):
    with open('tables/ABS_Column_names.txt','r') as f:
        ABSColumnlist = dict(json.load(f))
        columnKeys = (ABSColumnlist.keys())
        newlist = {}
        for item in myList:
            newlist[item] = ABSColumnlist[item]
        return newlist

def Level1List():
	LEVEL_1_DICT = {"Year":["2016","2011"],"Geographies":["SA","NSW","VIC"],"By":["PostCodes","Region","Suburb"]}
	return LEVEL_1_DICT

##Runtime Test	
if __name__ == "__main__":
    tablelist = ['2016Census_G02_SA_POA','2016Census_G01_SA_POA']
    COLUMNSLIST = ColumnList(tablelist)
    for each in COLUMNSLIST:
        print(each)
        print("--------------------------------------------------")
        for each in COLUMNSLIST[each]:
            print(each[0])
            print(each[1])