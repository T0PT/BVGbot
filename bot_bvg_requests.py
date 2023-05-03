import urllib.request
import urllib.parse
import urllib.error
url = 'https://v5.bvg.transport.rest/locations?query=alexander&results=3&fuzzy=true'
html = urllib.request.urlopen(url).read()
print(html.decode())