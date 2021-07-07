#  Import Libraries
import pandas as pd
import praw
from data import *
import time
import numpy
#https://medium.com/nerd-for-tech/wallstreetbets-sentiment-analysis-on-stock-prices-using-natural-language-processing-ed1e9e109a37

print("\nRunning sentiment analysis, this may take a few minutes...\n")

# Instantiate praw object
start_time = time.time()
reddit = praw.Reddit(
    user_agent="Comment Extraction",
    client_id="QktIf3FZ10C5jg",
    client_secret="52XN7-d-s7tBO8Wld9mPQ19PMaV8HA"
)

# Set program parameters
subs = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']  # sub-reddit to search
post_flairs = {'Daily Discussion', 'Weekend Discussion',
               'Discussion'}  # posts flairs to search || None flair is automatically considered
goodAuth = {'AutoModerator'}  # authors whom comments are allowed more than once
uniqueCmt = True  # allow one comment per author per symbol
ignoreAuthP = {'example'}  # authors to ignore for posts
ignoreAuthC = {'example'}  # authors to ignore for comment
upvoteRatio = 0.70  # upvote ratio for post to be considered, 0.70 = 70%
ups = 20  # define # of upvotes, post is considered if upvotes exceed this #
limit = 10  # define the limit, comments 'replace more' limit
upvotes = 2  # define # of upvotes, comment is considered if upvotes exceed this #
picks = 10  # define # of picks here, prints as "Top ## picks are:"
picks_ayz = 10  # define # of picks for sentiment analysis

posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
cmt_auth = {}

for sub in subs:
    subreddit = reddit.subreddit(sub)
    hot_python = subreddit.hot()  # sorting posts by hot
    # Extracting comments, symbols from subreddit
    for submission in hot_python:
        flair = submission.link_flair_text
        author = submission.author.name

        # Checking: post upvote ratio # of upvotes, post flair, and author
        if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (
                flair in post_flairs or flair is None) and author not in ignoreAuthP:
            submission.comment_sort = 'new'
            comments = submission.comments
            titles.append(submission.title)
            posts += 1
            submission.comments.replace_more(limit=limit)
            for comment in comments:
                # try except for deleted account?
                try:
                    auth = comment.author.name
                except:
                    pass
                c_analyzed += 1

                # checking: comment upvotes and author
                if comment.score > upvotes and auth not in ignoreAuthC:
                    split = comment.body.split(' ')
                    for word in split:
                        word = word.replace("$", "")
                        # upper = ticker, length of ticker <= 5, excluded words
                        if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks:

                            # unique comments, try/except for key errors
                            if uniqueCmt and auth not in goodAuth:
                                try:
                                    if auth in cmt_auth[word]:
                                        break
                                except:
                                    pass

                            # counting tickers
                            if word in tickers:
                                tickers[word] += 1
                                a_comments[word].append(comment.body)
                                cmt_auth[word].append(auth)
                                count += 1
                            else:
                                tickers[word] = 1
                                cmt_auth[word] = [auth]
                                a_comments[word] = [comment.body]
                                count += 1

# sorts the dictionary
symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse=True))
top_picks = list(symbols.keys())[0:picks]
time = (time.time() - start_time)

df = pd.DataFrame(dict([(k,pd.Series(v)) for k, v in a_comments.items()]))

df.to_csv("wallstreetsbets.csv")
#print(a_comments)
#print(titles)
