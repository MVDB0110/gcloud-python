networkName = "mongo"
project = "mongodb-276412"
clusters = ["mongo1", "mongo2"]
zones = ["europe-west4-a", "europe-west4-b", "europe-west4-c"]
machineType = "n1-standard-1"

def GenerateConfig(context):
    """Creates the Compute Engine with network and firewall."""

    resources = [{
        "name": networkName,
        "type": "network.py"
    }, {
        "name": networkName+'-allow',
        "type": "ssh.py",
        "properties": {
            "network": networkName
        }
    }]

    for cluster in clusters:
        for zone in zones:
            compute = {
                "name": str(cluster+'-'+zone.split('-')[2]).lower(),
                "type": "instance.py",
                "project": project,
                "properties": {
                    "machineType": machineType,
                    "zone": zone,
                    "network": networkName
                }
            }
            resources.append(compute)
    
    return { "resources": resources }
