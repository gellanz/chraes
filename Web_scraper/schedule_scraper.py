from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import pandas as pd
import time
import os

# User credentials
load_dotenv()
user = os.getenv('USERR')
password = os.getenv('PASSW')

# No window for Chrome driver
op = webdriver.ChromeOptions()
op.add_argument("--headless")

driver = webdriver.Chrome('Web_scraper/chromedriver', options=op)
driver.get('https://www.saes.upiita.ipn.mx/')

# Finding the input tags
user_in = driver.find_element_by_css_selector('#ctl00_leftColumn_LoginUser_UserName')
pas_in = driver.find_element_by_css_selector('.passwordEntry')
captcha_in = driver.find_element_by_css_selector("#ctl00_leftColumn_LoginUser_CaptchaCodeTextBox")

# Screenshot for the captcha
driver.save_screenshot("screen.png")

# Sending the user data to the form
user_in.send_keys(user)
pas_in.send_keys(password)
captcha = input("Captcha:")
captcha_in.send_keys(captcha)
pas_in.send_keys(Keys.RETURN)

# Going to the schedules page in the same session
driver.get('https://www.saes.upiita.ipn.mx/Academica/horarios.aspx')

careers = {"M" : [], "B": [], "T": []}
periods = ["1", "2", "3", "4", "5"]
shifts = ["M", "V"]
column_info = ["Grupo", "Asignatura", "Profesor", "Edificio", "Salón", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"]

# Scraping
for career in careers.keys():
    career_schedules_finder = driver.find_element_by_id("ctl00_mainCopy_Filtro_cboCarrera")
    career_schedules_selector = Select(career_schedules_finder)
    career_schedules_selector.select_by_value(career)
    for period in periods:
        # time.sleep(0.3)
        try:
            period_finder = driver.find_element_by_id("ctl00_mainCopy_Filtro_lsNoPeriodos")
            period_selector = Select(period_finder)
            period_selector.select_by_value(period)
        except:
            pass
        for shift in shifts:
            # time.sleep(0.3)
            shift_finder = driver.find_element_by_id("ctl00_mainCopy_Filtro_cboTurno")
            shift_selector = Select(shift_finder)
            shift_selector.select_by_value(shift)
            table = driver.find_element_by_id('ctl00_mainCopy_dbgHorarios')
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                course_row = row.find_elements(By.TAG_NAME, "td")
                course_data = [field.text for field in course_row]
                careers[career].append(course_data)

mechatronics = pd.DataFrame(careers["M"][1:], columns=column_info).drop(["Edificio", "Salón", "Sab"], axis=1)
bionics = pd.DataFrame(careers["B"][1:], columns=column_info).drop(["Edificio", "Salón", "Sab"], axis=1)
telematicss = pd.DataFrame(careers["T"][1:], columns=column_info).drop(["Edificio", "Salón", "Sab"], axis=1)

mechatronics.to_csv("Web_scraper/Data_2023_1/mechatronics_schedules.csv", index=False)
bionics.to_csv("Web_scraper/Data_2023_1/bionics_schedules.csv", index=False)
telematicss.to_csv("Web_scraper/Data_2023_1/telematics_schedules.csv", index=False)