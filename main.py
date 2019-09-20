import config
from tfs_requests import tfs_request
from request_utils import create_csv
import logging




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_release_audit():
    '''
    Create a CSV file that contains the release audit
    '''
    logger.info('Starting release audit with the following dates, Start Date : {0} , End Date : {1}' .format(config.startTime, config.endTime))
    tfs_object = tfs_request(config.tfs_endpoint, config.tfs_port, config.tfs_token)
    response = tfs_object.get_releases(config)
    generated_data = tfs_object.generate_release_data(response, config)
    csv_file = create_csv(generated_data, config.csv_file)
    return csv_file

def identities_audit():
    '''
    Create a CSV file with the members of the release administrators groups for production
    '''
    logger.info('Starting release administrator audit for the following project_id : {0}' .format(config.tfs_project_id))
    tfs_object = tfs_request(config.tfs_endpoint, config.tfs_port, config.tfs_token)
    response = tfs_object.get_project_identities(config)
    generated_data = tfs_object.generate_identities_data(response, config)

    return response

perform_release_audit()


