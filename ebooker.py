from ebooker_data import *

from ebooklib import epub
from PIL import Image, ImageDraw, ImageFont

#link1 = "https://www.cliffsnotes.com/literature/d/doctor-faustus/play-summary"
#link = "https://www.cliffsnotes.com/literature/g/gullivers-travels/book-summary"

#link = "https://www.shmoop.com/study-guides/poetry/do-not-go-gentle-into-that-good-night"

#link = 'https://www.sparknotes.com/shakespeare/hamlet/'

def main():

	link = input("Give a link: ")


	if "shmoop" in link:
		obj = Shmoop(link)
	elif "spark" in link:
		obj = Spark(link)
	elif "cliffsnotes" in link:
		obj = Cliffs(link)
	else:
		print("Website not supported")

	create_book(obj)




def create_cover(obj):
	## Create Cover Image ##

	title = obj.filename 
	author = obj.author

	W,H= (1600,2560)  
	image = Image.new(mode='RGB',size=(W,H),color=(255,255,255))
	draw = ImageDraw.Draw(image)
   

	font_t = ImageFont.truetype("Helvetica-Font/Helvetica-Bold.ttf", size=130,)
	font_a = ImageFont.truetype("Helvetica-Font/Helvetica.ttf", size=80,)

	_, _, wt, ht = draw.textbbox((0, 0), title, font=font_t)
	_, _, wa, ha = draw.textbbox((0, 0), author, font=font_a)

	draw.text(((W-wt)/2, (H-ht)/3), title, font=font_t,fill=(0,0,0))
	draw.text(((W-wa)/2, ((H-ha)/3)-2*ht), author, font=font_a,fill=(0,0,0))
	image.save("cover.jpg")


def add_chapters(obj,book):
	t = obj.titles
	c = obj.contents

	chapters = []
	i = 0
	while i in range(len(c)):
	# create chapter
	    ch = epub.EpubHtml(title=str(t[i]), file_name='page00'+str(i)+".xhtml", lang="en")
	    ch.content = str(c[i])
	    book.add_item(ch)
	    i = i+1
	    chapters.append(ch)

	return chapters

def create_book(obj):

	title = obj.title
	author = obj.author
	file = obj.filename

	book = epub.EpubBook()

	# add metadata
	book.set_title(title)
	book.set_language('en')

	book.add_author(author)



	cover = epub.EpubHtml(title=title, file_name="0000.xhtml", lang="en")
	cover.content = "<html><h1>"+title+"</h1></html>"
	book.add_item(cover)

	create_cover(obj)

	book.set_cover("image.jpg", open('cover.jpg', 'rb').read())
	 

	chapters = add_chapters(obj,book)

	# create table of contents
	# - add section
	# - add auto created links to chapters

	book.toc = (chapters)

	# add navigation files
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	# define css style
	style = '''
	@namespace epub "http://www.idpf.org/2007/ops";
	body {
	font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
	}
	h2 {
	 text-align: left;
	 text-transform: uppercase;
	 font-weight: 200;     
	}
	ol {
	    list-style-type: none;
	}
	ol > li:first-child {
	    margin-top: 0.3em;
	}
	nav[epub|type~='toc'] > ol > li > ol  {
	list-style-type:square;
	}
	nav[epub|type~='toc'] > ol > li > ol > li {
	    margin-top: 0.3em;
	}
	'''

	# add css file
	nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
	book.add_item(nav_css)

	# create spine
	book.spine = [cover,"nav"]+chapters

	filename = file+'-'+author+'.epub'

	# create epub file
	epub.write_epub("export/"+filename, book)

	print("Saved to: ","export/"+filename)


if __name__ == '__main__':
	main()