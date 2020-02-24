#크롤링시 copy_selector 한번으로는 가져올수 없어서 1st와 2nd로 나눔
import time

from selenium import webdriver
# from selenium import webdriver as wd
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

driver = webdriver.Chrome('/Users/cho/Downloads/chromedriver')
# 크롬을 연다. (★chromedriver.exe 의 경로를 제대로 설정해주는 것이 중요함)


url = 'https://post.naver.com/search/post.nhn?keyword=%EA%B9%80%EC%88%98%EB%AF%B8%20%EB%A0%88%EC%8B%9C%ED%94%BC'
driver.get(url)

SCROLL_PAUSE_TIME = 0.5
cnt_up = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
for cnt in range(0, 4):
	driver.find_element_by_xpath('//*[@id="more_btn"]/button').click()
	# btn 클릭후 스크롤 하단으로 내리기 반복
	while True:

		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		soomis_follow_recipes = soup.select('#_list_container > ul > li')

soomis_follow_recipe_doc = {
		'author': '',
		'description': '',
		'image': '',
		'category': '',
		'posting_day': '',
		'title': 'title',
		'url': url
	}

# 하나 더 만들어보자
for soomis_follow_recipe in soomis_follow_recipes:
    print(cnt_up)

    title = soomis_follow_recipe.select_one('div > div.feed_body > div.text_area > a.link_end > strong').text.strip()
    # if '공유' not in title: 소용 없
    print(title)
    #

    image = str(soomis_follow_recipe.select_one('div > div.feed_body > div.image_area > a.link_end > img ').attrs['src'])
    print(image)

    category = '따라하기 레시피'
    print(category)
    #
    posting_day = str(soomis_follow_recipe.select_one('div.feed_head > div > div.info_post > time').text.split()[0])
    print(posting_day)

    #
    description = soomis_follow_recipe.select_one('div.feed_body > div.text_area > a.link_end > p').text
    print(description)

    # tvN의 공식 레시피 제외 시키는 방법?
    # if 'tvN' in author:
    #   continue
    author = soomis_follow_recipe.select_one('div.feed_head > div > div.writer_area > p.writer > span.name > a').text
    # if 'tvN' or '첫사랑 이야기' not in author:
    print(author)
    #
    pre_url = soomis_follow_recipe.select_one('div.feed_body > div.text_area > a.link_end').get('href')
    url = 'https://post.naver.com' + pre_url
    print(url)


    soomis_follow_recipe_doc = {
        'author': author,
        'description': description,
        'image': image,
        'category': category,
        'posting_day': posting_day,
        'title': title,
        'url': url
    }
    cnt_up += 1

    # db.soomi_all_recipes.insert_one(soomis_follow_recipe_doc) #저장할때만 활성화 시키기
driver.close()

