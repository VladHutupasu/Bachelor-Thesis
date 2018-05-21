import praw

reddit = praw.Reddit(client_id="M8X9AvTd2vFqlg",
                     client_secret="0Li9mKaR1q-D3W7Q0k3PhsxzNzs",
                     password="vladyh2007",
                     username="VladHutupasu",
                     user_agent="redditScraper")

subreddit = reddit.subreddit('Bitcoin')

i=0
for submission in subreddit.search('Daily Discussion,', time_filter='all', sort='new', limit=1000):
    if not submission.stickied:
        i+=1
        submission.comments.replace_more(limit=None)
        allComments=submission.comments

        with open(str(i), "w", encoding='utf-8',
                  errors='ignore') as f_all:
            f_all.write(submission.title + "\n")

            for comment in allComments:
                f_all.write(comment.body + "\n")

    print(submission.title)
    print(str(len(submission.comments)))






print('TOTAL-> '+str(i))
