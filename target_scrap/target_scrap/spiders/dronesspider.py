from numpy import product
import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class DronesspiderSpider(scrapy.Spider):
    name = 'dronesspider'
    allowed_domains = ['https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab']
    start_urls = ['https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109&showOnlyQuestions=true']


    def parse(self, response):
        ''''''# Get the product title
        title_path = response.xpath('//*[@id="viewport"]/div[4]/div/div[1]/div[2]/h1/span')
        product_title = title_path.css('span::text').get()

        # Get the product description
        desc_path = response.xpath('//*[@id="specAndDescript"]/div[1]/div[2]/div[1]')
        product_desc = desc_path.css('div::text').get()

        # Get the product specifications
        specifications_path =  response.xpath('//*[@id="specAndDescript"]/div[1]/div[1]')
        product_specifications = specifications_path.css('div::text').get()

        # Get the product highlights
        highlights_path = response.xpath('//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div[2]/div/ul/div')
        highlights = highlights_path.css('span::text').getall()

        # Get the miages url 
        img_path = response.xpath('//*[@id="viewport"]/div[4]/div/div[2]/div[1]/div/div/div')
        img_url = img_path.css('img::attr(src)').get()

        # Get the product price
        price_path = response.xpath('//*[@id="viewport"]/div[4]/div')
        product_price = price_path.css('span::text').get()

        # Get the product Questions
        ### Parse questions

        URL = 'https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab'
        Myoption=webdriver.ChromeOptions()
        Myoption.add_argument("--incognito")
        Myoption.add_argument("--headless")

        #chrome location to set  executable_path=r"")
        driver = webdriver.Chrome(options=Myoption)
        driver.get(URL)
        driver.implicitly_wait(20)
        ALL_QUESTIONS = []
        time.sleep(5)
        elem = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[2]/div[2]/div[1]/div[1]')
        product_price = elem.text

        Q_A_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div/div[3]/div[2]/div/div/div[1]/div[2]/ul/li[3]/a/div')
        Q_A_button.click()

        time.sleep(10)

        allquestionsbutton = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div/div[3]/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/button')
        allquestionsbutton.click()

        time.sleep(10)
    

        ques = driver.find_elements(By.TAG_NAME, 'h3')
        for q in ques:
            if q.text.startswith('Q'):
                #print('###########################')
                #print(q.text)
                ALL_QUESTIONS.append(q.text)
        

        item ={
            'product_title': product_title,
            'product_price': product_price,
            'product_desc': product_desc,
            'product_specifications': product_specifications,
            'product_highlights': highlights,
            'product_img_url': img_url,
            'product_questions': ALL_QUESTIONS
        }

        yield item
        
        

        pass
