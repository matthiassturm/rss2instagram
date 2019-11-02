import os
import sys
import feedparser
import re
import requests
from io import BytesIO
from PIL import Image
from resizeimage import resizeimage

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot # noqa: E402

def get_post(feed_url, index):
	feed_content = feedparser.parse(feed_url)
	post = []
	post.append(feed_content['items'][index]['title'])
	post.append(feed_content['items'][index]['link'])
	post.append(feed_content['items'][index]['published'])
	post.append(re.search('(?P<url>https?://[^\s"]+)', feed_content['items'][index]['summary_detail']['value']).group('url'))
	return post

def get_story_image(feed_url):
	post = get_post(feed_url, 0)
	response = requests.get(post[3])
	cover = Image.open(BytesIO(response.content))

	w, h = cover.size
	new_w, new_h = 1080, 1920

	cover = resizeimage.resize_cover(cover, [new_w, new_h])

	# add foreground layer from rgba png file
	layer = Image.open('layer.png').convert('RGBA')
	cover.paste(layer, (0, 0), layer)

	return cover

def post_to_story(img):
	bot = Bot()
	bot.login()
	bot.upload_story_photo(img)

url = 'http://berlingraffiti.de/feed/'
cover = get_story_image(url)
cover.save('cover.jpg')
post_to_story('cover.jpg')