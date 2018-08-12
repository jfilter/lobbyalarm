import requests


def download_page(page):
    """extract is limited to one page at a time
    """
    url = f"https://lobbypedia.de/api.php?action=query&prop=extracts&titles={page['title']}&redirects=true&format=json&explaintext"
    print(url)
    r = requests.get(url)
    r.raise_for_status()
    r_json = r.json()

    # some sites were restricted so skip over them
    if not "query" in r_json:
        print(r_json, "aborting")
        return

    for p in r_json["query"]["pages"].values():
        if not 'extract' in p:
            continue
        # print(p)
        with open(f"../documents/{p['title'].replace('/', '_')}.txt", "w") as f:
            f.write(p['extract'])
        print(f"wrote {p['title']}")


all_pages_url = "https://lobbypedia.de/api.php?action=query&list=allpages&format=json"


cont = None
while True:
    url = all_pages_url
    if cont:
        url += '&apcontinue=' + cont
    print(url)
    r = requests.get(url)
    r.raise_for_status()
    r_json = r.json()
    if "query" in r_json:
        all_pages = r_json["query"]["allpages"]
        list(map(download_page, all_pages))
    print(r_json)
    if "query-continue" not in r_json:
        print('break')
        break
    else:
        cont = r_json["query-continue"]["allpages"]["apcontinue"]
