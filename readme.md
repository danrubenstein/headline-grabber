# Headline Grabber:

This is a Flask application built off of [this tutorial](https://blog.hartleybrody.com/fb-messenger-bot/) that takes the headlines from a bunch of places and puts them in front of you. It's currently implemented both as a Facebook bot (Headline Grabber) and as a command line application. 

This data is taken from [newsapi][https://newsapi.org/].

### Using Headline Grabber 

Queries against Headline Grabber are as follows:

```
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

```

There are also "sources" and "help" commands.

### Protocols

Currently, Headline Grabber exists as a Facebook bot. 

A command line utility is in development.

#### Facebook Bot

- Screen caps to come

#### Dependencies 

##### Client
- [Requests][http://docs.python-requests.org/en/master/]

##### Server
- See [requirements.txt][./requirements.txt]

### To-dos

- Testing. Lots of testing.
- Implementation of command line utility.

