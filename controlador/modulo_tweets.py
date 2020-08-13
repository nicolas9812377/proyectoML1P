import tweepy
import json
def obtenerTweets(n):
  # 4 cadenas para la autenticacion
  consumer_key = "cgr7RCgecGri8ECGP6W1uTfdN"
  consumer_secret = "4gvnMkiXnI0IRJPkrvIQSCTJxH1MOLAMKM3lTn1xhTVLB9K4Jy"
  access_token = "632593702-Meuukj41hpkMbQiBVfZuzkHtlHARxB0jl59jgmVp"
  access_token_secret = "NblysojLFfIendBE0MXJiM19L2F5EA9iAibSOzIK01wkI"
  
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  # con este objeto realizaremos todas las llamadas al API
  api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

  query = {'q': ['coronavirus','covid','covid-19'],
          'result_type': 'recent',
          'lang': 'es',
          'geocode': '-1.95529,-78.70604,350km',
          #'since': '2020-05-31',
          #'until' : '2020-06-01',
          'tweet_mode' :'extended'
          }
  t= []
  fecha = []
 
  for x,tweet in enumerate(tweepy.Cursor(api.search, **query).items(n)):
    try:
      fecha.append(str(tweet.created_at))
      t.append(tweet.retweeted_status.full_text.replace('\n', ' '))
    except:
      t.append(tweet.full_text.replace('\n', ' '))
  return t,fecha
