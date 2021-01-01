# coding=utf8
import time
from multiprocessing import Process

from config import *
from login import client
from logstr import log_str
from message import VERSION_INFO


class Scheduler(object):
	def scheduler_crawler(self,limit=USERS_CYCLE):
		"""
		关注画师作品
		"""
		from crawler import Crawler
		c = Crawler()
		while True:
			c.run()
			time.sleep(USERS_CYCLE)
		
	def scheduler_api(self):
		"""
		API
		"""
		from api import app
		app.run(API_HOST,API_PORT)

	def scheduler_bookmark(self, limit=BOOKMARK_CYCLE):
		"""
		收藏作品
		"""
		from bookmark import Bookmark
		b = Bookmark()
		while True:
			b.run()
			time.sleep(BOOKMARK_CYCLE)

	def run(self):
		log_str(VERSION_INFO)
		# client更新cookie
		client.check()

		if PIXIV_CRAWLER_ENABLED:
			pixiv_crawler = Process(target=self.scheduler_crawler)
			pixiv_crawler.start()

		if PIXIV_BOOKMARK_ENABLED:
			pixiv_bookmark = Process(target=self.scheduler_bookmark)
			pixiv_bookmark.start()

		if PIXIV_API_ENABLED and DB_ENABLE:
			pixiv_api = Process(target=self.scheduler_api)
			pixiv_api.start()


if __name__ == '__main__':
	s = Scheduler()
	s.run()