def GenerateConfig(context):
  """Creates the firewall."""

  resources = [{
      'name': context.env['name'],
      'type': 'compute.v1.firewall',
      'properties': {
          'network': '$(ref.' + context.properties['network'] + '.selfLink)',
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
              'IPProtocol': 'TCP',
              'ports': [22]
          }]
      }
  }]
  return {'resources': resources}
