import snscrape.modules.twitter as sntwitter

def build_query(query, until = "2023-06-08", since = "2023-06-06"):
    query = query + f" until:{until}" + f" since:{since}"
    return query


def getTweets(query, max = 1000):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query = query).get_items()):
        if i>max:
            break
        tweets.append({"username" : tweet.user.username,
                       "date" : tweet.date,
                       "content" : tweet.content,
                       "likeCount" : tweet.likeCount,
                       "retweetCount" : tweet.retweetCount,
                       "replyCount" : tweet.replyCount,
                       "lang" : tweet.lang,
                       "sourceLabel" : tweet.sourceLabel})
        
    return tweets


def sortTweets(tweets, sentiments):
    pass