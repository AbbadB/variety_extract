from datetime import datetime

from tqdm import tqdm

import helper

# webdriver configurations 
driver = helper.get_chromedriver()

TODAY = datetime.now().strftime('%Y-%m-%d')

def get_link (variety_id):
    url = 'https://sistemas.agricultura.gov.br/snpc/cultivarweb/detalhe_cultivar.php?codsr={}'.format(variety_id)
    driver.get(url)

    try:
        t_body = driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[3]/td/table/tbody')
        titles = t_body.find_elements_by_class_name('td_titulo123')

        for i, title in enumerate(titles):
            if title.find_element_by_tag_name('td').text == 'SITUAÇÃO:':
                situation_position = i
                
        results = t_body.find_elements_by_class_name('td_resultado123')
        situation = results[situation_position].find_element_by_tag_name('td').text
        if situation == 'REGISTRADA':
            variety_link_id={'url' : url, 'variety_id' : variety_id}
            helper.csv_dict_writer(variety_link_id, '/app/link_{}.csv'.format(TODAY))
    except:
        return  
# VALIDATING IP
driver.get('https://www.meuip.com.br/')
ip = driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/h3').text.split(' é ')[1]
helper.ip_validator(ip)

for variety_id in tqdm(list(range(0,50001))):
    get_link(variety_id)

driver.quit()