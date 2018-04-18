def download_pdf(url, filepath):
    import requests
    r = requests.get(url)
    with open(filepath, 'wb') as f:  
        f.write(r.content)