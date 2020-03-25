import sys
sys.path.append('/home/akash/Desktop/selenium-scrapper/selenium-3.141.0/selenium')
sys.path.append('/home/akash/Desktop/selenium-scrapper')
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import string
import time

def do_scrape(browser, u):
    browser.get(u.strip())
    timeout = 10
    des = "unknown"
    time.sleep(1)
    try:
        # Wait until the final element [Avatar link] is loaded.
        # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
        # the last things to be loaded.
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[1]/div/div/div[1]/div[1]/img')))
    except TimeoutException:
        print("Timed out waiting for page to load")
        return {}

    users_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]')
    rating_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div')
    users_rated_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[2]/span')
    des_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[2]/div[2]')
    des2_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[2]/div[3]')
    dev_element = browser.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]')
    #users_element = browser.find_elements_by_xpath("//span[@class='e-f-ih']")
    #reviews_element = browser.find_elements_by_xpath("//div[@class='KnRoYd-N-nd']")
    #category_element = browser.find_elements_by_xpath("//a[@class='e-f-y']")

    users = [x.text for x in users_element] 
    rating = [x.get_attribute('data-tooltip') for x in rating_element ]
    users_rated = [x.text for x in users_rated_element] 
    des = ''.join([x.text for x in des_element])
    des2 = ''.join([x.text for x in des2_element])
    dev = ''.join([x.text for x in dev_element])
    #users = [x.text for x in users_element] 
    #nrev = [x.text for x in reviews_element]
    #category = ','.join([x.text for x in category_element])
    #reviewers = ""
    out = {}
    #if len(nrev) > 0:
    #    reviewers = nrev[0]
    if len(users) > 0:
        users = users[0]
    if len(rating) > 0:
        rating = rating[0]
    if len(users_rated) > 0:
        users_rated = users_rated[0]
    users = ''.join([x for x in users if x in string.printable]).strip()
    out['Overview'] = des.encode('utf-8')
    out['Description'] = des2.encode('utf-8')
    out['users'] = users
    out['rating'] = rating.strip('Average rating: ')[0]
    out['users_rated'] = users_rated
    out['Developer'] = dev
    #out['reviews'] = reviewers
    #out['category'] = category
    return out

urls = []
rows = []
out_w = open('gsuite-addons-out.csv', 'w')
writer = csv.writer(out_w)

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)
count =  0


with open("gsuite-addons.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        count = count+1
        print(str(count) + ": " + row[0] + "," + row[1])
        row_new = row
        if (count == 1):
            row_new.append('Link')
            row_new.append('Total Users')
            row_new.append('Rating')
            row_new.append('Users Rated')
            row_new.append('Overview')
            row_new.append('Description')
            row_new.append('Developer')
            row_new.append('Mark Trusted?')
        else:
            url = 'https://gsuite.google.com/u/2/marketplace/app/app/' + row[1].split('-')[0]
            out = do_scrape(browser,url)
            if 'users' in out:
                row_new.append(url)
                row_new.append(out['users'])
            else:
                row_new.append('')
                row_new.append('')
            if 'rating' in out:
                row_new.append(out['rating'])
            else:
                row_new.append('')
            if 'users_rated' in out:
                row_new.append(out['users_rated'])
            else:
                row_new.append('')
            if 'Overview' in out:
                row_new.append(out['Overview'])
            else:
                row_new.append('')
            if 'Description' in out:
                row_new.append(out['Description'])
            else:
                row_new.append('')
            if 'Developer' in out:
                row_new.append(out['Developer'])
            else:
                row_new.append('')
            #if (len(row_new)) >= 8:
            #    if (row_new[3] != "Link to addon" and row_new[3] != ""):
            #        url = row_new[3]
            #        out = do_scrape(browser, url)
            #        if 'category' in out:
            #            row_new[4] = out['category']
            #        if 'reviews' in out:
            #            row_new[5] = out['reviews']
            #        if 'users' in out:
            #            row_new[6] = out['users']
            #        if 'description' in out:
            #            row_new[7] = out['description']
            if 'Gmail' in row[3] or 'Drive' in row[3] or 'Calendar' in row[3]:
                row_new.append('Yes')
            else:
                row_new.append('No') 
        writer.writerow(row_new)
        #if (count == 10):
        #    break

out_w.close()


