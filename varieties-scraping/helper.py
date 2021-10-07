# webpage opening
from seleniumwire import webdriver

# Import DictWriter class from CSV module
from csv import DictWriter, writer

import csv

from datetime import datetime

import os

import json

from pathlib import Path

PROXY_HOST = os.getenv('PROXY_HOST')  # rotating proxy or host
PROXY_PORT = os.getenv('PROXY_PORT')  # port
PROXY_USER = os.getenv('PROXY_USER')  # username
PROXY_PASS = os.getenv('PROXY_PASS')  # password
if os.getenv('USE_PROXY') == "False" or os.getenv('USE_PROXY') == "0":
    USE_PROXY = False
else:
    USE_PROXY = True

#setting the path
download_dir = os.path.join(os.getcwd(),'files')
tmp_dir = os.path.join(os.getcwd(),'tmp')

# Open your CSV file in append mode
# Create a file object for this file
def csv_dict_writer(dict_to_write, file):
    if os.path.exists(file) == False:
        with open(file, 'w', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(dict_to_write.keys())

    with open(file, 'a', newline='') as f_object:
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(
            f_object, fieldnames=dict_to_write.keys())

        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(dict_to_write)

        # Close the file object
        f_object.close()

# CREATING LINKS LIST
def links_list_create(file):
    values = []
    csvFile = csv.reader(open(file, "r"))
    next(csvFile)
    for row in csvFile:
        values.append(row[0].split())
    links_list = [item for sublist in values for item in sublist]
    return links_list

# Open your CSV file in append mode
# Create a file object for this file
def csv_link_writer(link, file):
    if os.path.exists(file) == False:
        with open(file, 'w', newline='') as f_object:
            f_object.write('Link\n')

    with open(file, 'a', newline='') as f_object:
        f_object.write(link+'\n')

        # Close the file object
        f_object.close()

# JSON WRITER
def json_writer(dictionary, file):
    Path("/".join(file.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
    if os.path.exists(file) == False:
        with open(file, 'w', newline='', encoding='utf8') as fp:
            json.dump(dictionary ,fp, indent=4, ensure_ascii=False)

# JSON READER
def json_reader(file):
    with open(file, 'r', newline='', encoding='utf8') as fp:
        return json.load(fp)

# IP VALIDATOR
def ip_validator(scrap_ip):
    if USE_PROXY == True:
        if os.getenv('PROXY_IP') != scrap_ip:
            raise Exception('Different IPs')
        else:
            print('Proxy IP OK')
        

# CHROME DRIVER 
def get_chromedriver():
    if USE_PROXY == True:
        proxy = {
            'proxy': {
                'http': 'http://{}:{}@{}:{}'.format(os.getenv('PROXY_USER'),
                                                    os.getenv('PROXY_PASS'),
                                                    os.getenv('PROXY_IP'),
                                                    os.getenv('PROXY_PORT')),
                'https': 'http://{}:{}@{}:{}'.format(os.getenv('PROXY_USER'),
                                                    os.getenv('PROXY_PASS'),
                                                    os.getenv('PROXY_IP'),
                                                    os.getenv('PROXY_PORT')),
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_experimental_option('prefs', {
            "download.default_directory": tmp_dir, #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
            "download_restrictions": 0,
            "safebrowsing.enabled": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads":1
        })
        driver = webdriver.Chrome(seleniumwire_options=proxy, options=options)
        return driver
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=options)
        options.add_experimental_option('prefs', {
            "download.default_directory": tmp_dir, #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
            "download_restrictions": 0,
            "safebrowsing.enabled": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads":1
        })
        driver = webdriver.Chrome(options=options)
        return driver
