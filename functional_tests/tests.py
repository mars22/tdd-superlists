from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.close()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), 'Enter a to-do item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        first_users_list_url = self.browser.current_url
        self.assertRegex(first_users_list_url, '/lists/.+/')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # second user cant see first user list

        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # second user create his list

        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys('item 1')
        input_box.send_keys(Keys.ENTER)

        second_users_list_url = self.browser.current_url
        self.assertRegex(second_users_list_url, '/lists/.+/')
        self.assertNotEqual(first_users_list_url, second_users_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('item 1', page_text)






        self.fail('Finish the test!')


