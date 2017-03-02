import re 
from constants import message_full_regex, message_default_regex

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
        '''
        if "help" in query
        '''
        return bool("help" in self.message)
        
    def is_sources(self):
        '''
        if "source" in query
        '''
        return bool("source" in self.message)
            



