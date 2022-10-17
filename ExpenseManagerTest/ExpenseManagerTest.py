import unittest
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ExpenseManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = HTTPServer(('localhost', 5566), SimpleHTTPRequestHandler)
        thread = Thread(target = self.server.serve_forever)
        thread.daemon = True
        thread.start()

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://localhost:5566")
        return super().setUp()
    def tearDown(self) -> None:
        self.driver.close()
        self.server.shutdown()
        return super().tearDown()

    def test_inCome_1(self):
        name_input = self.driver.find_element(By.ID, "name-input")
        name_input.click()
        name_input.send_keys("薪資")
        Select(self.driver.find_element(By.ID, "record-type-selector")).select_by_index(0) # 收入
        amount_input = self.driver.find_element(By.ID, "amount-input")
        amount_input.click()
        amount_input.send_keys("20")
        datepicker = self.driver.find_element(By.ID, "datepicker")
        datepicker.click()
        datepicker.send_keys("2022/10/13")
        detail_button = self.driver.find_element(By.ID, "add-to-detail-button")
        detail_button.click()
        Select(self.driver.find_element(By.ID, "record-type-selector")).select_by_index(0)
        datepicker = self.driver.find_element(By.ID, "date-from")
        datepicker.click()
        datepicker.clear()
        datepicker.send_keys("2022/10/01")
        datepicker = self.driver.find_element(By.ID, "date-to")
        datepicker.click()
        datepicker.clear()
        datepicker.send_keys("2022/10/31")
        income_row = self.driver.find_element(By.XPATH, '//*[@id="income-table"]/tbody/tr[2]')
        items = income_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual([item.text for item in items], ["薪資", "20", "100.00"])

        detail_row = self.driver.find_element(By.XPATH, '//*[@id="app"]/table[4]/tbody/tr')
        items = detail_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual([item.text for item in items[1:-1]], ["薪資", "收入", "20", "2022/10/13"])

if __name__ == '__main__':
    unittest.main()