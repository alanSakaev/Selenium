driver.implicitly_wait(10)

screen_answer = driver.find_element(By.CSS_SELECTOR, "div.screen")
print(screen_answer.text())