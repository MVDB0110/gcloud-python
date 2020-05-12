computeBaseUrl = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Creates the second virtual machine."""

    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join([computeBaseUrl, 
                                    'projects/', context.env['project'],
                                    '/zones/', context.properties['zone'], 
                                    '/machineTypes/', context.properties['machineType']]),
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': ''.join([computeBaseUrl, 'projects/',
                                            'ubuntu-os-cloud/global',
                                            '/images/family/ubuntu-2004-lts'])
                }
            }],
            'networkInterfaces': [{
                'network': '$(ref.' + context.properties['network'] + '.selfLink)',
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }],
            # Allow the instance to access logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],
            # Metadata
            'metadata': {
                'items': [{
                    # Startup script
                    'key': 'startup-script',
                    'value': ''.join(['#!/bin/bash\n', 'echo "test" >> /test.txt'])
                }]
            }
        }
    }]

    return {'resources': resources}
