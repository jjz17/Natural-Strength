import random
import re
import time
import urllib.request as urllib
from datetime import datetime

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def get_soup(url):
    """ Returns the BeautifulSoup object for website of the given category name in the
        given CL webpage's homepage

    Args:
        url(String): the given URL

    Returns:
        soup(bs4.BeautifulSoup): the BeautifulSoup object representation of the desired category page
    """

    # Open the target category page
    html = urllib.urlopen(url)

    # Create a BeautifulSoup object after the HTML page is read
    soup = BeautifulSoup(html.read())

    # Close the urllib connection to avoid issues with the website
    html.close()

    return soup


def get_dict(sex: str = 'M'):
    url = ''
    min_class = 0
    max_class = 0
    label_val = ''

    if sex == 'M':
        url = 'https://usapl.liftingdatabase.com/records-default?recordtypeid=120365&categoryid=59&weightclassid=122663'
        min_class = 52.0
        max_class = 141.0
        # ABSTRACT THIS
        label_val = 'USAPL Nationals 2022 - Male'
    else:
        url = 'https://usapl.liftingdatabase.com/records-default?recordtypeid=120362&categoryid=59&weightclassid=122653'
        min_class = 44.0
        max_class = 101.0
        label_val = 'USAPL Nationals 2022 - Female'

    soup = get_soup(url)
    choices = soup.find('optgroup', attrs={'label': label_val})
    options = choices.find_all('option')
    url_class_map = {}
    for option in options:
        w_class = ''
        # Handle max class
        if option.get_text()[-1] == '+':
            w_class = max_class
        else:
            w_class = float(option.get_text()) * -1
        if w_class >= min_class:
            url = option['value']
            url_class_map[url] = w_class
    print(url_class_map)
    return url_class_map


def get_records_df():
    m_dict = get_dict('M')
    f_dict = get_dict('F')
    dicts = [(m_dict,
              'https://usapl.liftingdatabase.com/records-default?recordtypeid=120365&categoryid=59&weightclassid=',
              'M'),
             (f_dict,
              'https://usapl.liftingdatabase.com/records-default?recordtypeid=120362&categoryid=59&weightclassid=',
              'F')]
    # Create DataFrame
    df = pd.DataFrame(columns=['Name', 'Weight Class', 'Lift', 'Weight (kg)', 'Date', 'Sex'])

    for info in dicts:
        info_dict = info[0]
        target_url = info[1]
        sex = info[2]
        for url, w_class in info_dict.items():
            page = f'{target_url}{url}'
            soup = get_soup(page)
            body = soup.find_all('tbody')[1]
            # print(body)
            # titles = body.find_all('th', {'colspan' : '9'})
            records = body.find_all('tr', class_=None)
            lift = ''
            for count, record in enumerate(records):
                # even tags are lift title
                if count > 0 and (count - 1) % 2 == 0:
                    lift = record.get_text().strip()
                #         print(lift)
                #         print(record.get_text().strip())
                # odd tags are info
                if count > 0 and (count - 1) % 2 == 1:
                    infos = record.find_all('td')
                    name = infos[1]
                    #                     weight_class = infos[0]
                    weight = infos[2]
                    date = infos[3]
                    # Create a temporary dictionary to store the information of the current post
                    temp_dict = {'Name': name, 'Weight Class': w_class, 'Lift': lift, 'Weight (kg)': weight,
                                 'Date': date, 'Sex': sex}
                    # Append the current post's information to the df DataFrame to create its respective row
                    df = df.append(temp_dict, ignore_index=True)
            #         for info in infos:
            #       except  print(info.get_text().strip())
            print('Running...')
            time.sleep(random.randint(2, 3))

    # Wrangling
    df['Name'] = df['Name'].apply(lambda x: x.get_text())
    df['Weight (kg)'] = df['Weight (kg)'].apply(
        lambda x: float(x.get_text().split()[0]) if len(x.get_text()) > 0 else np.nan)
    df['Date'] = df['Date'].apply(lambda x: re.sub(r"[\n\t\s]*", "", x.get_text()))
    df['Date'] = df['Date'].apply(
        lambda x: datetime(1, 1, 1).date() if len(x) == 0 else datetime.strptime(x, '%m/%d/%Y').date())

    return df


df = get_records_df()

df.to_csv('current_usapl_american_raw_records.csv', index=False)
