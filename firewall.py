def GenerateConfig(context):
  """Creates the firewall."""

  resources = [{
      'name': context.env['name']+'-ssh',
      'type': 'compute.v1.firewall',
      'properties': {
          'network': '$(ref.' + context.properties['network'] + '.selfLink)',
          'sourceRanges': context.properties['cidr'],
          'allowed': [{
              'IPProtocol': context.properties['protocol'],
              'ports': context.properties['port']
          }]
      }
  }]
  return {'resources': resources}
