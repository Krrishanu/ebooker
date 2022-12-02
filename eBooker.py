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

def get_links(link):

	s = get_soup(link)

	if 'shmoop' in link:

		#save_pages(s,filename) #Writing First Page for Shmoop

		b = s.select('.sidebar-main')
		urls = b[0].find_all('a',href=True)
		url = []
		for i in urls:
			 url.append('https://www.shmoop.com'+i['href'])
	    
	elif 'sparknotes' in link:
		l = s.select(".landing-page__umbrella")
		urls = []
		url = [link,]
		for i in range(len(l)):
			a = l[i].find_all("a",href=True)
			urls = urls+a
		for i in urls:
			url.append('https://www.sparknotes.com'+i['href'])

	elif 'cliffsnotes' in link:
		a= s.find_all(class_='secondary-navigation')
		urls = a[0].find_all('a',href=True)
		url=[]

		for i in urls:
			u = "https://www.cliffsnotes.com"+i['href']
			if u not in url:
				url.append(u)
		url = url[1:-5]

	return url


def get_content(url):
	i = 0 
	c = []
	t = []
	chapters=[]
	while i in range(len(url)):

	    s = get_soup(url[i])

	    if 'shmoop' in link:
	        content = s.select(".content-wrapper")
	    elif 'spark' in link:
	        content = s.select(".main-container")
	    elif 'cliffsnotes' in link:
	        content = s.select(".copy")

	    i+=1

	    t.append(s.title.text)
	    c.append(content[0])
	    print(s.title.text)

	return t,c 

def add_chapters(t,c,book):
	chapters = []
	i = 0
	while i in range(len(c)):
	# create chapter
	    ch = epub.EpubHtml(title=t[i], file_name=t[i]+str(i)+".xhtml", lang="en")
	    ch.content = str(c[i])
	    book.add_item(ch)
	    i+=1
	    chapters.append(ch)

	return chapters 


def main():
	global link
	link = input("Link: ")
	

	if "cliffsnotes" in link:
		filename = link.split('/')[-2]
	else:
		filename = link.split('/')[-1]

	filename = filename+".epub"

	s = get_soup(link)
	url = get_links(link)
	t,c = get_content(url)

	book = epub.EpubBook()

	# set metadata
	book.set_identifier(link.split('/')[-1])
	book.set_title(s.title.text)
	book.set_language("en")

	#book.set_cover("cover.jpg", "img.jpg", create_page=True)
	#book.set_cover("image.jpg", open('img.jpg', 'rb').read())

	cover = epub.EpubHtml(title=s.title.text, file_name="cover.xhtml", lang="en")
	cover.content = "<html><h1>"+s.title.text+"</h1></html>"
	book.add_item(cover)


	if 'sparknotes' in link:
		book.add_author("Spark")
	elif "shmoop" in link:
		book.add_author("Shmoop")
	elif "cliffsnotes" in link:
		book.add_author("Cliffs")

	ch = add_chapters(t,c,book)

	book.toc=(ch)


	# define CSS style
	style = "BODY {color: white;}"
	nav_css = epub.EpubItem(
	    uid="style_nav",
	    file_name="style/nav.css",
	    media_type="text/css",
	    content=style,
	)

	# add CSS file
	book.add_item(nav_css)



	# basic spine
	book.spine = [cover,"nav"]+ch

	# add default NCX and Nav file
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	# write to the file
	#filename = ''.join(e for e in s.title.text if e.isalnum())+'.epub'
	epub.write_epub(filename,book)
	

if __name__ == "__main__":
	main()
	