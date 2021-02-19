import requests
from bs4 import BeautifulSoup
import datetime
import json
import asyncio

class newscmd:
	def news_links():
		today=datetime.date.today()
		news = requests.get("https://www.animenewsnetwork.com/news/")
		soup = BeautifulSoup(news.content,features="html.parser")
		articles=[]
		fil_id_list=[]
		id_list=[]

		#-----updating json to current date

		with open('newsids.json', 'r') as file:
			data = json.load(file)
		firstkey=list(data["ids"])
		if today.day-1>int(firstkey[0]):
			print("cleared!")
			data = {"ids":{f"{today.day-1}":[]}}
			with open('newsids.json', 'w') as file:
				file.write('')
				json.dump(data, file)

		#-----getting links with "news" in them of current date

		for links in soup.find_all('a',href=True):
			if "/news/" in links['href'] and len(links['href']) > 17 and f'{today.month}-{str(int(today.day)-1)}' in links['href']:
				if links['href'] not in articles:
					grb, ids = links['href'].split('.')
					id_list.append(ids)
		#-----filtering the ids

					with open('newsids.json', 'r') as file:
						data = json.load(file)

					if ids in data["ids"][f"{today.day-1}"]:
						pass
					else:
						fil_id_list.append(ids)
						articles.append(links['href'])
		print(data)
		print(fil_id_list)
		jsonlist = data["ids"][f"{today.day-1}"] 
		jsonlist = jsonlist+fil_id_list
		data["ids"].update({f"{today.day-1}":jsonlist})
		with open('newsids.json', 'w') as file:
			json.dump(data,file)
		return fil_id_list

	def news_link_parser(news_links):
		url = 'https://animenewsnetwork.com/.'+news_links
		resp = requests.get(url)
		soup = BeautifulSoup(resp.content,"html.parser")
		tags = soup.find_all("p")
		i=0
		content=[]
		for tag in tags:
			if i<4:
				if tag.text != "":
					content.append(tag.text.replace('\n\n', ' '))
					i+=1
		#---------IMP!!!-------|
		content=''.join(content)
		content = f"{content[0:500]}...."
		
		#---------IMP!!!-------|
		tags= soup.find_all("link")
		for tag in tags:
			if "thumbnail" in tag["href"]:
		#----------IMP!---------|	
				img_link = tag["href"]
		#----------IMP!---------|
		tags = soup.find_all("title")
		for tag in tags:
			title = tag.text
		#----------IMP!---------|
		print(f'{title}{content}{img_link}{url}')
		return title, content, img_link, url

		#----------IMP!---------|