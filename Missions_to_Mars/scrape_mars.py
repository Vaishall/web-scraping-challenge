def scrape():

	import pandas as pd
	from bs4 import BeautifulSoup as bs
	import requests
	from selenium import webdriver
	from splinter import Browser

	#we visit the first site and get our title/paragraph text
	url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
	driver = webdriver.Chrome()
	driver.get(url)
	data = driver.page_source
	driver.quit()
	soup = bs(data, 'html.parser')
	news_title = soup.find('div','content_title').text
	news_p = soup.find('div','article_teaser_body').text

	#we visit the second site and navigate to our image page and save the url
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser = Browser('chrome', 'chromedriver.exe', headless=False)
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	browser.click_link_by_partial_text('FULL IMAGE')
	browser.click_link_by_partial_text('more info')
	browser.click_link_by_partial_href('/spaceimages/images/largesize')
	featured_image_url = browser.url
	browser.quit()

	#we visit our third site and retrieve the text of the latest tweet
	url = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(url)
	soup = bs(response.text, 'html.parser')
	tweet_text = soup.find('p','tweet-text').text
	#don't forget to remove the image text! If it exists, this will remove it.
	img_text = soup.find('a','u-hidden').text
	mars_weather = tweet_text.replace(img_text,'')

	#we visit our fourth site and retrieve the needed table
	url = "https://space-facts.com/mars/"
	tables = pd.read_html(url)
	df = tables[0].rename(columns={0:'Metric', 1:'Value'})
	df = df.set_index('Metric')
	html_table = df.to_html()

	#we visit our final site to retrieve our image urls
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser = Browser('chrome', 'chromedriver.exe', headless=False)
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')
	divs = soup.find_all('div', 'description')
	hemisphere_image_urls = []
	for div in divs:
	    link = div.find('a')
	    browser.visit("https://astrogeology.usgs.gov/"+link['href'])
	    title = link.text.replace(" Enhanced","")
	    html = browser.html
	    soup = bs(html, 'html.parser')
	    img_url = soup.find('a', text="Sample")['href']
	    hemisphere_image_urls.append({"title":title, "img_url":img_url})
	browser.quit()

	mars_dict = {'news_title':news_title,
				'news_p':news_p,
				'featured_image_url':featured_image_url,
				'mars_weather':mars_weather,
				'html_table':html_table,
				'hemisphere_image_urls':hemisphere_image_urls}
	return mars_dict