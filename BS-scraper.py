from bs4 import BeautifulSoup
import requests
import time

# url = requests.get('https://bitcointalk.org/index.php?board=1.0')
url = requests.get('https://www.reddit.com/r/Bitcoin/comments/8fah9t/daily_discussion_april_27_2018')

soup = BeautifulSoup(url.text, 'html.parser')


# with open('sb.txt', 'w') as f:
#     for subreddit in soup.find_all('span'):
#         try:
#                 f.write(subreddit.string + '\n')
#         except:
#             TypeError



with open('sb.txt', 'w') as f:
    for subreddit in soup.find_all('p'):
        time.sleep(2)
        try:
                f.write(subreddit.string + '\n')
        except:
            TypeError

