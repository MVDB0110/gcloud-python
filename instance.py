computeBaseUrl = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Creates the second virtual machine."""

    if context.properties['networkType'] == 'external':
        networkInterfaces = [{
            'subnetwork': context.properties['subNetwork'],
            'accessConfigs': [{
                'name': 'External NAT',
                'type': 'ONE_TO_ONE_NAT'
            }]
        }]
    else:
        networkInterfaces = [{
                'subnetwork': context.properties['subNetwork'],
            }]
    if context.properties['mongoType'] == 'dbData':
        importScript = "mongodata.sh"
    elif context.properties['mongoType'] == 'dbRouter':
        importScript = "mongos.sh"
    elif context.properties['mongoType'] == 'dbConfig':
        if 'a' in context.env['name']:
            networkInterfaces[0]['networkIP'] = '10.0.2.10'
        elif 'b' in context.env['name']:
            networkInterfaces[0]['networkIP'] = '10.0.2.11'
        elif 'c' in context.env['name']:
            networkInterfaces[0]['networkIP'] = '10.0.2.12'
        importScript = "mongoconf.sh"

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
            'networkInterfaces': networkInterfaces,
            # Allow the instance to access logging.
            "serviceAccounts": [
                {
                "email": "208077196965-compute@developer.gserviceaccount.com",
                "scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/trace.append"
                ]
                }
            ],
            # Metadata
            'metadata': {
                'items': [{
                    # Startup script
                    'key': 'startup-script',
                    'value': context.imports[importScript]
                }]
            }
        }
    }]

    return {'resources': resources}
