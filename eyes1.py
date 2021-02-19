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
		fil_id_list1=[]
		fil_id_list2=[]
		id_list1=[] #for yesterday
		id_list2=[] #for today

		#-----updating json to current date

		with open('newsids.json', 'r') as file:
			data = json.load(file)
		firstkey=list(data["ids"])
		if today.day-1>int(firstkey[0]):
			print(f"cleared! data of {today.day-2}")
			data["ids"].pop(f"{today.day-2}")
			data["ids"].update({today.day:[]})
			
			with open('newsids.json', 'w') as file:
				json.dump(data, file)

		#-----getting links with "news" in them of current date

		for links in soup.find_all('a',href=True):
			if "/news/" in links['href'] and len(links['href']) > 17:
				if f'{today.month}-{str(int(today.day))}' in links['href']:
					if links['href'] not in articles:
						grb, ids2 = links['href'].split('.')
						id_list2.append(ids2)
						with open('newsids.json', 'r') as file:
							data = json.load(file)
						if ids2 in data["ids"][f"{today.day}"]:
							pass
						else:
							fil_id_list2.append(ids2)
							articles.append(links['href'])

				elif f'{today.month}-{str(int(today.day)-1)}' in links['href']:
					if links['href'] not in articles:
						grb, ids1 = links['href'].split('.')
						id_list1.append(ids1)
						if ids1 in data["ids"][f"{today.day-1}"]:
							pass
						else:
							fil_id_list1.append(ids1)
							articles.append(links['href'])
		
		jsonlist2 = data["ids"][f"{today.day}"]
		jsonlist2 = jsonlist2+fil_id_list2 
		data["ids"].update({f"{today.day}":jsonlist2})
		jsonlist1 = data["ids"][f"{today.day-1}"] 
		jsonlist1 = jsonlist1+fil_id_list1
		data["ids"].update({f"{today.day-1}":jsonlist1})

		with open('newsids.json', 'w') as file:
			json.dump(data,file)
		fil_id_list =fil_id_list1+fil_id_list2
		print(fil_id_list2)
		print("------------------------------------")
		print(fil_id_list1)
		print("------------------------------------")
		print(data)
		print("------------------------------------")
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

		return title, content, img_link, url

		#----------IMP!---------|