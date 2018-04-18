# function to scrape OHCHR urls for organisations and pdfs

def ohchr_scrape(url):
    import requests
    import pandas as pd
    import re
    from bs4 import BeautifulSoup
    
    with requests.Session() as s:
        pagecode = s.get(url)
    
    soup = BeautifulSoup(pagecode.text, 'html5lib')
    table = soup.findAll('table')[1]
    
    orgs = []
    
    i = 1
    for table_row in table.findAll("tr"):   # loop through table rows
        # Each table row has a set of table cells, or tds
        table_cells = table_row.findAll('td')
        if len(table_cells) > 0:
            org = {} # dictionary storing organisation
            try:# store organisation name
                org['name'] = table_cells[0].text[20:]
            except:
                print('cannot find name for row ' + str(i))
            try: # store pdf url
                org['pdf'] = table_cells[1].find('a')['href']
            except: 
                print('error for pdf url for row ' + str(i))
            orgs.append(org)
        i=i+1
        
    dforgs = pd.DataFrame(orgs)
    dforgs = dforgs.drop_duplicates()
    dforgs = dforgs.drop(dforgs.index[0])

    return dforgs


def download_pdf(url, filepath):
    import requests
    r = requests.get(url)
    with open(filepath, 'wb') as f:  
        f.write(r.content)