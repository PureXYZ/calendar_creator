import requests

r = requests.get('https://api.github.com/events')

r.encoding = 'ascii'

print r.text