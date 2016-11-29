'''
    Simple script for cleaning up monasca alarms left after removed/destroyed VMs.
'''
import logging

from MonascaCleaner.MonascaCleaner import MonascaCleaner

log = logging.getLogger(__name__)

VERBOSE = True
DEBUG = False
CLOUD_NAME = 'cloud_v3_api'
API_VERSION = '2_0'
MONASCA_URL = 'http://monasca-api-1:8070/v{}'.format(API_VERSION.replace('_', '.'))

def main():
    '''
        Cleanup Monasca lefover alarms.
    '''
    mon = MonascaCleaner(CLOUD_NAME, API_VERSION, MONASCA_URL, VERBOSE, DEBUG)

    log.info("Cleaning alarms: ")
    #print mon.client.alarms.list()
    mon.clean_alarms()

if __name__ == '__main__':
    main()
