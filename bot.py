import json
import requests
import tweepy # for tweeting
import secrets # shhhh
import time
import logging

logging.basicConfig(level=logging.INFO,format=' %(asctime)s - %(levelname)s - %(message)s')

# def get_next_chunk():
#   # open text file
#   book = BookManager()
#   first_sentence = book.first_sentence()
#   # tweet the whole sentence if it's short enough
#   if len(first_sentence) <= 140:
#     chunk = first_sentence
#   # otherwise just print the first 140 characters
#   else:
#     chunk = first_sentence[0:140]

#   # delete what we just tweeted from the text file
#   book.delete_message(chunk)
#   return chunk

wallpaper_directory = '/home/pricecomstock/slash-selfie/wallpapers/'
wallpaper_url = 'http://pricecomstock.pythonanywhere.com/wallapi?key=TESTING&quote=%Q&attr=%A'

def tweet(message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message {}".format(message))
  api.update_status(status=message)

def tweetpic(filename,message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message {}".format(message))
  api.update_with_media(filename,status=message)

def tweetpicreply(filename,message,reply_id):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message {}".format(message))
  api.update_with_media(filename,status=message,in_reply_to_status_id=reply_id)

def get_tweets_since_id(handle,tweet_id):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Retrieving tweets for {}".format(handle))
  if tweet_id != 0:
    tweets=api.user_timeline(handle,since_id=tweet_id,count=5)
  else:
    tweets=api.user_timeline(handle,count=1)

  return tweets

def make_url_safe(s):
    replacements = [
        ('%','%25'),
        ('#','%23'),
        (':','%3A'),
        ('/','%2F'),
        ('@','%40'),
        ('?','%3F'),
        (' ','%20')
    ]
    safe = s
    for r in replacements:
        safe = safe.replace(r[0],r[1])
    return safe

if __name__ == '__main__':
    PERSISTENT_INFO_FILE_NAME = '/home/pricecomstock/slash-selfie/inspirational_trump/hello-world-bot/persistent.json'
    user='realDonaldTrump'
    try:
        with open(PERSISTENT_INFO_FILE_NAME) as persistent:
            p = json.load(persistent)
    except:
        p = {'lasttweet':0}

    last=p['lasttweet']
    logging.debug('Need tweets since ID: ' + str(last))

    tweets=get_tweets_since_id(user,last)
    logging.debug('Got ' + str(len(tweets)) + ' tweets!')
    if len(tweets) > 0:
        p['lasttweet'] = tweets[0]._json['id']

    with open(PERSISTENT_INFO_FILE_NAME,'w') as persistent:
        json.dump(p,persistent)

    if len(tweets) > 0:
        for so in tweets:
            t=so._json
            quote= t['text']
            logging.info('Wallpapering quote: ' + quote)
            attr='Donald J. Trump'
            request_url = wallpaper_url.replace('%Q',make_url_safe(quote)).replace('%A',make_url_safe(attr))
            logging.debug('Requesting to: ' + request_url)
            r=requests.get(request_url)
            j=r.json()
            filename=j['url'].split('=',1)[1]
            cutoff = (quote[:117] + '..') if len(quote) > 119 else quote
            tweetpicreply(wallpaper_directory + filename,'.@realDonaldTrump: ' + cutoff,t['id'])
            time.sleep(10)