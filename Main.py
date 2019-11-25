#V1.0

import requests, sys, base64, json, logging, socket, re, time, os
import xml.etree.ElementTree as ET
from template.cv_add_deduplication import AddDeduplicationPolicy
from template.cv_add_library import Library_Disk_Add
from template.cv_add_user import UserInfo_Add
from template.cv_add_subclient import SubClient
from configure.cv_basic_config import Basic_Info
from template.cv_sche_ecm import SchedPolicy_ECM
from template.cv_sche_clmp import SchedPolicy_CLMP
from template.cv_sche_staging import SchedPolicy_STAGING
from template.cv_sche_modify import SchedPolicy_Modify
from template.cv_sche_gold import SchedPolicy_GOLD
from template.cv_sche_silver import SchedPolicy_SILVER
from template.cv_sche_bronze import SchedPolicy_BRONZE

# FORMAT = "%(asctime)s %(thread)d %(message)s"
# logging.basicConfig(
#         level=logging.INFO,
#         format=FORMAT,
#         filename='logger.log' )
#
#
# log = logging.getLogger()
#
# logging.info("!!!!!!!!!!!!!!!!!!!")

#Check Configure File

# Input_Infra_Val = raw_input("=====>>> Have you install infra client in the BPS Server [yes|no]")
#
# if Input_Infra_Val.lower() == "no":
#     print "=====>>> The script has stopped. Please install the client in the BPS server. "
#     sys.exit()

# Input_MA_Val = raw_input("=====>>> Have you install MediaAgent in the Windows Server [yes|no]")
#
# if Input_MA_Val.lower() == "no":
#     print "=====>>> The script has stopped. Please install the  MediaAgent in the Windows Server. "
#     sys.exit()

for key,values in Basic_Info.items():
    print "%s = %s"%(key,values)
# print "\n=====>>> Please Check Parameter and Press 'Enter' key to continue installation..."
# os.system('pause > nul')

pwd = base64.b64encode(Basic_Info["CV_CommCell_Password"])
service = 'http://%s:81/SearchSvc/CVWebService.svc/'%(Basic_Info["CV_CommCell_Address"])

Http_Data_Part = {
  "password": pwd,
  "username": Basic_Info["CV_CommCell_User"]
}

Login_Act = json.dumps(Http_Data_Part)

headers_json = {
  'Accept' : 'application/json',
  'Content-Type': "application/json"
}

headers_xml = {
  'Accept' : 'application/json',
  'Content-Type': "text/xml"
}


#Connection Commvault API and get token
def GetToken():
  RequestToken = requests.post(service + 'Login', data=Login_Act, headers=headers_json)
  if RequestToken.status_code == 200:
      Token = json.loads(RequestToken.text)
      if len(Token["errList"]) == 0:
        headers_json['Authtoken'] = Token["token"]
        headers_xml['Authtoken'] = Token["token"]
        print "=====>>> Got the Token"
        return headers_json, headers_xml
      else:
        message = Token["errList"][0]["errLogMessage"]
        print "=====>>> ", message


#Select Commvault User
def ShowUser():
  SelectUser = json.loads(requests.get(service + "User", headers=headers_json).text)
  Select_Commvault_User = [User_Val["userEntity"]["userName"] for User_Val in SelectUser["users"]]
  for User_Val in Add_Commvault_User:
    if User_Val in Select_Commvault_User:
      print "=====>>> Create %s sucessful "%(User_Val)

#Get Current MediaAgent ID
def MediaAgent():
  Get_MediaAgent = requests.get(service + "MediaAgent", headers=headers_json)
  Get_MediaAgent = json.loads(Get_MediaAgent.text)["response"]

  for Get_MediaAgent_Val in Get_MediaAgent:
    if Get_MediaAgent_Val["entityInfo"]["name"] == Basic_Info["CV_MediaAgent_Name"]:
      Get_MediaAgent_ID = Get_MediaAgent_Val["entityInfo"]["id"]
      return Get_MediaAgent_ID


#Check Return Code
def Check_Return_Code(Dictionary):
    Code_Value = 0
    for Key,Value in Dictionary.items():
        if Key == "errorCode":
            Code_Value = Value
        elif "already exists" in Value:
            Code_Value = 5
        elif isinstance(Key,dict) :
            Check_Return_Code(Dictionary[Key])
    return Code_Value


#get disk library id

def Get_Library_Id():

    Library_ID={}
    SelectLibraryId = json.loads(requests.get(service + "Library", headers=headers_json).text)

    for Library_Val in SelectLibraryId["response"]:
        if Basic_Info["CV_DC_Number"] in Library_Val["entityInfo"]["name"]:
            Library_ID_Val = {Library_Val["entityInfo"]["name"]:Library_Val["entityInfo"]["id"]}
            Library_ID.update(Library_ID_Val)
    return Library_ID


#Add disk library for MediaAgent
def AddDiskLibrary(*args):

    Library_ID = {}
    Library_Disk_Add["library"]["mediaAgentId"] = Get_MediaAgent_ID
    Library_Disk_Add["library"]["libraryName"] += "_"+Basic_Info["CV_DC_Number"]

    for key,value in args[0].items():
        Library_Disk_Add["library"]["libraryName"] =  "%s_%s"%(value[1],Basic_Info["CV_DC_Number"])
        Library_Disk_Add["library"]["mountPath"] = value[0]
        AddMediaAgent_Act = json.dumps(Library_Disk_Add)
        AddMediaAgent_Res = json.loads(requests.post(service + "Library", data=AddMediaAgent_Act, headers=headers_json).text)
        Return_Code=Check_Return_Code(AddMediaAgent_Res)

        if Return_Code == 0:
            Library_ID_Val = {Library_Disk_Add["library"]["libraryName"]:AddMediaAgent_Res["library"]["libraryId"]}
            Library_ID.update(Library_ID_Val)
        elif Return_Code == 5:
            Library_ID = Get_Library_Id()
        else:
            print "Can't get libraryID, Stop the program"
            os.system("exit")

        print "=====>>> Got the Library ID , Value is %s" % Library_ID
        return Library_ID


#modify & check Dictionary Part_1, the Dedu policy will  call it
def Modify_Check_Diect_1(Dictionary,part, key,val):

    if isinstance(Dictionary,dict):

        for key in Dictionary:
            if  key == part:
                Dictionary[key] = val
            elif isinstance(Dictionary[key],list):
                Modify_Check_Diect_2(Dictionary[key],part,key,val)
            elif isinstance(Dictionary[key],dict):
                Modify_Check_Diect_1(Dictionary[key],part, key,val)
            elif isinstance(Dictionary,list):
                Modify_Check_Diect_2(Dictionary,part, key,val)

    return Dictionary


#modify & check Dictionary Part_2
def Modify_Check_Diect_2(Dictionary,part, key,val):

    for val_ in Dictionary:
        if isinstance(val_, dict):
            Modify_Check_Diect_1(val_,part, key,val)
        elif isinstance(val_, list):
            Modify_Check_Diect_2(val_,part, key,val)


#Add Deduplication Policy
def Add_Dedu_Policy(AddDeduplicationPolicy):

    Add_Dedu_Policy=""

    for key, value in Library_ID.items():

        if "infra" in key.lower():
            Library_Name = key.replace("DISKLIB_","")
            DDBB_PATH = "d:\\DDBB_INFRA"
            Library_Id_Val = Library_ID["DISKLIB_INFRA_" + Basic_Info["CV_DC_Number"]]

        elif "tenant" in key.lower():
            Library_Name = key.strip("DISKLIB_")
            DDBB_PATH = "d:\\DDBB_TENANT"
            Library_Id_Val = Library_ID["DISKLIB_TENANT_" + Basic_Info["CV_DC_Number"]]


        Part_Dict = {"storagePolicyName": "GDP_" + Library_Name,
                     "copyName": "GDP_" + Library_Name + "_Primary",
                     "path": DDBB_PATH,
                     "libraryId": Library_Id_Val,
                     "mediaAgentId": Get_MediaAgent_ID,
                     "mediaAgentName": Basic_Info["CV_MediaAgent_Name"]}

        for Part_val_key, Part_val_val in Part_Dict.items():
            Add_Dedu_Policy = Modify_Check_Diect_1(AddDeduplicationPolicy,Part_val_key, Part_val_key, Part_val_val)

        AddDedupPolicy_Act = json.dumps(Add_Dedu_Policy)
        AddDedupPolicy_Res = requests.post(service+"StoragePolicy",data=AddDedupPolicy_Act,headers=headers_json)



#Add StoragePolicy
def Add_Storage_Policy(Storage_Policy_List):

    Storage_Policy_Tree = ET.parse('template\\cv_add_storage_policy.xml')
    Storage_Policy_Root = Storage_Policy_Tree.getroot()
    for Sto_Pol_Lis_Val in Storage_Policy_List:
        XML_SP_Name = Storage_Policy_Root.find('storagePolicyName')
        XML_SP_Name.text = Sto_Pol_Lis_Val["sp_name"]
        XML_GDP_Name = Storage_Policy_Root.find('storagePolicyCopyInfo/useGlobalPolicy/storagePolicyName')
        XML_GDP_Name.text = Sto_Pol_Lis_Val["gsp_name"]
        XML_Cli_Dedu = Storage_Policy_Root.find('storagePolicyCopyInfo/dedupeFlags/enableClientSideDedup')
        XML_Cli_Dedu.text =  Sto_Pol_Lis_Val["client_dedu"]
        Storage_Policy_Tree.write('template\\cv_add_storage_policy.xml')
        Xml_File = open("template\\cv_add_storage_policy.xml", 'r')
        Xml_File_Data = Xml_File.read()
        Xml_File.close()
        data_response = requests.post(service + "StoragePolicy", data=Xml_File_Data , headers=headers_xml)

#Tenant_Policy
def Tenant_Policy(Tenant_Policy_Dict):
    for Tenant_Key, Tenant_Val in Tenant_Policy_Dict.items():
        Tenant_Policy_Tree = ET.parse('template\\cv_add_storage_policy_%s.xml'%(Tenant_Key.lower()))
        Tenant_Policy_Root= Tenant_Policy_Tree.getroot()
        XML_Tenant_Name = Tenant_Policy_Root.find('storagePolicyName')
        XML_Tenant_Name.text = Tenant_Val
        XML_GDP_Name_Gold = Tenant_Policy_Root.find('storagePolicyCopyInfo/useGlobalPolicy/storagePolicyName')
        XML_GDP_Name_Gold.text = "GDP_TENANT_" + Basic_Info["CV_DC_Number"]
        Tenant_Policy_Tree.write('template\\cv_add_storage_policy_%s.xml'%(Tenant_Key.lower()))
        Xml_File_Tenant = open('template\\cv_add_storage_policy_%s.xml'%(Tenant_Key.lower()), 'r')
        Xml_File_Tenant_Data = Xml_File_Tenant.read()
        Xml_File_Tenant.close()
        Data_Response_Tenant = requests.post(service + "StoragePolicy", data=Xml_File_Tenant_Data, headers=headers_xml)


#Add SubClient
def Modify_SC_Info(SubClient):
    if isinstance(SubClient,dict):
        for SubClient_Key, SubClient_Val in SubClient.items():
            if SubClient_Key == "subClientEntity":
                SubClient_Val["clientName"] = Basic_Info["CV_Client_Infra_Name"]
            elif SubClient_Key == "dataBackupStoragePolicy":
                SubClient_Val["storagePolicyName"] = "SP_INFRA_" + Basic_Info["CV_DC_Number"]
            elif isinstance(SubClient_Val,dict):
                Modify_SC_Info(SubClient[SubClient_Key])

    return SubClient

# Add SubClient
def AddSubClient(SubClient_Info):
    if Basic_Info["CV_DC_Role"] == "standard":
        SubClient_LIST = ["StagingArea"]
    else:
        SubClient_LIST = ["ECM","CLMP","StagingArea"]

    for SubClient_LIST_Val in SubClient_LIST:
        SC_Act = json.dumps(SubClient_Info[SubClient_LIST_Val])
        SC_Res = json.loads(requests.post(service + "Subclient", data=SC_Act, headers=headers_json).text)

    return SubClient_LIST


#Select SchedulePolicy
def SchedulePolicy(SchedPolicy_Infra_Dict, SchedPolicy_Tenant_Dict):
    ScPol = json.loads(requests.get(service + "SchedulePolicy" , headers=headers_json).text)
    ScPol_Lis = [Val["task"]["taskName"] for Val in ScPol["taskDetail"] if not re.findall("system|gold|bronze|silver",Val["task"]["taskName"].lower())]

    if len(ScPol_Lis) > 0:

        # "Put method"

        SchedPolicy_Modify["taskInfo"]["associations"][0]["clientName"] = Basic_Info["CV_Client_Infra_Name"]
        for ScPol_Val in ScPol_Lis:
            SchedPolicy_Modify["taskInfo"]["task"]["task"]["taskName"] = ScPol_Val
            SchedPolicy_Modify["taskInfo"]["associations"][0]["subclientName"] = "SC_"+ScPol_Val.replace("Sched_","")
            if "stag" in ScPol_Val.lower():
                SchedPolicy_Modify["taskInfo"]["associations"][0]["subclientName"] = "SC_STAGING_AREA"
            SubCli_PUT_Act = json.dumps(SchedPolicy_Modify)
            SubCli_PUT_Res = json.loads(
                requests.put(service + "Task", data=SubCli_PUT_Act, headers=headers_json).text)

    else:

        # "Post method"

        for Infra_Key, Infra_Val in SchedPolicy_Infra_Dict.items():
            if Basic_Info["CV_DC_Type"].lower() == "prod":
                Infra_Val["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["backupLevel"] = 4
            else:
                Infra_Val["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["backupLevel"] = 1

            Infra_Val["taskInfo"]["associations"][0]["clientName"] = Basic_Info["CV_Client_Infra_Name"]
            SubCli_POST_Infra = json.dumps(Infra_Val)
            Infra_Res = json.loads(
                requests.post(service + "Task", data=SubCli_POST_Infra , headers=headers_json).text)
            print Infra_Res

        for Tenant_Key, Tenant_Val in SchedPolicy_Tenant_Dict.items():

            if "prod" in Basic_Info["CV_DC_Type"].lower() :
                Tenant_Val["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["backupLevel"] = 4
            else:
                Tenant_Val["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["backupLevel"] = 1
                Tenant_Val["taskInfo"]["subTasks"][0]["subTask"]["subTaskName"] = "Full"

            SubCli_POST_Tenant = json.dumps(Tenant_Val)
            Tenant_Res = json.loads(
                requests.post(service + "Task", data=SubCli_POST_Tenant , headers=headers_json).text)

            print Tenant_Res

if __name__ == '__main__':

    '''Check Commvault Socket'''

    Check_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Check_Socket.settimeout(3)
    try:
        Check_Socket.connect((Basic_Info["CV_CommCell_Address"],81))
        print "=====>>> Port:81 is working now"
        Check_Socket.close()
    except:
        print "=====>>> Cant't connect to Commvault Server"
        sys.exit()

    #Login & Get token
    headers_json, headers_xml = GetToken()

    #get usename from cv_add_user.py'
    Add_Commvault_User=[User_Val["userEntity"]["userName"] for User_Val in UserInfo_Add["users"] ]


    # Insert User , if CV_DC_Number is DC1 then create user ,else don't create it
    if Basic_Info["CV_DC_Number"] == "DC1":
        InsertUser_Act = json.dumps(UserInfo_Add)
        InsertUser_Res = json.loads(requests.post(service + "User", data=InsertUser_Act, headers=headers_json).text)

    #Select User
    '''headers_json['Authtoken'] = 'asdasdfasdf'''
    ShowUser()


    #Get MediaAgent_ID
    Get_MediaAgent_ID = MediaAgent()
    print "=====>>> Got the MediaAgent ID, Value is : %s"%(Get_MediaAgent_ID)


    #Add Disk Library for MediaAgent
    Library = {"Drive_G":["G:\\VOL_LIB_INFRA","DISKLIB_INFRA"],"Drive_H":["H:\\VOL_LIB_TENANT","DISKLIB_TENANT"]}
    if Basic_Info["CV_Client_Tenant_Name"].strip() == "":
        Library = {"Drive_G":["G:\\VOL_LIB_INFRA","DISKLIB_INFRA"]}
    Library_ID = AddDiskLibrary(Library)


    #AddDeduplicationPolicy
    Add_Dedu_Policy(AddDeduplicationPolicy)

    # #AddStoragePolicy
    Storage_Policy_Dict = {"sp_name": "SP_INFRA_" + Basic_Info["CV_DC_Number"],
                         "gsp_name":"GDP_INFRA_"+ Basic_Info["CV_DC_Number"],
                         "client_dedu":"0"}
    Storage_Policy_List = []
    Storage_Policy_List.append(Storage_Policy_Dict)
    if Basic_Info["CV_Client_Tenant_Name"].strip() != "":
        Storage_Policy_Dict = {"sp_name": "SP_TENANT_" + Basic_Info["CV_DC_Number"],
                           "gsp_name": "GDP_TENANT_" + Basic_Info["CV_DC_Number"],
                           "client_dedu": "1"}
        Storage_Policy_List.append(Storage_Policy_Dict)

    Add_Storage_Policy(Storage_Policy_List)

    # AddTenant_Policy[Gold & Silver & Bronze]
    if Basic_Info["CV_Client_Tenant_Name"].strip() != "":
        Tenant_Policy_Dict = {"GOLD":"SP_SHARED_" + Basic_Info["CV_DC_Number"] + "_GOLD",
                     "SILVER":"SP_SHARED_" + Basic_Info["CV_DC_Number"] + "_SILVER",
                     "BRONZE": "SP_SHARED_" + Basic_Info["CV_DC_Number"] + "_BRONZE"}
        Tenant_Policy(Tenant_Policy_Dict)

    #add subclient
    SubClient_Info = Modify_SC_Info(SubClient)
    SubClient_LIST = AddSubClient(SubClient_Info)

    #Add SchedulePolicy
    SchedPolicy_Infra_Dict = {
      "ECM":SchedPolicy_ECM,
      "CLMP":SchedPolicy_CLMP,
      "StagingArea":SchedPolicy_STAGING
    }

    SchedPolicy_Tenant_Dict = {
      "GOLD": SchedPolicy_GOLD,
      "SILVER": SchedPolicy_SILVER,
      "BRONZE": SchedPolicy_BRONZE
    }
    SchedulePolicy(SchedPolicy_Infra_Dict, SchedPolicy_Tenant_Dict)


