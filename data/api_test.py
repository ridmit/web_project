from pprint import pprint

from requests import get, delete, post

# Тестирование AdsResource
pprint(get('http://localhost:5000/api/ads/1').json())
pprint(get('http://localhost:5000/api/ads/999').json())
pprint(get('http://localhost:5000/api/ads/q').json())

pprint(delete('http://localhost:5000/api/ads/5').json())

# Тестирование AdsListResource
pprint(get('http://localhost:5000/api/ads').json())

pprint(post('http://localhost:5000/api/ads').json())
pprint(post('http://localhost:5000/api/ads',
           json={'title': 'Заголовок'}).json())
pprint(post('http://localhost:5000/api/ads',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_sold': False,
                 'price': 207,
                 'filename': "123.jpg"}).json())
