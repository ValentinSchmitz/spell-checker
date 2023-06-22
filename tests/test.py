import requests as req

def download(url):
    try:
        res = req.get(url)
    except ConnectionError as error:
        return None
    if res.status_code != 200:
        pass
    return res

print(download(("https://api.github.com/repos/jankelemen/convert-dict-tool-from-chromium/contents/")).json())