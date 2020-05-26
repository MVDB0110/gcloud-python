def GenerateConfig(context):
    """Creates the Cloud NAT."""

    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.routers',
        'properties': {
            'network': context.properties['network'],
            'region': context.properties['region'],
            'nats': [{
                'name': context.env['name'] + '-config',
                'sourceSubnetworkIpRangesToNat': 'ALL_SUBNETWORKS_ALL_IP_RANGES',
                "natIpAllocateOption": "AUTO_ONLY"
            }]
        }
    }]

    return {'resources': resources}