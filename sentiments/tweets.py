#!/usr/bin/env python3

import sys, json, timeit, array
import twython, analyzer
from termcolor import colored
from colored import bg,fg,attr,stylize

def main(argv):
    if len(sys.argv) != 2:
        print("Usage: ./{} [username]".format(__name__))
        sys.exit(0)
    username = sys.argv[1]
    timeline = Twit().usertimeline(username)
    t = analyzer.Analyzer()
    for tweet in timeline:
        tweet = t.analyze(tweet)

        text = ""
        for word in tweet["text"].keys():
            text += (word + " " )
        text = "(" + str(tweet["score"]) + ")\t" + text
        if tweet["score"] >= 1:
            #if colored <module>
                #textsetting = bg(75) + attr(1)
                #print(textsetting + "{}".format(stylize(text, fg(15) )))
            #if termcolor <different module>
                #text = colored(text, "yellow", "on_green", attrs=["bold"])
            text = colored(text, "green", attrs=["bold"])
            print(text)
        elif tweet["score"] < 0:
                #textsetting = bg(177) + attr(1)
                #print(textsetting + "{}".format(stylize(text, fg(178) )))
                #text = colored(text,"white", "on_magenta", attrs=["bold"])
            text = colored(text, "red", attrs=["bold"])
            print(text)


        else:
            #text = colored(text,"white", "on_yellow")
            text = colored(text, "yellow")
            print(text)




class Twit:

    account={\
        "app_key": "kM6WAnMDxlyHGXZKi3c0m7z2n",\
        "app_secret": "E8JYjvSjEqnZTFdzwNDCxl6ptrSMqzuYGKI9025UfBWLscprWZ",\
        "oauth_token": "811275948-Jc8IZaSt17Q3Tr076av7hgvbc21r95QF5vL1xgMK",\
        "oauth_token_secret": "skyZKa3vamwagnYynkHFODjBN8dVF3OGRW3khEpbrtcMF",\
        }

    tweet=(\
            "created_at",
            "id",
            "id_str",
            "text",
            "truncated",
            "entities",
            "source",
            "in_reply_to_status_id",
            "in_reply_to_status_id_str",
            "in_reply_to_user_id",
            "in_reply_to_user_id_str",
            "in_reply_to_screen_name",
            "user",
            "geo",
            "coordinates",
            "place",
            "contributors",
            "retweeted_status",
            "is_quote_status",
            "retweet_count",
            "favorite_count",
            "favorited",
            "retweeted",
            "possibly_sensitive",
            "lang")


    def __init__(self):
        self.twitter = twython.Twython(**Twit.account)
        self.auth()


    def auth(self, *args, **kwargs):
        try:
            obj = self.twitter.verify_credentials(**kwargs)
        except twython.TwythonAuthError:
            raise RuntimeError("Bad token") from None

        #welcome message
        #==============
        #save text as lambda first to save space
        #(ie avoiding storing the string literal)
        text = lambda: "connected to {1} [@{0}, #{2}]".format\
        (obj["screen_name"], obj["name"], obj["id_str"])
        #print(text())

        return

    def user(self, screen_name, *kwargs):
        obj = self.twitter.show_user(screen_name=screen_name)
        for param in kwargs:
            del obj[param]
        return obj


    def usertimeline(self, screen_name="@avogado6", *args, count=50):
        timeline_options = dict(\
        since_id=None,
        max_id= None,
        trim_user=True,
        exclude_replies= True,
        include_rts= True)
        try:
            timeline = self.twitter.get_user_timeline\
            (screen_name=screen_name, count=count, **timeline_options)
        except twython.TwythonError:
            raise
        propfil = set(args) | set(["created_at","text"])

        for tweet,i in zip(timeline, range(len(timeline))):
            for prop in tweet.keys():
                timeline[i] = {k:v for k,v in tweet.items() if (k in propfil)}
        return timeline




if __name__ == "__main__":
    main(sys.argv)