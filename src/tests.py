import unittest
from api import get_google_search_result
from message import IncomingMessage

class test_google_search_query(unittest.TestCase):

	def test_search_length(self):
		print("here")
		self.assertEqual(len(get_google_search_result("apple")), 5)

	def test_search_returns_200(self):
		print("here")
		self.assertNotEqual(get_google_search_result("apple"), None)

class message_validity_tests(unittest.TestCase):

	def test_full_message_valid(self):
		msg = IncomingMessage("top 5 nyt")
		self.assertTrue(msg.message_parse_ok)

	def test_full_message_valid_source(self):
		msg = IncomingMessage("top 5 nyt")
		self.assertEqual("nyt", msg.source_requested)

	def test_full_message_valid_sort(self):
		msg = IncomingMessage("Top 5 NYT")
		self.assertEqual("top", msg.sort_by)

	def test_full_message_valid_count(self):
		msg = IncomingMessage("Top 5 NYT")
		self.assertEqual(5, msg.num_requested)

	def message_sort_not_supported(self):
		pass 

	def special_characters_message(self):
		pass 

	def whitespace_message(self):
		pass 

	def message_help_recognized(self):
		pass
	

if __name__ == '__main__':
    unittest.main()