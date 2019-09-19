import config
from tfs_requests import tfs_request
from request_utils import create_csv
import logging




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


startTime = '2018-04-01T00:00:00' 
endTime = '2019-03-31T00:00:00'
logger.info('Starting release audit with the following dates, Start Date : {0} , End Date : {1}' .format(startTime, endTime))
tfs_object = tfs_request(config.tfs_endpoint, config.tfs_port, config.tfs_token)

response = tfs_object.get_releases(config.tfs_collection, config.tfs_project_id, startTime, endTime)


generated_data = tfs_object.generate_release_data(response, config)

create_csv(generated_data, 'test.csv')
print('pause')
