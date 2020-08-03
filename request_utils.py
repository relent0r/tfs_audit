import csv
import logging
import os

logger = logging.getLogger(__name__)

def create_csv(list, filename):
    with open (filename, 'w', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Data', 'Release Name', 'Environment', 'CRQ'])
        for l in list:
            filewriter.writerow(l)

    filepath = os.path.abspath(filename)
    return logger.info('CSV File Written : {}' .format(filepath))