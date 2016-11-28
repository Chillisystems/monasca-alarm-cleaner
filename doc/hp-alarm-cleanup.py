#!/usr/bin/python

import os
import sys

import MySQLdb

import os_client_config
import shade

OS_VARS = ['OS_REGION_NAME',
           'OS_USERNAME',
           'OS_PASSWORD',
           'OS_TENANT_NAME',
           'OS_AUTH_URL']

DELETE_SQL = """
    DELETE a FROM alarm a WHERE a.id IN (%s); COMMIT;
"""

GET_SQL = """
    SELECT
      a.id AS alarm_id,
      mdg.dimensions AS metric_dimensions
    FROM alarm AS a
    INNER JOIN alarm_definition ad
      ON ad.id = a.alarm_definition_id
    INNER JOIN alarm_metric AS am
      ON am.alarm_id = a.id
    INNER JOIN metric_definition_dimensions AS mdd
      ON mdd.id = am.metric_definition_dimensions_id
    INNER JOIN metric_definition AS md
      ON md.id = mdd.metric_definition_id
    LEFT OUTER JOIN (SELECT
      dimension_set_id,
      name,
      value,
      group_concat(name, '=', value) AS dimensions
    FROM metric_dimension
    GROUP BY dimension_set_id) AS mdg
      ON mdg.dimension_set_id = mdd.metric_dimension_set_id
    WHERE ad.deleted_at IS NULL
    AND a.state = 'UNDETERMINED'
    AND mdg.dimensions LIKE '%component=vm%'
    AND mdg.dimensions LIKE '%region={}%'
    ORDER BY a.id;
"""

def get_cloud():
#    client_config = os_client_config.OpenStackConfig(cloud='cloud_v3_api')
#    cloud_config = client_config.get_one_cloud()
    return shade.OpenStackCloud(cloud='cloud_v3_api')


def prune_alarms(active_vm_ids):

    db = MySQLdb.connect(user='monasca',
                         passwd='monasca',
                         host='monasca-backend-1',
                         port=3306,
                         db='monasca')

    try:
        db_conn = db.cursor()
        db_conn.execute(GET_SQL.format('RegionOne'))

        alarms = {}
        for (alarm_id, dims) in db_conn:
            dim_dict = dict(s.split('=') for s in dims.split(','))
            if 'resource_id' in dim_dict.keys():
                alarms[alarm_id] = dim_dict['resource_id']

        alarm_ids_to_delete = []
        for (alarm_id, resource_id) in alarms.iteritems():
            if resource_id not in active_vm_ids:
                alarm_ids_to_delete.append(alarm_id)
                print "Deleting alarm id '%s' for deleted vm '%s'" % \
                      (alarm_id, resource_id)

        print(alarm_ids_to_delete)
        if len(alarm_ids_to_delete) > 0:
            db_conn.execute(DELETE_SQL % str(alarm_ids_to_delete).strip('[]'))

    finally:
        db_conn.close()
        db.close()


def main():
    cloud = get_cloud()
    servers = cloud.nova_client.servers.list(search_opts={'all_tenants': 1},
                                             limit=-1)
    prune_alarms(list(server.id for server in servers))

if __name__ == '__main__':
    main()