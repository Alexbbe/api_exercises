import requests
import json
from pprint import pprint

url = 'https://wger.de/en/user/login'
# url2 = 'https://wger.de/api/v2/day/'
# url3 = "https://wger.de/en/user/api-key"
# data = {"username": "balbaealexandru@gmail.com","password":"12345678abc","submit":"Login"}
# headers = {  'Accept': 'application/json',
#              'X-CSRFToken':'7UtujyPkrhtmFshrMyKuxGhDDKcGeFIb5WYqANXy595WBnPHrDkkbokILBRy3FLo',
#              'Referer':'https://wger.de/en/user/login',
#              'Cookie':'csrftoken=7UtujyPkrhtmFshrMyKuxGhDDKcGeFIb5WYqANXy595WBnPHrDkkbokILBRy3FLo; sessionid=lzbuadede20y8w2lz7yh3ef5iott5cm2'}

# r = requests.post(url=url, data=data, headers=headers)
# g = requests.get(url=url2,headers=headers)
r1 = requests.get(url=url)

g1 = requests.get('https://wger.de/api/v2/')
print(g1.json()['day'])
# print(r)
# print(r.content)
# print(g)
# print(json.loads(g.content))

print(r1.content)
# pprint(json.loads(r1.headers))
pprint(r1.cookies)
