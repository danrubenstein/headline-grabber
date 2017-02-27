import re 
from constants import message_full_regex, message_default_regex
from api import get_google_search_result

class IncomingMessage:
	''' 
	Acceptable requests against the bot are defined against a basic syntax

	<sort_by><count_headlines><source>

	Where

		<sort_by> := ['latest', 'top'] 
		<num_requested> := a non-zero positive integer
		<source> := a source name.

	Notes:

	- Queries are automatically converted to lower case.
	- If either of the first parameters are not defined, the incoming message 
	will take the latest five stories from newsapi. 
	'''
	def __init__(self, message):
		self.message = message.lower()
		self.message_parsed = False

		# Defaults
		self.message_parse_ok = True
		self.sort_by = "top"
		self.num_requested = 5 
		self.default_parse = False
		self.source_requested = None
		
		p = re.compile(message_full_regex)
		m = p.match(self.message) 

		if m:
			self.sort_by = self.message.split()[0]
			self.num_requested = int(self.message.split()[1])
			self.source_requested = " ".join(self.message.split()[2:])
		else: 
			p = re.compile(message_default_regex)
			m = p.match(self.message)
			if m:
				self.source_requested = self.message
				self.default_parse = True
			else:
				self.message_parse_ok = False

	def is_help(self):
		if "help" in self.message:
			return True
		else:
			return False

class NewsResponse:
	
	'''
	Crafted off of acceptable incoming messages only 
	'''

	def __init__(self, incoming_message):
		
		# Defaults
		self.source_found = False 
		self.articles_requested = False 
		self.articles_found = False 



