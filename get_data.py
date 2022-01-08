from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import csv

user = "2019640120"
password = "aA:12345"

filter_data =[
{
	'periodo': "5",
	"turno": "M",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "4",
	"turno": "M",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "2",
	"turno": "M",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "3",
	"turno": "M",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "4",
	"turno": "V",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "2",
	"turno": "V",
	"grupo": "Todo",
	"carrera": "Bionica"
},{	
	'periodo': "3",
	"turno": "V",
	"grupo": "Todo",
	"carrera": "Bionica"
},{
	'periodo': "5",
	"turno": "V",
	"grupo": "Todo",
	"carrera": "Bionica"
}]
driver = webdriver.Firefox()

#LOGIN

driver.get('https://www.saes.upiita.ipn.mx/')

user_in = driver.find_element_by_css_selector('#ctl00_leftColumn_LoginUser_UserName')
pas_in = driver.find_element_by_css_selector('.passwordEntry')
captcha_in = driver.find_element_by_css_selector("#ctl00_leftColumn_LoginUser_CaptchaCodeTextBox")

user_in.send_keys(user)
pas_in.send_keys(password)
captcha_in.send_keys(input("Captcha:"))
pas_in.send_keys(Keys.RETURN)


#Go to academia


input("Go to academia Is it ready?")

def get_rows(inf_d):

	#Group info

	period = Select(driver.find_element_by_css_selector('#ctl00_mainCopy_Filtro_lsNoPeriodos'))
	period.select_by_value(inf_d["periodo"])

	shift = Select(driver.find_element_by_css_selector('#ctl00_mainCopy_Filtro_cboTurno'))
	shift.select_by_value(inf_d["turno"])

	group = Select(driver.find_element_by_css_selector('#ctl00_mainCopy_lsSecuencias'))
	group.select_by_value(inf_d["grupo"])

	input("Is there the data ready?")
	#Geting data

	table = driver.find_element_by_css_selector('#ctl00_mainCopy_dbgHorarios')

	rows = table.find_elements(By.TAG_NAME, "tr")

	return(rows[1:])



data=[]
for inf_d in filter_data:
	print(inf_d)
	data_section=[]
	for row in get_rows(inf_d):
		row_info = []
		for col in row.find_elements(By.TAG_NAME, "td"):
			row_info.append(col.text)
		data_section.append(row_info)
	data.append(data_section)
print(data[1])
outfile = open("data_saes_1M",'wb')
pickle.dump(data,outfile)
outfile.close()



