from webdriver_wrapper import WebDriverWrapper
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import os
from datetime import date, datetime, timedelta
import telepot

BOT_API_KEY = os.environ['BOT_API_KEY']
BOT_INSTANCE = telepot.Bot(BOT_API_KEY)

class AgendaBolsoCrawler:
    def __init__(self, day):
        self.driver = WebDriverWrapper()._driver
        self.wait = WebDriverWait(self.driver, 10)

        #Diario ou retroativo

        self.scrape(day)
        #self.retroativo()

    def retroativo(self):
        #Defina os dias de inicios e fim
        start = date(2019, 1, 1)
        end = date(2019, 7, 7)
        delta = end - start
        for i in range(delta.days):
            self.scrape(start + timedelta(days=i))

    def scrape(self,day):
        items_agenda = []
        day_string = day.strftime("%Y-%m-%d")
        print('Dia: '+day_string)
        self.driver.get('https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/' + day_string)
        time.sleep(5)
        compromissos = self.driver.find_elements_by_class_name("item-compromisso")
        try:
            for compromisso in compromissos:
                horario = '*Horário:* '+ compromisso.find_element_by_xpath(".//time").text + '\n'
                titulo = compromisso.find_element_by_xpath(".//h4[@class='compromisso-titulo']").text + '\n'
                local = '*Local:* ' + compromisso.find_element_by_xpath(".//p[@class='compromisso-local']").text + '\n'
                items_agenda.append([horario,titulo,local])
            if(items_agenda):
                self.send_to_chats(items_agenda, day_string)
        except:
            print('Not Found')
    
    def send_to_chats(self,rows, day_string):
        chats = []
        string_rows = '\n'.join(''.join(row) for row in rows)
        string_rows = '*Agenda Bolsonaro '+ day_string + '* \n' + string_rows
        bot_updates = BOT_INSTANCE.getUpdates()
        for update in bot_updates:
            try:
                chats.append(update['message']['chat']['id'])
            except:
                print('empity message')
        #deduplicate
        chats = list(set(chats))
        print(chats)
        print(string_rows)
        for chat in chats:
            BOT_INSTANCE.sendMessage(chat, string_rows, parse_mode='markdown')



        
def lambda_handler(event=None, context=None,day = datetime.now()):
    print('Coletando agenda presidencial')
    AgendaBolsoCrawler(day = day)