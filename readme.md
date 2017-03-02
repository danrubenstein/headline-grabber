# Headline Grabber:

## Intro 

This is a Flask application built off of [this tutorial](https://blog.hartleybrody.com/fb-messenger-bot/) that takes the headlines from a bunch of places and puts them in front of you. It's currently implemented both as a Facebook bot (Headline Grabber) and as a command line application. 

Information is taken from the [newsapi](https://newsapi.org/) API.

## Using Headline Grabber 

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

### [Facebook Bot](https://www.facebook.com/Headline-Grabber-248841565559881)

You can interact with Headline Grabber by sending it a message. There's no present intention of using the Facebook page other than for its chat functionality.

- Getting Headlines
	![Example](/images/example.png)
- Asking for help
	![Help](/images/help.png)
- Listing sources
	![Sources](/images/sources.png)

### [Command Line Utility](./client.py)

The same queries that are made in the Facebook bot can also be made from the terminal. I've taken to calling the command `news`, so one can use the following script to get this from the command line.

```
curl -o ~/client.py https://raw.githubusercontent.com/danrubenstein/headline-grabber/master/client.py
echo "alias news=~/client.py" >> ./.bash_profile
```

Usage is pretty much the same:

```
$ news top 4 nyt
1) Obama Administration Rushed to Preserve Intelligence of Russian Election Hacking: http://www.nytimes.com/2017/03/01/us/politics/obama-trump-russia-election-hacking.html?src=rec&amp;recp=0
2) Jeff Sessions Recuses Himself From Russia Inquiry: http://www.nytimes.com/2017/03/02/us/politics/jeff-sessions-russia-trump-investigation-democrats.html?src=rec&amp;recp=1
3) Fact Check: Trump’s First Address to Congress: http://www.nytimes.com/interactive/2017/02/28/us/politics/fact-check-trump-congress-address.html?src=rec&amp;recp=2
4) 5 Key Takeaways From President Trump’s Speech: http://www.nytimes.com/2017/03/01/us/politics/takeaways-president-trump-speech-congress.html?src=rec&amp;recp=3
$
```

## Dependencies 

### Client
- [Python 3](https://www.python.org/downloads/)
- [Requests](http://docs.python-requests.org/en/master/)

### Server
- See [requirements.txt](./requirements.txt)

## To-dos

- Testing. Lots of testing.

