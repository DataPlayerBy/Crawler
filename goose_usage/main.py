import requests
from goose3 import Goose
from goose3.text import StopWordsChinese
url = 'http://sports.sina.com.cn/basketball/nba/2018-09-24/doc-ifxeuwwr7592449.shtml'
html = requests.get(url).content
goose = Goose({'stopwords_class': StopWordsChinese})
article = goose.extract(raw_html=html)
print('title:{}'.format(article.title))
print('content:{}'.format(article.cleaned_text))
print('opengraph:{}'.format(article.opengraph))
