from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import pandas as pd
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
captcha_in.send_keys(input("Captcha:"))
pas_in.send_keys(Keys.RETURN)

# Going to the ocupation page in the same session
driver.get('https://www.saes.upiita.ipn.mx/Academica/Ocupabilidad_grupos.aspx')

# Selecting actual school period
driver.find_element_by_id("ctl00_mainCopy_rblEsquema_0").click()


# Iterating over the 3 carreers
careers = {"M" : [], "B": [], "T": []}
columns_name = ["Grupo", "Semestre", "Cupo", "Inscritos", "Disponibles", "Asignatura"]
for career in careers.keys():
    # Finding the carreer selector 
    career_finder = driver.find_element_by_id("ctl00_mainCopy_dpdcarrera")
    career_selector = Select(career_finder)
    # Selecting which career to find
    career_selector.select_by_value(career)
    # Getting a single string for all the web table
    ocupability_str = driver.find_element_by_id("ctl00_mainCopy_GrvOcupabilidad").text
    # Split the rows for each \n into a single string
    rows = ocupability_str.split("\n")
    # Separate in columns by the spaces between them
    ocupability_processed = [col.split(" ") for col in rows[1:]]
    # the course name gets separated, let's fix it
    for row in ocupability_processed:
        # slicing the course name
        course_name_slice = row[2:-4]
        # concatenating
        course_str = " ".join(course_name_slice)
        # deleting the separated course name string
        del row[1:-4]
        # appending the concatenated string
        row.append(course_str)
        careers[career].append(row)
# Pandas dataframe
mechatronics = pd.DataFrame(careers["M"][1:], columns=columns_name)
bionics = pd.DataFrame(careers["B"][1:], columns=columns_name)
telematicss = pd.DataFrame(careers["T"][1:], columns=columns_name)
mechatronics.to_csv("Web_scraper/Data2022_2/mechatronics_ocupability.csv", index=False)
bionics.to_csv("Web_scraper/Data2022_2/bionics_ocupability.csv", index=False)
telematicss.to_csv("Web_scraper/Data2022_2/telematics_ocupability.csv", index=False)
