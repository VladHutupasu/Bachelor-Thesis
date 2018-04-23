from bs4 import BeautifulSoup
import requests

url = requests.get('https://bitcointalk.org/index.php?board=1.0')

soup = BeautifulSoup(url.text, 'html.parser')


with open('sb.txt', 'w') as f:
    for subreddit in soup.find_all('span'):
        try:
                f.write(subreddit.string + '\n')
        except:
            TypeError