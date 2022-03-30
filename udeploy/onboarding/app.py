import connect
import cmd
import sys
import json
from pprint import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

props = dict(line.strip().split('=') for line in open('env.properties'))

## uDeploy Connection Params
url=props['udeploy.url']
user=props['udeploy.username']
token=props['udeploy.token']

## Application Params
# appName=props['application.name']
# appPort=props['application.port']
# junction=props['application.junction']
# userName=props['application.username']
# userPasswd=props['application.userpass']

# Disable insecure SSL Warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def create_ms_component(appName):
    # Create a new component based on above params
    new_component_template= {
                        "name": appName,
                        "description": appName,
                        "templateId": "c486d066-e9ac-4ebe-8ddd-c6a310d5bcb7",
                        "templateVersion": "",
                        "componentType": "STANDARD",
                        "sourceConfigPlugin": "",
                        "importAutomatically": "false",
                        "useVfs": "true",
                        "defaultVersionType": "FULL",
                        "importAgentType": "inherit",
                        "inheritSystemCleanup": "true",
                        "runVersionCreationProcess": "false",
                        "properties": {},
                        "importProperties": {
                        "properties": {}
                            },
                        "teamMappings": [{
                        "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                            }]
                        }

    head = {'Content-type':'application/json',
            'Accept':'application/json'
           }

    ud=connect.udeploy(url,user,token)
    res=ud.uput('/cli/component/create',new_component_template,head)
    if res.status_code != 200:
        print ("[ERROR] Some error occured while creating the new Component {0}".format(appName))
        print (res.text)
        return False
    else:
        print ("[INFO] New Component {0} Created Successfully".format(appName))
        create_component_json_response=json.loads(res.text)
        component_id=create_component_json_response['id']
        return component_id

def attach_ms_tag_to_component(component_id):
    head = {
            'Content-type':'application/json',
            'Accept':'application/json'
           }

    tag_template = {
                    "ids": ["{0}".format(component_id)],
                    "name": "UOAPI"
    }
    uri='/rest/tag/Component'
    furl = url + uri
    payld = json.dumps(tag_template)
    res=requests.put(furl,auth=(user,token),headers=head,data=payld,verify=False)
    if res.status_code != 204:
        print ("[ERROR] Some error occured while adding tag to the new Component {0}".format(appName))
        return False
    else:
        print ("[INFO] Tag added Successfully to component {0}".format(appName))
        return True

def create_ms_application(appName,component_id):
    new_application_template={
                                "application": {
                                "name": "{0}".format(appName),
                                "description": "",
                                "templateId": "47756720-784b-4afc-bfb3-eca69ffb8fb3",
                                "templateVersion": "",
                                "notificationSchemeId": "bdd39b45-4695-4f4e-a177-ed6899ec42e4",
                                "enforceCompleteSnapshots": "False",
                                "teamMappings": [{
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }]
                            },
                            "components": {
                                "existingComponents": ["{0}".format(component_id)],
                                "newComponents": []
                            },
                            "environments": [{
                                "name": "DEV",
                                "templateId": "744c69de-baab-4783-a824-53228fa8ab16",
                                "templateVersion": 39,
                                "description": "",
                                "requireApprovals": False,
                                "noSelfApprovals": False,
                                "exemptProcesses": "",
                                "lockSnapshots": False,
                                "color": "#008ABF",
                                "teamMappings": [{
                                    "resourceRoleId": "b6832d84-9707-42de-acf4-a8cb8fe1592c",
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }],
                                "resources": []
                            }, {
                                "name": "QA",
                                "templateId": "93ea3d2f-c781-43d2-8600-8133cfd6030e",
                                "templateVersion": 54,
                                "description": "",
                                "requireApprovals": True,
                                "noSelfApprovals": True,
                                "exemptProcesses": "",
                                "lockSnapshots": False,
                                "color": "#00B2EF",
                                "teamMappings": [{
                                    "resourceRoleId": "8766d5bf-dad2-4ebc-9bfa-7de0cd80336c",
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }],
                                "resources": []
                            }, {
                                "name": "STG",
                                "templateId": "86ecdcbd-42e7-49d1-a974-8fc3fefd8242",
                                "templateVersion": 51,
                                "description": "",
                                "requireApprovals": False,
                                "noSelfApprovals": False,
                                "exemptProcesses": "",
                                "lockSnapshots": False,
                                "color": "#FDB813",
                                "teamMappings": [{
                                    "resourceRoleId": "f2495cb1-2dea-46cf-9b99-eddf98a73196",
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }],
                                "resources": []
                            }, {
                                "name": "STG02",
                                "templateId": "abc39bbf-26c5-44dc-9ee3-a3fe4871aaaa",
                                "templateVersion": 37,
                                "description": "",
                                "requireApprovals": False,
                                "noSelfApprovals": False,
                                "exemptProcesses": "",
                                "lockSnapshots": False,
                                "color": "#00B2EF",
                                "teamMappings": [{
                                    "resourceRoleId": "f0e8ab92-f896-4fd9-ad36-5c2c25928385",
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }],
                                "resources": []
                            }, {
                                "name": "UAT",
                                "templateId": "aa7c9bfa-e04d-4c52-b280-7045b4057518",
                                "templateVersion": 51,
                                "description": "",
                                "requireApprovals": True,
                                "noSelfApprovals": True,
                                "exemptProcesses": "",
                                "lockSnapshots": False,
                                "color": "#17AF4B",
                                "teamMappings": [{
                                    "resourceRoleId": "96dc0a13-e591-449b-aeff-21f3cdf9e7a5",
                                    "teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                                }],
                                "resources": []
                            }, {
		                        "name": "Digital",
		                        "templateId": "16b6fe9c-a4c3-97e6-318d-b8353ec75d82",
		                        "templateVersion": 10,
                        		"description": "",
                        		"requireApprovals": False,
                        		"noSelfApprovals": False,
                        		"exemptProcesses": "",
                        		"lockSnapshots": False,
                        		"color": "#008A52",
                        		"teamMappings": [{
                        			"resourceRoleId": "e59461b9-1af8-4e6e-9cf7-ce94db8feb1d",
                        			"teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                        		}],
                        		"resources": []
                        	}, {
                        		"name": "Parks and Resorts",
                        		"templateId": "16f1562f-6983-5902-edda-66946dc30e49",
                        		"templateVersion": 8,
                        		"description": "",
                        		"requireApprovals": False,
                        		"noSelfApprovals": False,
                        		"exemptProcesses": "",
                        		"lockSnapshots": False,
                        		"color": "#594F13",
                        		"teamMappings": [{
                        			"resourceRoleId": "f839969c-efa0-4995-8920-d75ce131b271",
                        			"teamId": "ce08f0fc-b2e7-4df9-b713-f787d04be999"
                        		}],
                        		"resources": []
                        	}]
    }
    head = {
            'Content-type':'application/json',
            'Accept':'application/json'
           }
    ud=connect.udeploy(url,user,token)
    res=ud.uput('/rest/deploy/application/createFromWizard',new_application_template,head)
    if res.status_code != 200:
        print ("[ERROR] Some error occured while creating the new Application {0}".format(appName))
        print (res.text)
    else:
        print ("[INFO] New Application {0} Created Successfully".format(appName))
    #     print (res.text)

def add_component_properties(appName,appPort,junction,userName,userPasswd):
    print ("[INFO] Now at this time, adding component properties to newly created Component in uDeploy")
    # print ("appPort={0}".format(appPort))
    # print ("junction={0}".format(junction))
    # print ("userName={0}".format(userName))
    # print ("userPasswd={0}".format(userPasswd))

    head = {'Content-type':'application/json',
            'Accept':'application/json'
           }

    prop='/cli/component/propValue?name=appPort&value={0}&component={1}&isSecure=false'.format(appPort,appName)
    furl = url + prop
    res=requests.put(furl,auth=(user,token),headers=head,verify=False)

    prop='/cli/component/propValue?name=junction&value={0}&component={1}&isSecure=false'.format(junction,appName)
    furl = url + prop
    res=requests.put(furl,auth=(user,token),headers=head,verify=False)

    prop='/cli/component/propValue?name=userName&value={0}&component={1}&isSecure=false'.format(userName,appName)
    furl = url + prop
    res=requests.put(furl,auth=(user,token),headers=head,verify=False)

    prop='/cli/component/propValue?name=userPasswd&value={0}&component={1}&isSecure=false'.format(userPasswd,appName)
    furl = url + prop
    res=requests.put(furl,auth=(user,token),headers=head,verify=False)

def add_agents_to_dev(appName,dev_agents):
    # appName="ms-test"
    print ("[INFO] Adding agents to dev")

    head = {'Content-type':'application/json',
            'Accept':'application/json'
           }
    # Get base path of the resources
    prop='/cli/environment/getBaseResources?environment=DEV&application={0}'.format(appName)
    furl = url + prop
    res=requests.get(furl,auth=(user,token),headers=head,verify=False)
    resource_path_json_response=json.loads(res.text)
    resource_path=resource_path_json_response[0]['path']
    print (resource_path)

    # prop='/cli/environment/addBaseResource?application={0}&environment=DEV&resource={1}/{2}'.format(appName,resource_path,dev_agents)
    prop='/cli/environment/addBaseResource?application={0}&environment=DEV&resource={1}'.format(appName,dev_agents)
    furl = url + prop
    res=requests.put(furl,auth=(user,token),headers=head,verify=False)
    print (res.text)
    print (res.status_code)

if __name__ == "__main__":

    print ("******************uDeploy Onboarding - Microservices******************")
    appName=input("Enter the name of the application : ")
    appPort=input("What port does it run on : ")
    junction=input("what's the name of the junction : ")
    userName=input("what's gonna be the linux level username for this app : ")
    userPasswd=input("Enter the password for the above user : ")

    print ("[INFO] Kicking off onboarding")
    component_id=create_ms_component(appName)
    if component_id:
        tag_status=attach_ms_tag_to_component(component_id)
        if tag_status:
            create_ms_application(appName,component_id)
        else:
            print ("[ERROR] Some error occureed while adding tag to component.")
            sys.exit()
    else:
        print ("[ERROR] Some error occureed while creating components.")
        sys.exit()

    add_component_properties(appName,appPort,junction,userName,userPasswd)
    # add_agents_to_dev(appName,"e30473ad-d03c-4d15-a880-402883399ab7")
    # add_agents_to_dev("f7d36939-5ff0-4d4d-89d8-96f6e3328ac9")
    print ("***********************************************************************")
