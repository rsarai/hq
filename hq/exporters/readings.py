import requests
from bs4 import BeautifulSoup


for i in range(1, 50):
    res = requests.get(f"https://blog.quastor.org/?page={i}")
    content = res.content

    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all("div", {"class": "my-16"})
    important_div = divs[1]

    links = ["https://blog.quastor.org/" + link.get("href") for link in important_div.find_all("a")]
    headers = [title.string for title in important_div.find_all("h2")]

    for h, l in zip(headers, links):
        print(h, l)


# BYTE_BYTE_GO_URL = "https://blog.bytebytego.com/sitemap.xml"
# ARCHITECTURE_URL = "https://architecturenotes.co/sitemap-posts.xml"
# res = requests.get(ARCHITECTURE_URL)
# xml = res.text

# soup = BeautifulSoup(xml)
# sitemapTags = soup.find_all("loc")

# print("The number of sitemaps are {0}".format(len(sitemapTags)))

# xmlDict = {}
# for sitemap in sitemapTags:
#     xmlDict[sitemap.text] = sitemap.findNext("lastmod").text

QUASTOR_URL = "https://blog.quastor.org/sitemap.xml"
res = requests.get(QUASTOR_URL)
xml = res.text

soup = BeautifulSoup(xml)
sitemapTags = soup.find_all("sitemap")

print("The number of sitemaps are {0}".format(len(sitemapTags)))

xmlDict = {}
for sitemap in sitemapTags:
    ss = requests.get(sitemap.findNext("loc").text)
    _xml = ss.text
    _soup = BeautifulSoup(_xml)
    _sitemapTags = _soup.find_all("loc")
    for sitemap in _sitemapTags:
        xmlDict[sitemap.text] = sitemap.findNext("lastmod").text
