import snscrape.modules.twitter as sntwitter

def getTweets(query, max = 1000):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query = query).get_items()):
        if i>max:
            break
        tweets.append([tweet.user.username, tweet.date, tweet.content,
                       tweet.likeCount, tweet.retweetCount, tweet.replyCount,
                       tweet.lang, tweet.sourceLabel])
        
    return tweets


def sortTweets(tweets, sentiments):
    pass