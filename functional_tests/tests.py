import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest  # from the standard library


# Notes about unittest:
# setup() and tearDown() are special methods that get run before and after every test, so they're a bit like
# the try/except or try/finally
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # methods that begin with "test_" are treated as tests to be run the by unittest runner ( unittest.main() )
    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes check out the home page of the to-do app
        self.browser.get(self.live_server_url)

        # User notices the header and title mention To Do Lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to add a to-do list item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types in the text box a to-do: "Buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')

        # When User hits enter, the page updates and shows the newly added to-do list with
        # "1: Buy peacock feathers" added to it
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_table('1: Buy peacock feathers')

        # There is still a text box inviting the User to add another item
        # So, the user enters another and sees it update on the screen
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # the item is added to the previous list
        self.check_for_row_in_table('1: Buy peacock feathers')
        self.check_for_row_in_table('2: Use peacock feathers to make a fly')

        # A url is generated where the User can go to and see their created list
        self.fail('Finish the test!')
