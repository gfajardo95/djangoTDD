from selenium import webdriver
import unittest  # from the standard library


# Notes about unittest:
# setup() and tearDown() are special methods that get run before and after every test, so they're a bit like
# the try/except or try/finally
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # methods that begin with "test_" are treated as tests to be run the by unittest runner ( unittest.main() )
    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes check out the home page of the to-do app
        self.browser.get('http://localhost:8000')

        # User notices the header and title mention To Do Lists
        # assert's second parameter is the error message
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is invited to add a to-do list item straight away

        # User types in the text box a to-do

        # When User hits enter, the page updates and shows the newly added to-do list item

        # There is still a text box inviting the User to add another item
        # So, the user enters another and sees it update on the screen, adding the item to
        # the previous list

        # A url is generated where the User can go to and see their created list


if __name__ == '__main__':
    unittest.main(warnings='ignore')
