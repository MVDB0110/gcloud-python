networkName = "test"
project = "mongodb-276412"

def GenerateConfig(context):
    """Creates the Compute Engine with network and firewall."""

    resources = [{
        "name": "vm",
        "type": "instance.py",
        "project": project,
        "properties": {
            "machineType": "n1-standard-1",
            "zone": "europe-west4-a",
            "name": "test",
            "network": networkName
        }
    }, {
        "name": networkName,
        "type": "network.py"
    }, {
        "name": networkName + "-firewall",
        "type": "firewall.py",
        "properties": {
            "network": networkName
        }
    }]
    return { "resources": resources }
