from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import pytest

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def filling_in_fields(
    first_name_param="",
    last_name_param="",
    address_param="",
    zip_code_param="",
    city_param="",
    country_param="",
    email_param="",
    phone_number_param="",
    job_position_param="",
    company_param=""
    ):
    
    values_to_fill = {
        'first-name': first_name_param,
        'last-name': last_name_param,
        'address': address_param,
        'zip-code': zip_code_param,
        'city': city_param,
        'country': country_param,
        'e-mail': email_param,
        'phone': phone_number_param,
        'job-position': job_position_param,
        'company': company_param,
    }
    
    driver.get('https://bonigarcia.dev/selenium-webdriver-java/data-types.html')
    driver.maximize_window()
    
    inputs_elements = driver.find_elements(By.CSS_SELECTOR, "input")
    
    #Заполнение полей по атрибуту name
    for input_element in inputs_elements:
        input_element_attr = input_element.get_attribute("name")
        if input_element_attr in values_to_fill:
            input_element.send_keys(values_to_fill[input_element_attr])

    # Нажатие на Submit
    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
    )
    driver.execute_script("""
    arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});
    """, submit_button)
    submit_button.click()
    
    # # Ожидание, пока на странице не появятся элементы с "div.alert"
    # WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
    # )
    # #Массив заполненных полей
    # filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    
    # return filled_inputs

@pytest.mark.parametrize("""
    first_name_param,
    last_name_param,
    address_param,
    zip_code_param,
    city_param,
    country_param,
    email_param,
    phone_number_param,
    job_position_param,
    company_param,
    first_name_param_ret,
    last_name_param_ret,
    address_param_ret,
    zip_code_param_ret,
    city_param_ret,
    country_param_ret,
    email_param_ret,
    phone_number_param_ret,
    job_position_param_ret,
    company_param_ret""",
    [(
        "Иван",
        "Петров",
        "",
        "",
        "",
        "",
        "",
        "",
        "QA",
        "Google",
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        True,
    ),
     (
        "Иван",
        "Петров",
        "Ленина,66",
        "123",
        "Москва",
        "Россия",
        "test@yandex.ru",
        "+7(999)888-12-34",
        "QA",
        "Google",
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
     ),
     (
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
     )])
def test_filling_in_fields(
    first_name_param,
    last_name_param,
    address_param,
    zip_code_param,
    city_param,
    country_param,
    email_param,
    phone_number_param,
    job_position_param,
    company_param,
    first_name_param_ret,
    last_name_param_ret,
    address_param_ret,
    zip_code_param_ret,
    city_param_ret,
    country_param_ret,
    email_param_ret,
    phone_number_param_ret,
    job_position_param_ret,
    company_param_ret
):
    values_to_check = {
    'first-name': first_name_param_ret,
    'last-name': last_name_param_ret,
    'address': address_param_ret,
    'zip-code': zip_code_param_ret,
    'city': city_param_ret,
    'country': country_param_ret,
    'e-mail': email_param_ret,
    'phone': phone_number_param_ret,
    'job-position': job_position_param_ret,
    'company': company_param_ret,
    }
    
    filling_in_fields(
        first_name_param,
        last_name_param,
        address_param,
        zip_code_param,
        city_param,
        country_param,
        email_param,
        phone_number_param,
        job_position_param,
        company_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_input in filled_inputs:
            filled_input_attr_id = filled_input.get_attribute('id')
            if filled_input_attr_id in values_to_check:
                filled_input_attr_class = filled_input.get_attribute('class')
                if "alert-success" in filled_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == values_to_check[filled_input_attr_id]

#Тест отдельно для поля First name
@pytest.mark.parametrize("first_name_param, filled_in_first_name_ret",
                         [("First name",True),("",False)])
def test_filing_in_first_name(first_name_param, filled_in_first_name_ret):
    filling_in_fields(first_name_param=first_name_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "first-name" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_first_name_ret

#Тест отдельно для поля Last name
@pytest.mark.parametrize("last_name_param, filled_in_last_name_ret",
                         [("Last name",True),("",False)])
def test_filing_in_last_name(last_name_param, filled_in_last_name_ret):
    filling_in_fields(last_name_param=last_name_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "last-name" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_last_name_ret
            
#Тест отдельно для поля Address
@pytest.mark.parametrize("address_param, filled_in_address_ret",
                         [("Address",True),("",False)])
def test_filing_in_address(address_param, filled_in_address_ret):
    filling_in_fields(address_param=address_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "address" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_address_ret
            
#Тест отдельно для поля Zip code
@pytest.mark.parametrize("zip_code_param, filled_in_zip_code_ret",
                         [("Zip code",True),("",False)])
def test_filing_in_zip_code(zip_code_param, filled_in_zip_code_ret):
    filling_in_fields(zip_code_param=zip_code_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "zip-code" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_zip_code_ret
            
#Тест отдельно для поля City
@pytest.mark.parametrize("city_param, filled_in_city_ret",
                         [("City",True),("",False)])
def test_filing_in_city(city_param, filled_in_city_ret):
    filling_in_fields(city_param=city_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "city" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_city_ret
            
#Тест отдельно для поля Country
@pytest.mark.parametrize("country_param, filled_in_country_ret",
                         [("Country",True),("",False)])
def test_filing_in_country(country_param, filled_in_country_ret):
    filling_in_fields(country_param=country_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "country" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_country_ret
            
#Тест отдельно для поля E-mail
@pytest.mark.parametrize("email_param, filled_in_email_ret",
                         [("email@mail.ru",True),("email","Invalid input")])
def test_filing_in_email(email_param, filled_in_email_ret):
    filling_in_fields(email_param=email_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    print(len(filled_inputs))
    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "e-mail" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                is_success = "alert-success" in filled_in_input_attr_class
                assert is_success == filled_in_email_ret
    else:
        assert "Invalid input" == filled_in_email_ret

#Тест отдельно для поля Phone number
@pytest.mark.parametrize("phone_param, filled_in_phone_ret",
                         [("Phone number",True),("",False)])
def test_filing_in_phone_number(phone_param, filled_in_phone_ret):
    filling_in_fields(phone_number_param=phone_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "phone" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_phone_ret
            
#Тест отдельно для поля Job position
@pytest.mark.parametrize("job_position_param, filled_in_job_position_ret",
                         [("Job position",True),("",False)])
def test_filing_in_job_position(job_position_param, filled_in_job_position_ret):
    filling_in_fields(job_position_param=job_position_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "job-position" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_job_position_ret
            
#Тест отдельно для поля Company
@pytest.mark.parametrize("company_param, filled_in_company_ret",
                         [("Company",True),("",False)])
def test_filing_in_company(company_param, filled_in_company_ret):
    filling_in_fields(company_param=company_param)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
        )
        #Массив заполненных полей
        filled_inputs = driver.find_elements(By.CSS_SELECTOR, "div.alert")
    except TimeoutException:
        filled_inputs = []

    if len(filled_inputs) != 0:
        for filled_in_input in filled_inputs:
            filled_in_input_attr_id = filled_in_input.get_attribute("id")
            if "company" in filled_in_input_attr_id:
                filled_in_input_attr_class = filled_in_input.get_attribute("class")
                if "alert-success" in filled_in_input_attr_class:
                    is_success = True
                else:
                    is_success = False
                assert is_success == filled_in_company_ret
