networkName = "mongo"
project = "mongodb-276412"
clusters = ["data-router", "config-set", "data-set-1"]
zones = ["europe-west4-a", "europe-west4-b", "europe-west4-c"]
machineType = "n1-standard-1"

def GenerateConfig(context):
    """Creates the Compute Engine with network and firewall."""

    resources = [{
        "name": networkName,
        "type": "network.py"
    }, {
        "name": "routers",
        "type": "subnet.py",
        "properties": {
            "network": "$(ref." + networkName + ".selfLink)",
            "ipCidrRange": "10.0.0.0/23",
            "region": "europe-west4",
            "enableFlowLogs": False,
            "privateIpGoogleAccess": True
        }
    }, {
        "name": "config",
        "type": "subnet.py",
        "properties": {
            "network": "$(ref." + networkName + ".selfLink)",
            "ipCidrRange": "10.0.2.0/23",
            "region": "europe-west4",
            "enableFlowLogs": False,
            "privateIpGoogleAccess": False
        }
    }, {
        "name": "data",
        "type": "subnet.py",
        "properties": {
            "network": "$(ref." + networkName + ".selfLink)",
            "ipCidrRange": "10.0.4.0/23",
            "region": "europe-west4",
            "enableFlowLogs": False,
            "privateIpGoogleAccess": False
        }
    }, {
        "name": networkName+'-allow-db',
        "type": "firewall.py",
        "properties": {
            "network": networkName,
            "port": [27017],
            "protocol": 'TCP',
            "cidr": ['0.0.0.0/0']
        }
    }, {
        "name": networkName+'-allow-ssh',
        "type": "firewall.py",
        "properties": {
            "network": networkName,
            "port": [22],
            "protocol": 'TCP',
            "cidr": ['0.0.0.0/0']
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
                    "network": networkName,
                    "subNetwork": "data"
                }
            }
            resources.append(compute)
    
    return { "resources": resources }
