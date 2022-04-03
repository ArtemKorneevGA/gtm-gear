import json, copy, os

from googleapiclient.http import HttpMock
from googleapiclient.http import RequestMockBuilder, HttpRequestMock

from apiclient.discovery import build

from gtm_gear.service import Service
from gtm_gear.container import Container
from gtm_gear.workspace import Workspace


from helpers.request_config import *
from helpers.request_mock import RequestMockCreateBuilder, getEntityIdLabel


def get_dict(path): 
    with open(path) as json_file:
        return json.load(json_file)

def datafile(filename):
    return os.path.join('./', filename)

def get_mock_workspace(path):
    export_json = get_dict(path)
    requestBuilder = prepare_request_builder(export_json)
    http = HttpMock(datafile("./data/container.json"), {"status": "200"})
    mock_service = Service(None,'',http, requestBuilder)
    source_container = Container(mock_service, export_json['containerVersion']["container"]["accountId"], export_json['containerVersion']["container"]["publicId"], False)
    return Workspace(source_container, 'Default Workspace', False)


def prepare_request_builder(export_json):
    # Prepare workspace
    workspace = dict(export_json['containerVersion']["container"])
    workspaceId = 1
    workspace["workspaceId"] = workspaceId
    workspace["name"] = 'Default Workspace'
    workspace['path'] = f'accounts/{workspace["accountId"]}/containers/{workspace["containerId"]}/workspaces/{workspace["workspaceId"]}'
    del workspace["usageContext"]
    del workspace["publicId"]
    workspace['tagManagerUrl'] = f'https://tagmanager.google.com/#/container/accounts/{workspace["accountId"]}/containers/{workspace["containerId"]}/workspaces/{workspace["workspaceId"]}?apiLink=workspace'

    # Prepare workspace and container rout 
    request_dict = {
            "tagmanager.accounts.containers.list": 
            (None, json.dumps({"container":[dict(export_json['containerVersion']["container"])]})),
            "tagmanager.accounts.containers.workspaces.list": 
            (None, json.dumps({"workspace":[workspace]})),

        }
    # Prepare routs for all default entities
    for key in list(ENTITY_CONFIG.keys()):
        entities = []
        importKeyName="key"
        if "importKey" in ENTITY_CONFIG[key].keys():
            importKeyName = "importKey"

        if ENTITY_CONFIG[key][importKeyName] in export_json['containerVersion'].keys():
            entities =copy.deepcopy(export_json['containerVersion'][ENTITY_CONFIG[key][importKeyName]])
            for entity in entities:
                if key == 'built_in_variables':
                    entity["path"] = f'accounts/{workspace["accountId"]}/containers/{workspace["containerId"]}/workspaces/{workspaceId}/built_in_variables'
                else:
                    entityType = getEntityIdLabel(key)
                    entity["path"] = f'accounts/{workspace["accountId"]}/containers/{workspace["containerId"]}/workspaces/{workspaceId}/{key}/{entity[entityType]}'

        request_dict[f"tagmanager.accounts.containers.workspaces.{key}.list"] = (None, json.dumps({ENTITY_CONFIG[key]["key"]: entities}))
    
    # Get requestBuilder
    requestBuilder = RequestMockCreateBuilder(
        request_dict, export_json
    )
    return requestBuilder
