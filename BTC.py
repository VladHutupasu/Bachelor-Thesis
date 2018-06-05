import praw

reddit = praw.Reddit(client_id="M8X9AvTd2vFqlg",
                     client_secret="0Li9mKaR1q-D3W7Q0k3PhsxzNzs",
                     password="vladyh2007",
                     username="VladHutupasu",
                     user_agent="redditScraper")

subreddit = reddit.subreddit('Bitcoin')

fileNumber=0
for submission in subreddit.search('Daily Discussion', time_filter='all', sort='new', limit=1000):
    if not submission.stickied:
        if 'Daily Discussion' in submission.title:
            fileNumber += 1

            if fileNumber>32:
                break
            else:
                print(submission.title)


                submission.comments.replace_more(limit=None)
                allComments=submission.comments.list()
                print(str(len(allComments)))

                with open(str(fileNumber), "w", encoding='utf-8',
                      errors='ignore') as f_all:
                    f_all.write(submission.title + " -- TITLE\n")

                    for comment in allComments:
                        f_all.write(comment.body + "\n")
    if fileNumber==32:
        print("BYE BYE")
        break








print('TOTAL-> '+str(fileNumber))
