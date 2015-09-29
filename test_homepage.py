import os
from unittest import TestCase
import re
from selenium import webdriver


def get_docker_host():
    docker_host = os.getenv('DOCKER_HOST', None)
    if docker_host:
        # docker_host is something like tcp://192.168.99.100:2376
        # so, let's extract the IP address
        match = re.match('^tcp://(.*):\d+$', docker_host)
        if match:
            return match.group(1)

    raise ValueError("Weird value for DOCKER_HOST, expected something like tcp://IP:PORT")


base_url = 'http://' + get_docker_host() + ':8080'


class Homepage(object):

    def __init__(self, driver):
        self.driver = driver

    def get_title_element(self):
        return self.driver.find_element_by_css_selector("h1")


class AddSurprisePage(object):

    def __init__(self, driver):
        self.driver = driver

    def get_form_el(self):
        return self.driver.find_element_by_css_selector("form")

    def get_link_input(self):
        return self.driver.find_element_by_css_selector("form input#id_link")

    def get_description_input(self):
        return self.driver.find_element_by_css_selector("form textarea#id_description")

    def get_submit_button(self):
        return self.driver.find_element_by_css_selector("form input[type=submit]")


class AddSurpriseConfirmationPage(object):

    def __init__(self, driver):
        self.driver = driver

    def get_success_message(self):
        return self.driver.find_element_by_css_selector(".alert-success")


class BasicPagesTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_homepage(self):
        self.driver.get(base_url)
        page = Homepage(self.driver)

        self.assertIsNotNone(page.get_title_element())
        self.assertEqual(page.get_title_element().text, "Welcome")

    def test_add_surprise_structure(self):
        self.driver.get(base_url + '/add-surprise')
        page = AddSurprisePage(self.driver)

        self.assertIsNotNone(page.get_form_el())
        self.assertIsNotNone(page.get_link_input())
        self.assertIsNotNone(page.get_description_input())
        self.assertIsNotNone(page.get_submit_button())

    def test_add_surprise_action(self):
        self.driver.get(base_url + '/add-surprise')
        page = AddSurprisePage(self.driver)

        page.get_link_input().send_keys("http://livecoding.tv/publysher")
        page.get_description_input().send_keys("A really cool site")
        page.get_submit_button().click()

        page = AddSurpriseConfirmationPage(self.driver)
        msg = page.get_success_message()
        self.assertIsNotNone(msg)
        self.assertRegex(msg.text, r'Your surprise has been added')
