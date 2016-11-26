import re
from bs4 import BeautifulSoup

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
	urlPattern = re.compile('^(((http)|(https))://)?(www\.)?(pro-football-reference\.com/years/)(\d){4}(/week_)(\d){1-2}(\.htm)$',
							 re.I)	#regex for valid site
	if urlPattern.match(baseURL) is None:	#No match, invalid URL!
		pass #TODO THROW EXCEPTION
	#TODO: CREATE SOUP, LOOK FOR LINKS WITH "FINAL"
	#TODO: DOWNLOAD EACH GAME'S HTML FILE
	pass
