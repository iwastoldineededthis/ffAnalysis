import re
import urllib2
from bs4 import BeautifulSoup

SITEURL = 'http://www.pro-football-reference.com'
def expandYear(year, workingDirectory):
	'''
	Downloads all games played into the html/[year]/ directory.
	Every week split up into sub-directory

	year:	(int) year to scrape data from
			if year not within records, throws a URLException'''

	#verify url/year are fine
	#make directory for year
	#for each week, make new directory, download games

	pass
def __downloadWeek(baseURL, workingDirectory):
	'''
	Expands a given week games into its respective html files, then downloads them
	into the directory provided

	To be accessed by expandYear

	baseURL:	(str) pro-football-reference.com weekly score split
	workingDirectory:	(str) path to which the html files should be saved

	Exceptions:	URLException if baseURL not a pro-football-reference.com weekly results site
	'''
	print baseURL
	urlPattern = re.compile('^(((http)|(https))://)?(www\.)?(pro-football-reference\.com/years/)(\d){4}(/week_)((\d){1}|(\d){2})(\.htm)$',
							 re.I)	#regex for valid site
	if urlPattern.match(baseURL) is None:	#No match, invalid URL!
		raise URLError('url should be a pro-footbal-reference.com week page')
	weekChannel = urllib2.urlopen(baseURL)
	weekHtml = weekChannel.read()
	weekFileName = baseURL.split('/')[-1]	#takes file name for us to save from site URL
	weekFileLoc = workingDirectory + weekFileName
	with open(weekFileLoc, 'w') as file:
		file.write(weekHtml)
	siteParse = BeautifulSoup(weekHtml, 'html.parser')
	linkList = siteParse.find_all('a')	#finds all link tags
	for link in linkList:
		boxscoreRegEx = re.compile("^/boxscores/(\d){9}[a-zA-Z]{3}\.htm$")	#regex for box score links to download
		if boxscoreRegEx.match(link.attrs['href']):	#link is a valid box score link
			newURL = SITEURL + link.attrs['href']	#creates full new url
			fileName = newURL.split('/')[-1]	#takes file name of html for what we want to save
			fileLoc = workingDirectory + fileName
			siteChannel = urllib2.urlopen(newURL)
			html = siteChannel.read()
			with open(fileLoc, 'w') as file:
				print 'Writing ' + fileName + ' to ' + fileLoc + '...'
				file.write(html)

class URLError(Exception):
	pass

__downloadWeek('http://www.pro-football-reference.com/years/2016/week_1.htm', 'html/week_1/')