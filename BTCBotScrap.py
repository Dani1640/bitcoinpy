# Librerias
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from colorama import Fore, Style
from datetime import datetime
import os

# Otras funciones
clear = lambda: os.system('cls')

# Configurar Selenium - Chrome en modo HeadLess
browser_path = os.path.join( os.getcwd() , 'config', 'chromedriver.exe' )
directory_down = os.path.join( os.getcwd() , 'download' ) 
chromeOptions = Options()
chromeOptions.headless = True
prefs = {
            "download.default_directory": directory_down ,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=browser_path, options=chromeOptions)

# Paramertros del Scrapper
moneda_base = 'BTC'
moneda_compara = 'USD'

wait = WebDriverWait(driver, 1)
# Scrapper Página TradingView
url = f'https://es.tradingview.com/symbols/{moneda_base}{moneda_compara}/technicals/'
print(url)
driver.get(url)

def set_color(recom):
    if recom == 'FUERTE VENTA' or recom == 'VENDER':
        return Fore.RED
    elif recom == 'FUERTE COMPRA' or recom == 'COMPRAR':
        return Fore.GREEN
    else:
        return Style.RESET_ALL

def set_color_valor(anterior, nuevo):
    if nuevo > anterior:
        return Fore.GREEN
    else:
        return Fore.RED

def cast_moneda(valor):
    
    if valor == '':
        return 0
    else:
        return float(valor)
    
# Limpia consola
clear()
print( ' ::: BITCOIN ANALIZER ::: ')

moneda_valor = ''
while True:
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]')))
    driver.implicitly_wait(1)
    val_moneda = cast_moneda(moneda_valor)
    val_moneda_n =  cast_moneda(driver.find_elements_by_class_name('tv-symbol-price-quote__value')[0].text)
    if moneda_valor != val_moneda_n:  
        moneda_valor = val_moneda_n
        moneda_valor_n_str = '%.2f' % moneda_valor
        recom_resumen = driver.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[2]/span[2]').text
        recom_oscilador = driver.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[1]/span').text
        recom_medias_mov = driver.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[3]/span').text
        ahora  = datetime.now()
        ahora_str = ahora.strftime('%Y/%m/%d %H:%M:%S')
        print(' - ', 
              Style.RESET_ALL + ahora_str, 
              set_color_valor(val_moneda, val_moneda_n) + moneda_valor_n_str, 
              Style.RESET_ALL + ' | Resumen', 
              set_color(recom_resumen) + recom_resumen , 
              Style.RESET_ALL + ' | Osciladores', 
              set_color(recom_oscilador) + recom_oscilador, 
              Style.RESET_ALL + ' | Medias Movs', 
              set_color(recom_medias_mov) + recom_medias_mov + Style.RESET_ALL 
        )
        
        
driver.quit()