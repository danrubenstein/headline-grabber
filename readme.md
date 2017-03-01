# Headline Grabber:

This is a Flask application built off of [this tutorial](https://blog.hartleybrody.com/fb-messenger-bot/) that takes the headlines from a bunch of places and puts them in front of you. It's currently implemented both as a Facebook bot (Headline Grabber) and as a command line application. 

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

### Protocols

Currently, Headline Grabber exists as a Facebook bot, and as a command line utility. 


#### As a command line utility 

curl -o client.py

```
~: $ news nyt
1) Fact Check: Trump’s First Address to Congress: http://www.nytimes.com/interactive/2017/02/28/us/politics/fact-check-trump-congress-address.html?src=rec&amp;recp=0
2) Trump, in Optimistic Address, Asks Congress to End ‘Trivial Fights’: http://www.nytimes.com/2017/02/28/us/politics/trump-address-congress.html?src=rec&amp;recp=1
3) Colon and Rectal Cancers Rising in Young People: http://www.nytimes.com/2017/02/28/well/live/colon-and-rectal-cancers-rising-in-young-people.html?src=rec&amp;recp=2
4) Trump’s Speech to Congress and Democrats’ Response: Video and Analysis: http://www.nytimes.com/interactive/2017/02/28/us/politics/trump-congress-address-live-video-analysis.html?src=rec&amp;recp=3
5) Trump Addressed Joint Session of Congress For the First Time: http://www.nytimes.com/2017/02/28/us/politics/trump-address-joint-session-congress.html?src=rec&amp;recp=4
~: $ 
```

#### Facebook Bot

#### Dependencies 

##### Client
- [Requests][http://docs.python-requests.org/en/master/]
##### Server
- See [requirements.txt][./requirements.txt]

