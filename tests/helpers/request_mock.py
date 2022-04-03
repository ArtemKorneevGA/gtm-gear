

import json
import copy

from googleapiclient.model import JsonModel
from googleapiclient.http import HttpMock
from googleapiclient.http import RequestMockBuilder, HttpRequestMock
from googleapiclient.errors import UnexpectedMethodError

from apiclient.discovery import build

from helpers.request_config import *


def getEntityIdLabel(entity_type):
    return f'{ENTITY_CONFIG[entity_type]["key"]}Id'

class RequestMockCreateBuilder(RequestMockBuilder):
    """A simple mock of HttpRequest

    Pass in a dictionary to the constructor that maps request methodIds to
    tuples of (httplib2.Response, content, opt_expected_body) that should be
    returned when that method is called. None may also be passed in for the
    httplib2.Response, in which case a 200 OK response will be generated.
    If an opt_expected_body (str or dict) is provided, it will be compared to
    the body and UnexpectedBodyError will be raised on inequality.

    Example:
      response = '{"data": {"id": "tag:google.c...'
      requestBuilder = RequestMockBuilder(
        {
          'plus.activities.get': (None, response),
        }
      )
      googleapiclient.discovery.build("plus", "v1", requestBuilder=requestBuilder)

    Methods that you do not supply a response for will return a
    200 OK with an empty string as the response content or raise an excpetion
    if check_unexpected is set to True. The methodId is taken from the rpcName
    in the discovery document.

    For more details see the project wiki.
    """

    def __init__(self, responses, export_json):
        """Constructor for RequestMockBuilder

        The constructed object should be a callable object
        that can replace the class HttpResponse.

        responses - A dictionary that maps methodIds into tuples
                    of (httplib2.Response, content). The methodId
                    comes from the 'rpcName' field in the discovery
                    document.
        check_unexpected - A boolean setting whether or not UnexpectedMethodError
                           should be raised on unsupplied method.
        """
        self.responses = responses
        self.export_json = export_json
        self.accountId = export_json['containerVersion']["container"]["accountId"]
        self.containerId = export_json['containerVersion']["container"]["containerId"]
        self.check_unexpected = False
    
    def getEntityType(self, methodId):
        for key in ENTITY_CONFIG.keys():
            if f".{key}." in methodId:
                return key
        raise ValueError

    def getEntityIdLabel(self, entity_type):
        return f'{ENTITY_CONFIG[entity_type]["key"]}Id'

    def getNextEntityId(self, entity_type):
        entity_id = getEntityIdLabel(entity_type)
        ids = [int(e[entity_id]) for e in self.export_json['containerVersion'][ENTITY_CONFIG[entity_type]['key']]]
        max_id = max(ids) + 1
        return max_id

    def addEntity(self, entity_type, entity):
        self.export_json['containerVersion'][ENTITY_CONFIG[entity_type]['key']].append(entity)

    def getBuiltInVariable(self,uri):
        for key in DEFAULT_BUILT_IN_VARIABLES:
            if key in uri:
                return key
        raise ValueError

    def __call__(
        self,
        http,
        postproc,
        uri,
        method="GET",
        body=None,
        headers=None,
        methodId=None,
        resumable=None,
    ):
        """Implements the callable interface that discovery.build() expects
        of requestBuilder, which is to build an object compatible with
        HttpRequest.execute(). See that method for the description of the
        parameters and the expected response.
        """
        if methodId in self.responses:
            response = self.responses[methodId]
            resp, content = response[:2]
            return HttpRequestMock(resp, content, postproc)
        elif "create" in methodId and method == "POST" and "built_in_variables" in methodId:
            entity_type = self.getEntityType(methodId)
            built_in_type = self.getBuiltInVariable(uri)
            content = {}
            content["accountId"] = self.accountId
            content["containerId"] = self.containerId
            content["type"] = DEFAULT_BUILT_IN_VARIABLES[built_in_type]['exportName']
            content["name"] = DEFAULT_BUILT_IN_VARIABLES[built_in_type]['name']

            self.addEntity(entity_type, content)
            return HttpRequestMock(None, "{}", postproc)

        elif "create" in methodId and method == "POST" and "built_in_variables" not in methodId:
            content = json.loads(body)
            entity_type = self.getEntityType(methodId)
            entity_type_id_name = self.getEntityIdLabel(entity_type)
            entity_next_id = self.getNextEntityId(entity_type)
            content["accountId"] = self.accountId
            content["containerId"] = self.containerId
            content[entity_type_id_name] = entity_next_id
            content["path"] = f'accounts/{self.accountId}/containers/{self.containerId}/workspaces/1/{entity_type}/{entity_next_id}'
            self.addEntity(entity_type, content)
            return HttpRequestMock(None, json.dumps(content), postproc)

        elif self.check_unexpected:
            raise UnexpectedMethodError(methodId=methodId)
        else:
            model = JsonModel(False)
            return HttpRequestMock(None, "{}", model.response)

