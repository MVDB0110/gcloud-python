def GenerateConfig(context):
    """Creates the subnetwork."""
    settings = context.properties
    requiredSettings = ['network', 'ipCidrRange', 'region', 
        'enableFlowLogs', 'privateIpGoogleAccess']

    properties = {p: settings[p] for p in requiredSettings}
    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.subnetworks',
        'properties': properties
    }]

    return {'resources': resources}