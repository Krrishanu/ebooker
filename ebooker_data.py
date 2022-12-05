import requests, lxml
from bs4 import BeautifulSoup as bs
from ebooklib import epub

def get_soup(link):

	r = requests.get(link)
	if r.status_code == 200:
		s = bs(r.text,"lxml")
	else:
		print("404 NOT FOUND!")

	return s 

class Shmoop:

	def __init__(self,link):
		
		self.link = link
		self.filename = self.link.split('/')[-1]
		self.author = "Shmoop"

		self.soup = get_soup(self.link)
		self.title = self.soup.title.text

		self.url = self.get_links()
								
		title,content = self.get_content()
		self.titles = title
		self.contents = content





	def get_links(self):

		#save_pages(s,filename) #Writing First Page for Shmoop

		b = self.soup.select('.sidebar-main')
		urls = b[0].find_all('a',href=True)
		url = [self.link]
		for i in urls:
			 url.append('https://www.shmoop.com'+i['href'])

		return url



	def get_content(self):

		i = 0 
		contents = []
		title = []
		chapters=[]

		l_del = self.title.split('Introduction')[0]
		r_del = self.title.split('Introduction')[-1]

		while i in range(len(self.url)):
			s = get_soup(self.url[i])
			content = s.select(".content-wrapper")
			
			contents.append(content[0])

			## cleaning titles ##
			t = s.title.text


			title.append(t)

			print(t)

			i = i+1
		
			

		return title, contents 



class Cliffs:

	def __init__(self,link):
		
		self.link = link
		self.filename = self.link.split('/')[-2]
		self.author = "Cliffsnotes"

		self.soup = get_soup(self.link)
		self.title = self.soup.select(".title-wrapper > h1:nth-child(1)")[0].text

		self.url = self.get_links()
								
		title,content = self.get_content()
		self.titles = title
		self.contents = content





	def get_links(self):

		#save_pages(s,filename) #Writing First Page for Shmoop

		a= self.soup.find_all(class_='secondary-navigation')
		urls = a[0].find_all('a',href=True)
		url=[]

		for i in urls:
			u = "https://www.cliffsnotes.com"+i['href']
			if u not in url:
				url.append(u)

		return url



	def get_content(self):

		i = 0 
		contents = []
		title = []
		chapters=[]

		while i in range(len(self.url)):
			s = get_soup(self.url[i])
			content = s.select(".copy")
			if len(content)!=0:
				title.append(s.title.text)
				contents.append(content[0])

				print(s.title.text)

			i += 1

		
			

		return title, contents 



class Spark:

	def __init__(self,link):
		
		self.link = link
		self.filename = self.link.split('/')[-2]
		self.author = "Sparknotes"

		self.soup = get_soup(self.link)
		self.title = self.soup.title.text

		self.url = self.get_links()
								
		title,content = self.get_content()
		self.titles = title
		self.contents = content





	def get_links(self):

		#save_pages(s,filename) #Writing First Page for Shmoop

		l = self.soup.select(".landing-page__umbrella")
		url = [self.link]
		urls= []
		for i in l:

			a = i.find_all("a",href=True)
			urls = urls+a 
		for i in urls:
			if 'quiz' not in str(i):
				url.append('https://www.sparknotes.com'+i['href'])

		return url



	def get_content(self):

		i = 0 
		contents = []
		title = []

		while i in range(len(self.url)):
			s = get_soup(self.url[i])
			content = s.select(".main-container")

			if len(content)!=0:
				contents.append(str("<h2>"+s.title.text)+"</h2>"+str(content[0]))
				title.append(s.title.text)

			print(s.title.text)

			i += 1

		
			

		return title, contents 

