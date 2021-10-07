import argparse

from datetime import datetime

import pandas as pd

import time

import os

import re

from tqdm import tqdm

from unidecode import unidecode

import helper

parser = argparse.ArgumentParser(description='Variety Extraction')
parser.add_argument('-i', '--input', metavar='', required=True, help='Set a link .csv')
parser = parser.parse_args()

# creating files directory 
os.system("mkdir -p /app/files")

# setting the path
path_to_files = os.getcwd()+os.sep+'files'+os.sep

driver = helper.get_chromedriver()

# VALIDATING IP
driver.get('https://www.meuip.com.br/')
ip = driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/h3').text.split(' é ')[1]
helper.ip_validator(ip)

# SETTING TODAY
TODAY = datetime.now().strftime('%Y-%m-%d')

# CREATING LINKS LIST
links_list = helper.links_list_create(parser.input)

failed_links   = '/app/failed_links_{}.csv'.format(TODAY)
correct_links  = '/app/correct_links_{}.csv'.format(TODAY)

for csv_link in tqdm(links_list):
    # se ja estiver no csv de 'baixados'
    #    continue
    if os.path.exists(correct_links) == True:
        df = pd.read_csv(correct_links)
        if df['Link'].isin([csv_link]).sum():
            continue
    
    varieties = {}
    # lists for data separation
    fields_list = []
    results_list = []
    regions_list = []

    driver.get(csv_link)

    # Finding the table where are the data
    try:
        table = driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[3]/td/table/tbody')
    except:
        helper.csv_link_writer(csv_link, failed_links)
        continue
    
    # finding where are the titles
    titles = table.find_elements_by_class_name('td_titulo123')

    # finding where are the results
    results = table.find_elements_by_class_name('td_resultado123')

    # finding where are the regions
    regions = table.find_elements_by_id('arqs')

    # Regions extraction by the text where "DESCRITORES" are not found
    for region in regions:
        if 'DESCRITORES' not in region.text:
            regions_list.append(region.text)
    varieties["regions"] = regions_list

    # Extracting the title name from the rows
    for title in titles:
        if "DESCRITORES" not in title.text and "REGIÃO" not in title.text:
            fields_list.append(title.text.replace(":",""))

    # Extracting the results from the rows
    for result in results[0:len(fields_list)]:
        results_list.append(result.text)

    # Merging the two lists from fields into the results
    for i in range(len(fields_list)):
        varieties[fields_list[i]] = results_list[i]

    variety_name = re.sub(r'[^\w]', '', unidecode(varieties['NOME COMUM']).split('/')[0].replace(',','').replace(' ', '').replace("\\", ''))

    json_file = '/app/files/variety_{}_{}_{}.json'.format(csv_link.split("=")[1], variety_name, TODAY)
    helper.json_writer(varieties, json_file)

    json_dict = helper.json_reader(json_file)

    if len(list(json_dict.keys())[1]) == 0:
        helper.csv_link_writer(csv_link, failed_links)
    else:
        helper.csv_link_writer(csv_link, correct_links)
        
    # Finding where are the descriptores by id
    descriptors = table.find_elements_by_id('arqs')

    for descriptor in descriptors: 
        if "DESCRITORES" in descriptor.text:
            button_click = driver.find_element_by_xpath('//a[@href="javascript:void(0);"]')
            button_click.click()

    try:
        file_name = 'files'+os.sep+csv_link.split("=")[1]+"_"+list(json_dict.values())[1].replace("*","").replace(" ","")+"_"+variety_name+'_'+TODAY+".pdf"
    except:
        helper.csv_link_writer(csv_link, failed_links)
    try:
        os.rename(path_to_files+'document.pdf',file_name) 
    except:
        continue

driver.quit()