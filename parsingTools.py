import re
import urllib2
import os
from bs4 import BeautifulSoup

SITEURL = 'http://www.pro-football-reference.com'
def expandYear(year, workingDirectory):
	'''
	Downloads all games played into the html/[year]/ directory.
	Every week split up into sub-directory

	year:	(int) year to scrape data from
			if year not within records, throws a URLException'''

	#verify directory/year are fine
	#for each week, make new directory, download games

	if not os.path.isdir(workingDirectory):	#check if working directory is valid
		raise DirectoryError('no such directory as ' + workingDirectory)

	if year < 1925 or year > 2016:	#check if year is valid
		raise CriteriaError('year ' + year + ' not valid! Provide a year between 1925 and 2016.')

	yearURL = SITEURL + '/years/' + str(year)	#read our year site, start parsing
	yearChannel = urllib2.urlopen(yearURL)
	yearHtml = yearChannel.read()
	yearParser = BeautifulSoup(yearHtml, 'html.parser')
	linkList = yearParser.find_all('a')	#make a list of all links
	for link in linkList:
		weekRegEx = re.compile('^/years/(\d){4}/week_((\d){1}|(\d){2})(\.htm)$')	#regex to match a link to a week's page
		linkLoc = link.attrs['href']	#actual url from a given link
		if weekRegEx.match(linkLoc):	#if url matches our pattern, it's a link to a week
			weekNumber = linkLoc.split('/')[-1].split('.')[0]	#gets a string with the week in form 'week_xx'
			print 'Downloading ' + weekNumber + '...'
			weekDirectory = workingDirectory + weekNumber + '/'
			if not os.path.isdir(weekDirectory):	#if no directory exists for the week, make new one
				os.mkdir(weekDirectory)
			weekURL = SITEURL + linkLoc
			__downloadWeek(weekURL, weekDirectory)

def __downloadWeek(baseURL, workingDirectory):
	'''
	Expands a given week games into its respective html files, then downloads them
	into the directory provided

	To be accessed by expandYear

	baseURL:	(str) pro-football-reference.com weekly score split
	workingDirectory:	(str) path to which the html files should be saved

	Exceptions:	URLException if baseURL not a pro-football-reference.com weekly results site
	'''
	if not os.path.isdir(workingDirectory):	#Check if our working directory is valid
		raise DirectoryError('no such directory as ' + workingDirectory)

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
			fileLoc = workingDirectory + fileName 	#local location to save file to
			siteChannel = urllib2.urlopen(newURL)
			html = siteChannel.read()
			with open(fileLoc, 'w') as file:
				print 'Writing ' + fileName + ' to ' + fileLoc + '...'
				file.write(html)

class URLError(Exception):
	pass
class DirectoryError(Exception):
	pass
class CriteriaError(Exception):
	pass
expandYear(2016, 'html/2016/')