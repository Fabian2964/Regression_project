#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# source 1: https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
# source 2: https://stackoverflow.com/questions/6442118/python-measuring-pixel-brightness

def get_image_brightness(image_list):
    global bright_list
    bright_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            brightness = (0.2126*R) + (0.7152*G) + (0.0722*B)
            bright_list.append(brightness)
        except:
            bright_list.append(np.nan)
        print(i)
    return(bright_list)

def get_dominant_color(image_list):
    colors = ['red', 'green', 'blue']
    global color_list
    color_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            dominant_color = colors[np.argmax([R, G, B])]
            color_list.append(dominant_color)
        except:
            color_list.append(np.nan)
        print(i)
    return(color_list)


def get_faz_articles(max_date):

    url_entrypage = 'https://www.faz.net/uebersichten/schlagzeilen/s1.html?zeitraum=unbegrenzt#listPagination'
    response_entrypage = requests.get(url_entrypage)
    page_entrypage = response_entrypage.text
    soup_entrypage = bs(page_entrypage)
    
    page_no = int(soup_entrypage.find(class_='ctn-List_CounterTotal').text.strip())
    max_d = dt.strptime(max_date, '%d.%m.%Y')
    
    global d
    d = {'id': [], 'title_headline': [], 'title_link': [], 'premium': [], 'datetime': [], 'link': [], 'headline_text': [],
     'teaser': [], 'image': []}
    
    for j in range(1, page_no):
    
        url = 'https://www.faz.net/uebersichten/schlagzeilen/s'+str(j)+'.html?zeitraum=unbegrenzt#listPagination'
        response = requests.get(url)
        page = response.text
        soup = bs(page)
        
        date_site = dt.strptime(soup.find_all(class_='tsr-Base_ContentMetaTime')[0]['title'][:-10], '%d.%m.%Y')
        
        if date_site >= max_d:
            
            for i in soup.find_all('article'):
                
                try:
                    position = i.find(class_='js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink')['href'].find('html')
                    link = i.find(class_='js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink')['href']
                    identifier = link[(position-9):(position-1)]
                    d['id'].append(identifier)
                except:
                    d['id'].append('na')
                
                try:
                    title_headline = i.find(class_='tsr-Base_HeadlineText').text
                    title_headline = title_headline.replace('\n', '')
                    title_headline = title_headline.replace('\t', '')
                    title_headline = title_headline.rstrip()
                    d['title_headline'].append(title_headline)
                except:
                    d['title_headline'].append('na')
                
                try:
                    title_link = i.find(class_='js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink')['title']
                    d['title_link'].append(title_link)
                except:
                    d['title_link'].append('na')
                    
                try:
                    premium = i.find(class_='js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink')['data-is-premium']
                    d['premium'].append(premium)
                except:
                    d['premium'].append('na')
                
                try:
                    link = i.find(class_='js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink')['href']
                    d['link'].append(link)
                except:
                    d['link'].append('na')
                    
                try:
                    datetime = pd.to_datetime(i.find(class_='tsr-Base_ContentMetaTime')['title'].strip(' Uhr'))
                    d['datetime'].append(datetime)
                except:
                    d['datetime'].append(pd.to_datetime(np.nan))
                
                try:
                    headline_text = i.find(class_='tsr-Base_HeadlineEmphasisText').text
                    headline_text = headline_text.replace('\n', '')
                    headline_text = headline_text.replace('\t', '')
                    headline_txt = headline_text.rstrip()
                    d['headline_text'].append(headline_txt)
                except:
                    d['headline_text'].append('na')
                
                try:
                    teaser = i.find(class_='tsr-Base_Content')
                    teaser = i.text
                    teaser = teaser.replace('\n', '')
                    teaser = teaser.replace('\t', '')
                    d['teaser'].append(teaser)
                except:
                    d['teaser'].append('na')
                    
                try:
                    image = i.find(class_='media tsr-Base_Image js-lazy')['data-lazy-src']
                    d['image'].append(image)
                except:
                    d['image'].append('na')

     
        else:
            break
        
        print(f'Scraping for page {j} complete.')
    
    return(d)

def get_ivw_daily(month_no, date_table):

    clicks_months = dt.today().month - month_no -1
    x = 1
    y = 1
    
    for i in range(len(date_table)):
        y = 1
        for j in range(len(date_table.T)):
            if (pd.isna(date_table.iloc[x-1, y-1])) == False:

                chromedriver = "/media/fabian/VM_space/Metis/02_Regression/chrome_driver/chromedriver" # path to the chromedriver executable
                os.environ["webdriver.chrome.driver"] = chromedriver
                driver = webdriver.Chrome(chromedriver)
                ivw_url = 'https://ausweisung.ivw-online.de/index.php?tagl=1&mz_szm=202202&it=1&setc=1'
                driver.get(ivw_url)
                date_picker = driver.find_element_by_xpath('//*[@id="ibody"]/div[3]/div/div/form/div/input')
                driver.execute_script("arguments[0].click();", date_picker)
                time.sleep(1)
                
                for k in range(clicks_months):
                    date_picker = driver.find_element_by_xpath('//*[@id="ibody"]/div[4]/div[2]/div[1]/table/thead/tr[1]/th[1]/span').click()
#                     driver.execute_script("arguments[0].click();", date_picker)
                    time.sleep(1)
                
                for l in range(2):
                    date_picker = driver.find_element_by_xpath(f'//*[@id="ibody"]/div[4]/div[2]/div[1]/table/tbody/tr[{x}]/td[{y}]').click()
                    time.sleep(1)
                
                date_picker = driver.find_element_by_xpath('//*[@id="ibody"]/div[3]/div/div/form/table/tbody/tr/td[1]/div/input')
                driver.execute_script("arguments[0].click();", date_picker)
                time.sleep(1)
                driver.quit()
                
                print(f'Tag {int(date_table.iloc[x-1, y-1])} download complete.')
                
            y += 1
        x += 1

