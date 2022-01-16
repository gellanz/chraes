from azure.cosmos import CosmosClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import pandas as pd
import os
from random import randint
import time

def create_id(df):
    df["id"] = df["Asignatura"] + df["Grupo"]
    return df

def concat_sort(df1, df2):
    df1 = df1.sort_values("id").reset_index(drop=True)
    df2 = df2.sort_values("id").reset_index(drop=True)
    df_complete = pd.concat([df1, df2], join="inner", axis=1)
    df_complete = df_complete.loc[:,~df_complete.columns.duplicated()]
    return df_complete

def to_cosmos_db(df, career_letter, containerdb):
    courses_keys = df.columns.tolist()
    processed_courses = df.values.tolist()
    data = [dict(zip(courses_keys, course)) for course in processed_courses]
    api = {"courses": data}
    if career_letter == "M":
        container_Mtemp.upsert_item(api)
    elif career_letter == "B":
        container_Btemp.upsert_item(api)
    else:
        container_Ttemp.upsert_item(api)
    api["id"] = career_letter
    containerdb.upsert_item(api)

# User credentials
load_dotenv()
user = os.getenv('USERR')
password = os.getenv('PASSW')
HOST = os.getenv('HOST')
MASTER_KEY = os.getenv('KEY')
DATABASE_ID = os.getenv('DBID')
# CONTAINER_ID = os.getenv('CONTAINERID')

# Azure credentials
client = CosmosClient(HOST, {'masterKey': MASTER_KEY})
db = client.get_database_client(DATABASE_ID)
container_prueba = db.get_container_client("Prubea")
container_Mtemp = db.get_container_client("MTemp")
container_Btemp = db.get_container_client("BTemp")
container_Ttemp = db.get_container_client("TTemp")

# Schedules
M_schedule = pd.read_csv("Web_scraper/Data2022_2/mechatronics_schedules.csv").dropna()
B_schedule = pd.read_csv("Web_scraper/Data2022_2/bionics_schedules.csv").dropna()
T_schedule = pd.read_csv("Web_scraper/Data2022_2/telematics_schedules.csv").dropna()
columns_name = ["Grupo", "Semestre", "Cupo", "Inscritos", "Disponibles", "Asignatura", "id"]

for career_df in [M_schedule, B_schedule, T_schedule]:
    career_df = create_id(career_df)

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

################ here would be the while loop ###############
# while True:
# Going to the ocupation page in the same session
driver.get('https://www.saes.upiita.ipn.mx/Academica/Ocupabilidad_grupos.aspx')

# Selecting actual school period
driver.find_element_by_id("ctl00_mainCopy_rblEsquema_0").click()

# Iterating over the 3 carreers
careers = {"M" : [], "B": [], "T": []}
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
        # appending the ID
        row.append(course_str + row[0])
        # appending the course
        careers[career].append(row)

M_ocupability = pd.DataFrame(careers["M"], columns=columns_name)
B_ocupability = pd.DataFrame(careers["B"], columns=columns_name)
T_ocupability = pd.DataFrame(careers["T"], columns=columns_name)

careers_to_api = {"M": (M_schedule, M_ocupability), "B": (B_schedule, B_ocupability), "T": (T_schedule, T_ocupability)}

for career_letter in careers_to_api.keys():
    career_full = concat_sort(careers_to_api[career_letter][0], careers_to_api[career_letter][1])
    to_cosmos_db(career_full, career_letter, container_prueba)

    # time.sleep(10)