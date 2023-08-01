import requests, lxml
from bs4 import BeautifulSoup as bs
from ebooklib import epub

def get_soup(link):
	s = None
	r = requests.get(link)
	if r.status_code == 200:
		s = bs(r.text,"lxml")
		return s
	else:
		print("404 NOT FOUND!")

	 

class Shmoop:

	def __init__(self,link):
		
		self.link = link
		self.filename = self.link.split('/')[-1]
		self.author = "Shmoop"

		self.soup = get_soup(self.link)
		self.title = self.soup.title.text

#		self.url = self.get_links()
								
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

		pg = self.link

		l_del = self.title.split('Introduction')[0]
		r_del = self.title.split('Introduction')[-1]

		while True:
			

			s = get_soup(pg)
			content = s.select(".content-wrapper")
			
			contents.append(content[0])

			## cleaning titles ##
			t = s.title.text


			title.append(t)

			print(t)

			# Next Page

			navs = s.select(".btn-next")

			if len(navs)!=0:

				nxt_pg = "https://www.shmoop.com" + navs[-1]['href']

				pg = nxt_pg

			else:
				break
		
			

		return title, contents 



class Cliffs:

	def __init__(self,link):
		
		self.link = link
		self.filename = self.link.split('/')[-2]
		self.author = "Cliffsnotes"

		self.soup = get_soup(self.link)
		self.title = self.soup.select(".title-wrapper > h1:nth-child(1)")[0].text

#		self.url = self.get_links()
								
		title,content = self.get_content()
		self.titles = title
		self.contents = content



	def get_content(self):

		i = 0 
		contents = []
		title = []
		chapters=[]

		pgs_visited = [self.link,]

		pg = self.link

		while i == 0:
			s = get_soup(pg)
			

			# Getting Data
			content = s.select(".copy")

			if len(content)!=0:
				title.append(s.title.text)
				contents.append(content[0])

				print(s.title.text)

			# Pagination

			navs = s.select(".nav-bttn-filled")

			if len(navs)!=0:

				nxt_pg = "https://www.cliffsnotes.com" + navs[-1]['href']

			else:

				nxt_pg = None

			if nxt_pg != None and nxt_pg not in pgs_visited:
				
				pgs_visited.append(nxt_pg)
				pg = nxt_pg

			else:
				print('Total '+str(len(pgs_visited))+' Pages')
				i = 1

		return title, contents 







'''
			if len(content)!=0:
				title.append(s.title.text)
				contents.append(content[0])

				print(s.title.text)



			i += 1





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

	'''

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

		pg = self.link

		pgs_visited=[self.link,]

		while i == 0:

			s = get_soup(pg)

			if pg in self.url:
				self.url.remove(pg)


			content = s.select(".main-container")

			if len(content)!=0:
				contents.append(str("<h2>"+s.title.text)+"</h2>"+str(content[0]))
				title.append(s.title.text)



			print(s.title.text)

			# Check for next page
			
			n = s.select(".page-turn-nav__link--next")


			if len(n)!=0:
				nxt_pg = 'https://www.sparknotes.com'+n[0]['href']+'/'

				pg = nxt_pg

				pgs_visited.append(pg)
				
			elif len(self.url) !=0:
				pg = self.url[0]

			else:
				i = 1


		
			

		return title, contents 

