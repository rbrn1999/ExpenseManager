import pytest
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def fixture(): #set-up and tear-down for each test
    server = HTTPServer(('localhost', 5566), SimpleHTTPRequestHandler)
    thread = Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) #這行是不是不用加？？明細好像收入跟支出會一起看
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
    assert total_money.text == "總額：20"

def test_inCome_2(fixture):
    driver = fixture
    u_item = driver.find_element(By.XPATH, '//*[@id="app"]/div/div')
    u_item.click()
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("1500")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/15")
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
    assert [item.text for item in items] == ["工作", "1500", "100.00"]

    detail_row = driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
    items = detail_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items[1:-1]] == ["工作", "收入", "1500", "2022/10/15"]    

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：1500"

def test_expenses_3(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薯條")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("55")
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
    income_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薯條", "55", "100.00"]

    detail_row = driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
    items = detail_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items[1:-1]] == ["薯條", "支出", "55", "2022/10/13"]

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：-55"

def test_expenses_4(fixture):
    driver = fixture
    choose_expense_item = driver.find_element(By.ID, "two")
    choose_expense_item.click()
    eat_common_item = driver.find_element(By.XPATH, '//*[@id="app"]/div/div')
    eat_common_item.click()
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("120")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/15")
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
    income_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["吃飯", "120", "100.00"]

    detail_row = driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
    items = detail_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items[1:-1]] == ["吃飯", "支出", "120", "2022/10/15"]

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：-120"

def test_addCommonIncomeItem(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("獎學金")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    com_button = driver.find_element(By.ID, "add-to-usual-button")
    com_button.click()
    
    com_items = driver.find_elements(By.CLASS_NAME, 'u-item')
    assert "獎學金" in [item.text for item in com_items]
    # 可可
    # com_item = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]')
    # assert com_item.text == "獎學金"
    

def test_addCommonExpenseItem(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("衣服")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    com_button = driver.find_element(By.ID, "add-to-usual-button")
    com_button.click()
    
    com_items = driver.find_elements(By.CLASS_NAME, 'u-item')
    assert "衣服" in [item.text for item in com_items]
    # 不可
    # com_item = driver.find_element(By.XPATH, '//*[@id="app"]/div/div')
    # assert com_item.text == "衣服"

# 注意一下可能有錯
def test_recentOption7days(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薪資")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("1200")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/13")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.clear()
    name_input.send_keys("衣服")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.clear()
    amount_input.send_keys("320")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/15")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()

    Select(driver.find_element(By.ID, "recent-days-selector")).select_by_index(0) # 最近7天
    expense_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = expense_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["衣服", "320", "100.00"]
    income_row = driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薪資", "1200", "100.00"]

    detail_table = driver.find_element(By.CLASS_NAME, 'detail_table')
    rows = detail_table.find_elements(By.TAG_NAME, "tr")
    rows = [[item.text for item in row.find_elements(By.TAG_NAME, "td")[1:-1]] for row in rows]    
    assert ["薪資", "收入", "1200", "2022/10/13"] in rows
    assert ["衣服", "支出", "320", "2022/10/15"] in rows
    # 這個也可可
    # detail_row = driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
    # items = detail_row.find_elements(By.TAG_NAME, "td")
    # assert [item.text for item in items[1:-1]] == ["衣服", "支出", "320", "2022/10/15"]

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：880"

def test_recentOption1Month(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薪資")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("1200")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/13")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.clear()
    name_input.send_keys("衣服")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.clear()
    amount_input.send_keys("320")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/15")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()

    Select(driver.find_element(By.ID, "recent-days-selector")).select_by_index(1) # 最近1個月
    expense_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = expense_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["衣服", "320", "100.00"]
    income_row = driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薪資", "1200", "100.00"]

    detail_table = driver.find_element(By.CLASS_NAME, 'detail_table')
    rows = detail_table.find_elements(By.TAG_NAME, "tr")
    rows = [[item.text for item in row.find_elements(By.TAG_NAME, "td")[1:-1]] for row in rows]
    assert ["薪資", "收入", "1200", "2022/10/13"] in rows
    assert ["衣服", "支出", "320", "2022/10/15"] in rows

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：880"

def test_recentOption3Months(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薪資")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("1200")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/13")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.clear()
    name_input.send_keys("衣服")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.clear()
    amount_input.send_keys("320")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/15")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()

    Select(driver.find_element(By.ID, "recent-days-selector")).select_by_index(2) # 最近3個月
    expense_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = expense_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["衣服", "320", "100.00"]
    income_row = driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薪資", "1200", "100.00"]

    detail_table = driver.find_element(By.CLASS_NAME, 'detail_table')
    rows = detail_table.find_elements(By.TAG_NAME, "tr")
    rows = [[item.text for item in row.find_elements(By.TAG_NAME, "td")[1:-1]] for row in rows]
    assert ["薪資", "收入", "1200", "2022/10/13"] in rows
    assert ["衣服", "支出", "320", "2022/10/15"] in rows

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：880"

def test_settingDateRange(fixture):
    driver = fixture
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.send_keys("薪資")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.send_keys("1200")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.send_keys("2022/10/13")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()
    name_input = driver.find_element(By.ID, "name-input")
    name_input.click()
    name_input.clear()
    name_input.send_keys("衣服")
    Select(driver.find_element(By.ID, "record-type-selector")).select_by_index(1) # 支出
    amount_input = driver.find_element(By.ID, "amount-input")
    amount_input.click()
    amount_input.clear()
    amount_input.send_keys("320")
    datepicker = driver.find_element(By.ID, "datepicker")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/15")
    detail_button = driver.find_element(By.ID, "add-to-detail-button")
    detail_button.click()

    datepicker = driver.find_element(By.ID, "date-from")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/13")
    datepicker = driver.find_element(By.ID, "date-to")
    datepicker.click()
    datepicker.clear()
    datepicker.send_keys("2022/10/15")

    expense_row = driver.find_element(By.XPATH, '//*[@id="expense-table"]/tbody/tr[2]')
    items = expense_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["衣服", "320", "100.00"]
    income_row = driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
    items = income_row.find_elements(By.TAG_NAME, "td")
    assert [item.text for item in items] == ["薪資", "1200", "100.00"]

    detail_table = driver.find_element(By.CLASS_NAME, 'detail_table')
    rows = detail_table.find_elements(By.TAG_NAME, "tr")
    rows = [[item.text for item in row.find_elements(By.TAG_NAME, "td")[1:-1]] for row in rows]
    assert ["薪資", "收入", "1200", "2022/10/13"] in rows
    assert ["衣服", "支出", "320", "2022/10/15"] in rows

    total_money = driver.find_element(By.ID, "total_money")
    assert total_money.text == "總額：880"

def test_clearDate(fixture):
    driver = fixture
    clear_buttom = driver.find_element(By.XPATH, '//*[@id="app"]/input[3]')
    clear_buttom.click()

    datepickerfrom = driver.find_element(By.ID, "date-from")
    assert datepickerfrom.text == ""
    datepickerto = driver.find_element(By.ID, "date-to")
    assert datepickerto.text == ""

if __name__ == '__main__':
    pytest.main()