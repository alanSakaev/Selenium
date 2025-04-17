from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def web_calculator_with_delay(delay_param, num1_param, num2_param, operation_param):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    driver.maximize_window()
    
    # Задержка вычисления
    input_delay = driver.find_element(By.ID, "delay")
    input_delay.clear()
    input_delay.send_keys(f"{delay_param}")

    # Набор первого числа
    for digit in str(num1_param):
        driver.find_element(By.XPATH, f"//span[contains(@class, 'btn') and text()='{digit}']").click()
    
    # Набор математической операции
    driver.find_element(By.XPATH, f"//span[contains(@class, 'btn') and text()='{operation_param}']").click()
    
    # Набор второго числа
    for digit in str(num2_param):
        driver.find_element(By.XPATH, f"//span[contains(@class, 'btn') and text()='{digit}']").click()
    
    driver.find_element(By.XPATH, "//span[contains(@class, 'btn') and text()='=']").click()

    # Содержимое экрана до отображения на нем результата вычисления
    initial_value = driver.find_element(By.CSS_SELECTOR, "div.screen").text

    # Ожидание смены содержимого экрана в соответствии с задержкой вычисления
    wait = WebDriverWait(driver, delay_param)
    wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div.screen").text != initial_value)

    return driver.find_element(By.CSS_SELECTOR, "div.screen").text

@pytest.mark.parametrize("delay_param, num1_param, num2_param, operation_param, web_calculator_with_expectation_ret",
                         [(1,10,12,'+',22),
                          (2,25,5,'-',20),
                          (5,10,4,'x',40),
                          (3,12345679,8,'x',98765432),
                          (4,100,200,'-',-100)
                          ])
def test_web_calculator_with_expectation(delay_param, num1_param, num2_param, operation_param, web_calculator_with_expectation_ret):
    result = web_calculator_with_delay(delay_param, num1_param, num2_param, operation_param)
    assert result == str(web_calculator_with_expectation_ret)
