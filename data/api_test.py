from pprint import pprint

from requests import get, delete

pprint(get('http://localhost:5000/api/ads/1').json())
pprint(get('http://localhost:5000/api/ads/999').json())
pprint(get('http://localhost:5000/api/ads/q').json())

pprint(delete('http://localhost:5000/api/ads/5').json())
