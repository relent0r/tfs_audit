import requests
from base64 import b64encode
import logging
from json import loads


logger = logging.getLogger(__name__)

class tfs_request():

    def __init__(self, host, port, token):
        self.host = host
        self.port = port
        self.token = token
        self.scheme = 'https'
        self.apiversion = '4.1-preview'
        self.url = '{0}://{1}:{2}'.format(
            self.scheme,
            self.host,
            self.port
        )
        blankuser_token = ':' + token
        self.headers = {
            'Authorization': 'Basic %s' % b64encode(blankuser_token.encode()).decode('ascii')
        }
    
    def convert_json(self, json_object):
        try:
            d = loads(json_object)
        except AttributeError as e:
            logger.warn('Exception is : {0}' .format(e))
            exit()
        return d

    def make_req(self, uri, headers):

        try:
            response = requests.request('GET', uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status()
            elif response.status_code == 200:
                data = response.status_code
                logger.debug(data)
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is {0}' .format(response.status_code))
        return response


    def get_releases(self, config):
        continuation_token = ''
        full_list = []
        contID = True
        headers = self.headers
        uri = self.url + '/' + config.tfs_collection + '/' + config.tfs_project_id + '/_apis/release/deployments?minStartedTime='+ config.startTime + '&maxStartedTime=' \
            + config.endTime +'&query=ascending&api-version=' + self.apiversion
        
        initial_request = self.make_req(uri, headers)
        continuation_token = initial_request.headers['x-ms-continuationtoken']
        full_list.append(initial_request.text)
        while contID is True:
            try:
                if continuation_token:
                    contID = True
                    logger.debug('Continuation ID is true')
                    uri_continuation = self.url + '/' + config.tfs_collection + '/' + config.tfs_project_id + '/_apis/release/deployments?minStartedTime='+ config.startTime + '&maxStartedTime=' \
                        + config.endTime +'&query=ascending' + '&continuationToken=' + continuation_token + '&api-version=' + self.apiversion
                    continuation_request = self.make_req(uri_continuation, headers)
                    full_list.append(continuation_request.text)
                    continuation_token = continuation_request.headers['x-ms-continuationtoken']
            except KeyError:
                contID = False
                logger.debug('Coninuation ID is false')

        return full_list

    def generate_release_data(self, response, config):
        release_list = []
        
        for item in response:
            converted_releases = self.convert_json(item)['value'] 
            #lesson to learn, don't assign a name 'json', it will break after the first iteration. You are changing
            #the module reference to a variable reference
            for json_object in converted_releases:
                for env in config.environments:
                    if json_object['releaseEnvironment']['name'].startswith(env):
                        logger.debug('{0} present in environment list' .format(json_object['releaseEnvironment']['name']))
                        release_item = []
                        release_item.append(json_object['startedOn'])
                        release_item.append(json_object['release']['name'])
                        release_item.append(json_object['releaseEnvironment']['name'])
                        for approval in json_object['preDeployApprovals']:
                            logger.debug(approval['comments'])
                            release_item.append(approval['comments'])
                        release_list.append(release_item)
                    else:
                        logger.debug('{0} not in environment list' .format(json_object['releaseEnvironment']['name']))
                        pass
        return release_list

    def get_project_identities(self, config):

        headers = self.headers
        uri = self.url + '/' + config.tfs_collection + '/_apis/identities?scopeId='+ config.tfs_project_id +'&api-version=' + self.apiversion
        identities = self.make_req(uri, headers)       

        return identities.text

    def generate_identities_data(self, response, config):

        converted_identities = self.convert_json(response)['value']
        for json_object in converted_identities:
            for env in config.groups:
                group_text = json_object['providerDisplayName'].split('\\', 1)[-1]
                if group_text == env:
                    logger.debug(json_object['providerDisplayName'])
                    group_members = json_object['memberIds']
                    for members in group_members:
                        uri = self.url + '/' + config.tfs_collection + '/_apis/identities?scopeId='+ config.tfs_project_id +'&api-version=' + self.apiversion
                        logger.debug(members['DisplayName'])


        
        return 'stuff'

