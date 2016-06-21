import praw
import time
import re
import sqlite3
import random
from config import username, password

word_to_match = [r'\bcoinBot\b', r'\bflip me a coin\b', r'\b!coinflip\b', r'\bcoin flip\b', r'\bflipacoinforme\b',
                 r'\bflip a coin for me\b']

# configuration for reddit login and sqlite3 database.
conn = sqlite3.connect('coin')
c = conn.cursor()
r = praw.Reddit(user_agent='Tosses a coin. 50/50 chance!')

storage = []

r.login(username, password, disable_warning=True)


# flips coin
def coin_flip():
    if random.randrange(0, 100) < 50:
        return 'Heads'
    else:
        return 'Tails'


# main bot loop
def run_bot():
    subreddit = r.get_subreddit("all")
    comments = subreddit.get_comments(limit=200)
    for comment in comments:
        comment_text = comment.body.lower()
        is_match = any(re.search(string, comment_text) for string in word_to_match)
        if comment.id not in storage and is_match:
            coin_toss_result = coin_flip()
            print("Flipping Coin for reddit user: " + str(comment.author) + ". The result was " + str(coin_toss_result))
            storage.append(comment.id)
            comment.reply('The coin flip resulted in... **' + coin_toss_result + '**.' +
                          '\n'
                          '\n'
                          '\n'
                          'Want me to flip a coin? Comment "flip me a coin" or "coin flip" and I will come as fast as '
                          'I can :)'
                          '\n'
                          '\n'
                          '*****'
                          '\n'
                          '>I am a bot! Did I mess something up? ' +
                          '[Report an issue here!](https://github.com/elebumm/FlipACoinForMe)')
            c.execute("INSERT INTO coin (commentID, author, subreddit, comment, result) VALUES (?, ?, ?, ?, ?)",
                      (str(comment.id), str(comment.author), str(comment.subreddit), str(comment.body),
                       str(coin_toss_result)))
            conn.commit()

    print('Currently flipped: ' + str(len(storage)) + ' coins.')


while True:
    try:
        run_bot()
        time.sleep(3)
    except:
        continue

