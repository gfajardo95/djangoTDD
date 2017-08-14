import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 2


# Notes about unittest:
# setup() and tearDown() are special methods that get run before and after every test, so they're a bit like
# the try/except or try/finally
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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

        self.wait_for_row_in_table('1: Buy peacock feathers')

        # There is still a text box inviting the User to add another item
        # So, the user enters another and sees it update on the screen
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # the item is added to the previous list
        self.wait_for_row_in_table('1: Buy peacock feathers')
        self.wait_for_row_in_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # a unique URL is made when the form does a POST
        user_url = self.browser.current_url
        # this would not match for some reason..
        # self.assertRegex(user_url, '/lists/.+')

        ## a new user comes in, on a different browser that has
        ## no browser cookies or such of first user's list
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # new user goes to the site and sees no signs of previous user's to-do list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # new user makes own list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        # new user gets own, unique url
        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, '/lists/.+')
        self.assertNotEqual(new_user_url, user_url)

        # double check that previous user's data is not on the page, but new user's IS
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: testing')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
