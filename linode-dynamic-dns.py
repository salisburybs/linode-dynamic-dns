from __future__ import print_function
from linode import api as linode_api
import requests

## Quick script thrown together for Linode Dynamic DNS with python
## Bryan Salisbury

ip_url = 'http://icanhazip.com/'

#name of dns zone in Linode Manager
domain_zone    = 'fullzonename.com'

#should match hostname for zone resource. Could be empty.
resource_name  = 'subdomain'

apikey = '...linode..api..key...'

req = requests.get(ip_url)
req.raise_for_status()
local_ip = req.text

api = linode_api.Api(apikey)
for d in api.domain_list():
    if d['DOMAIN'] == domain_zone:
        res_list = api.domain_resource_list(DomainID=d['DOMAINID'])
        for r in res_list:
            if r['NAME'] == resource_name:
                res_id = r['RESOURCEID']
                if r['TARGET'] != local_ip:
                    api.domain_resource_update(DomainID=d['DOMAINID'],
                        ResourceID=res_id,Target=local_ip)
                    print('updated resource')
                else:
                    print('no changes required')
                break
        break
        
