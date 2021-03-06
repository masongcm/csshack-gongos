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
            try: # store language
                org['lang'] = table_cells[1].find('a').contents[0]
                org['lang'] = org['lang'].lower()
            except: 
                print('error for language for row ' + str(i))
            orgs.append(org)
        i=i+1
        
    dforgs = pd.DataFrame(orgs)
    dforgs = dforgs.drop(dforgs.index[0])
        
    return dforgs

# function to download pdf from URL
# url = url of pdf file
# filepath = path of file to write
def download_pdf(url, filepath):
    import requests
    r = requests.get(url)
    with open(filepath, 'wb') as f:  
        f.write(r.content)
        
# function to extract text from document
# (returns text as a string)
def extract_text(document):
    import PyPDF2
    from PyPDF2 import PdfFileReader
    with open(document,'rb') as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        text_page = []
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = read_pdf.getPage(page_number)
            page_content = page.extractText()
            text_page.append(page_content)
    text = " ".join(text_page)
    return text

#function to extract text from documents and converting them into a dictionary
# dictionary keys are names of NGOs
# dictionary values are full text of report
def extract_to_dict(country):
    text_dict = {}
    for index, row in country.iterrows():
        try: 
            text_dict[index] = [row['name'],[extract_text(row['file'])], row['lang']]
        except:
            print('Cannot extract text for ' + str(row['name']))
    return text_dict

# function gets the text from csv file
# turns them into a dataframe 
def get_text(datain):
    import pandas as pd
    data_dict = extract_to_dict(datain)
    data = pd.DataFrame(data_dict)
    data = data.reset_index().transpose()
    data.rename(columns = {0:'ngo_name', 1:'text', 2:'language'} , inplace=True)
    data = data.drop('index', axis=0)
    data['text'] = data['text'].apply(lambda x: x[0].replace("\n",""))
    data['language'] = data['language'].replace("español", "spanish")
    data['language'] = data['language'].replace("français", "french")
    return data

# function to retrieve pdfs from urls and attach pdf path to dataset
def get_pdfs(data, folderpath):
    import time
    filenames = []
    for index, row in data.iterrows():
        pdfurl = row['pdf']
        orgname = row['name']
        try:
            filename = folderpath + "_".join(orgname.split()) + '.pdf'
            filenames.append(filename)
            download_pdf(pdfurl, filename)
            print('Downloaded ' + orgname)
        except:
            print('Skipping ' + orgname)
        time.sleep(.5)
    data['file'] = filenames
    return data