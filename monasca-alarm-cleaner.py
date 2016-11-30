#!/usr/bin/env python

'''
    Simple script for cleaning up monasca alarms left after removed/destroyed VMs.
'''
import sys
import logging
import argparse

from MonascaCleaner.MonascaCleaner import MonascaCleaner

log = logging.getLogger(__name__)

def main():
    '''
        Cleanup Monasca lefover alarms.
    '''

    parser = argparse.ArgumentParser(description='Monasca Alarm Cleaner program')

    parser.add_argument('-d', action="store_true", dest="debug_flag", default=False,
                        help='Enable debug output.')
    parser.add_argument('-v', action="store_true", dest="verbose_flag", default=False,
                        help='Enable verbose output.')
    parser.add_argument('-a', action="store_true", dest="alarm_list_flag", default=False,
                        help='List existing alarms in undetermined state.')
    parser.add_argument('-C', action="store", dest="cloud_name", required=True,
                        help='os_client_config cloud definition name like: cloud_v3_api')
    parser.add_argument('-U', action="store", dest="monasca_base_url", required=True,
                        help='Monasca api base URL like: http://monasca-api-1:8070')
    parser.add_argument('-A', action="store", dest="api_version", default='2_0',
                        help='Monasca api version definition.')

    args = parser.parse_args()

    monasca_url = '{}/v{}'.format(args.monasca_base_url, args.api_version.replace('_', '.'))

    mon = MonascaCleaner(args.cloud_name, args.api_version,
                         monasca_url, args.verbose_flag, args.debug_flag)

    if args.alarm_list_flag:
        if args.debug_flag:
            log.debug("List all alarms defined in monasca")
            print(mon.client.alarms.list())
            sys.exit(0)
        else:
            log.info("List all alarms in undetermined state")
            print(mon.list_vm_undetermined_alarms())
            sys.exit(0)
    else:
        log.info("Cleaning alarms: ")
        mon.clean_alarms()

if __name__ == '__main__':
    main()
