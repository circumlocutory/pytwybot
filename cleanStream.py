#This script follows a user's Twitter stream and messages them when they tweet.
#The interval between tweets can be adjusted using the sleep() function

from twython import TwythonStreamer, Twython
from datetime import date
import random
import time

#auth.py is the second file, containing your dev.twitter.com credentials
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

def timediff():
    #timediff() gets the difference between the previous launch date and today
    #d0 should be formatted yyyy/m//d
    #Example date added
    d0 = date(2017, 1, 3)
    d1 = date.today()
    result = d1 - d0
    result = result.days
    return result

#Populate this messages array with various openers. A few examples are included for inspiration    
messages = [
    "Get back to work. ",
    "Stop this. ",
    "Finish the game. ",
    "We're waiting. ",
    "Back to development! ",
    "You're talking nonsense. ",
    "It's all irrelevant. ",
    "The time is short. ",
    "Focus on the task at hand. "
    ]

#This block performs initial setup when the script first runs
flavor = random.choice(messages)
result = timediff()
#message must begin with the Twitter handle of whom you wish to tweet
#after flavor, add gameTitle
message = "@someonesTwitterHandle "+ flavor + "gameTitle shipped " + str(result) + " days ago!"
lastMessage = message
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

def buildTweet(messages):
    #buildTweet() creates the message for you, and checks it isn't the same as your last message, to avoid flagging as spam
    global lastMessage
    flavor = random.choice(messages)
    result = timediff()
    message = "@someonesTwitterHandle "+ flavor + "gameTitle shipped " + str(result) + " days ago!"
    #if lastMessage == message, then buildTweet() again
    if lastMessage == message:
        buildTweet(messages)
    return message

#This is the real focus of the bot's functionality, where the magic happens
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            try:
                username = data['user']['screen_name']
                tweet = data['text']
                print("@%s: %s" % (username, tweet))
                #Bot only tweets if user has tweeted
                #username == 'someonesTwitterHandle'
                if username == 'someonesTwitterHandle':
                    message = buildTweet(messages)
                    print("Built tweet")
                    #waits 30 seconds before tweeting, for a more natural cadence
                    time.sleep(30)
                    twitter.update_status(status=message)
                    print("Tweeted: %s" % message)
                    global lastMessage
                    lastMessage = message
                    print("Waiting 6 hours before tweeting again")
                    #Bot stops looking
                    self.disconnect()
                    #Waits 21600 seconds - 6 hours
                    time.sleep(21600)
                    #Attempts to re-open the stream
                    stream.statuses.filter(follow=['6348742'])
            except BaseException as e:
                print("Threw an exception: " + str(e))
                #if an exception is thrown, it will state why, and will wait for the next tweet before trying again
                pass

stream = MyStreamer(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

print("Stream is now running")

#this code searches for tweets from a given userID
#Get the id of the account from here: http://gettwitterid.com/
stream.statuses.filter(follow=['userID'])
