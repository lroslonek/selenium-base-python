import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.BasePage import BasePage
from pages.ResultsPage import ResultsPage
from pages.SignInPage import SignInPage
from utils.WebdriverWaits import WebdriverWaits
from utils.YamlReader import read_configuration


class MainPage(BasePage):

    __country_modal_locator = (By.XPATH, '//*[@id="Form"]/div[7]/div/div/div/button')
    __ad_modal_locator = (By.XPATH, '//*[@id="advertPopup"]/div/div/div[1]/button')
    __search_box_locator = (By.ID, 'txtSearch')

    _BASE_URL = read_configuration('base-url')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self._BASE_URL)
        logging.info("SportsDirect page opened")

    def search_for_phrase(self, phrase):
        search_box = self.driver.find_element(*self.__search_box_locator)
        search_box.send_keys(phrase)
        search_box.send_keys(Keys.RETURN)
        return ResultsPage(self.driver)

    def dismiss_modals(self):
        self.__dismiss_advert_modal()
        self.__dismiss_country_modal()

    def go_to_sign_in_page(self):
        self.driver.find_element(*self._sign_in_locator).click()
        return SignInPage(self.driver)

    def __dismiss_advert_modal(self):
        try:
            WebdriverWaits.wait_for_element_visible(self.driver, 3, self.__ad_modal_locator).click()
        except TimeoutException:
            logging.warning("no advert modal...")  # advert modal not always present

    def __dismiss_country_modal(self):
        try:
            WebdriverWaits.wait_for_element_visible(self.driver, 3, self.__country_modal_locator).click()
        except TimeoutException:
            logging.warning("no country modal...")  # country modal not always present
