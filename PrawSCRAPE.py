import praw

reddit = praw.Reddit(client_id="M8X9AvTd2vFqlg",
                     client_secret="0Li9mKaR1q-D3W7Q0k3PhsxzNzs",
                     password="vladyh2007",
                     username="VladHutupasu",
                     user_agent="redditScraper")

subreddit = reddit.subreddit('bitcoin')
hot_sub = subreddit.controversial('day')
i=0

for submission in hot_sub:
    if not submission.stickied:
        print(submission.title)
        i=i+1
        # comments = submission.comments
        # for comment in comments:
        #     print('COMMENT->'+comment.body)


print('TOTAL NUMBER->>>>>>>>>'+str(i))
