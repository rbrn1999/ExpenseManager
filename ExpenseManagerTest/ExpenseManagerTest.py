import pytest
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def fixture(): #set-up and tear-down for each test
    server = HTTPServer(('localhost', 5566), SimpleHTTPRequestHandler)
    thread = Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://localhost:5566")

    yield driver

    driver.close()
    server.shutdown()
    thread.join()

def test_inCome_1(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薪資")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("20")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/13")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0)
    datepicker = driver.find_element(By.ID, "date-from")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/01")
    datepicker = driver.find_element(By.ID, "date-to")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/31")
    income_row = driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薪資", "20", "100.00"]

    detail_row = driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
    items = detail_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items[1:-1]] == ["薪資", "收入", "20", "2022/10/13"]

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額:20"


if __name__ == '__main__':
    pytest.main()