import argparse
import os
import time
import googleapiclient.discovery
from six.moves import input


def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def create_instance(compute, project, zone, name):
    # Get the latest Ubuntu Focal Fossa image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2004-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startupScripts/' + name), 'r').read()

    config = {
        'name': name+'-'+zone,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()


def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)


def main(project, zones, instance_name, wait=True):
    compute = googleapiclient.discovery.build('compute', 'v1')
    for zone in zones:
        print('Zone:',zone)
        print('Creating instance.')

        operation = create_instance(compute, project, zone, instance_name)
        wait_for_operation(compute, project, zone, operation['name'])

        instances = list_instances(compute, project, zone)

        print('Instances in project %s and zone %s:' % (project, zone))
        for instance in instances:
            print(' - ' + instance['name'])

        #operation = delete_instance(compute, project, zone, instance_name)
        #wait_for_operation(compute, project, zone, operation['name'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Arguments for single compute instance creation.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--zone',
        default='europe-west4',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        'hostname', help='New instance name.')

    args = parser.parse_args()
    zones = []
    for zone in ['a','b','c']:
        zones.append(args.zone+'-'+zone)
    main("mongodb-276412", zones, args.hostname)
