import requests
from bs4 import BeautifulSoup
import collections
collections.Callable = collections.abc.Callable

try:
    vgm_url = 'https://blinkit.com/cn/vegetables-fruits/fresh-vegetables/cid/1487/1489/'
    html_text = requests.get(vgm_url, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'})
    html_text.raise_for_status()
    soup = BeautifulSoup(html_text.text, 'html.parser')
    print(soup)
    vegies= soup.find('div', class_="products--card").find_all('a')
    for vegie in vegies:
        divContainer = vegie.find('div', class_="plp-product")
        print(divContainer.prettify())
        divImage =  divContainer.find('img')
        print(divImage.prettify())

    # vegies= soup.
    #

except Exception as e:
    print(e)