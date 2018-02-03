import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import bs4

city_list = ['birmingham-al', 'mobile-al', 'montgomery-al', 'fresno-ca', 'los-angeles-ca', 
'oakland-ca', 'sacramento-ca', 'san-diego-ca', 'san-francisco-ca', 'san-jose-ca', 
'stockton-ca', 'denver-co', 'new-haven-ct', 'stamford,-darien,-and-new-canaan-ct', 
'east-hartford-ct', 'new-britain-ct', 'jacksonville-fl', 'miami-fl', 
'st.petersburg-fl', 'tampa-fl', 'atlanta-ga', 'augusta-ga', 'columbus-ga', 
'macon-ga', 'aurora-il', 'chicago-il', 'decatur-il', 'east-st.-louis-il', 
'joliet-il', 'rockford-il', 'springfield-il', 'evansville-in', 'fort-wayne-in', 
'indianapolis-in', 'lake-county-gary-in', 'muncie-in', 'southbend-in', 
'terre-haute-in', 'wichita-ks', 'lexington-ky', 'louisville-ky', 'new-orleans-la', 
'baltimore-md', 'malden-ma', 'brockton-ma', 'holyoke-chicopee-ma', 'arlington-ma', 
'belmont-ma', 'boston-ma', 'braintree-ma', 'brookline-ma', 'cambridge-ma', 
'chelsea-ma', 'dedham-ma', 'everett-ma', 'lexington-ma', 'haverhill-ma', 
'medford-ma', 'melrose-ma', 'milton-ma', 'needham-ma', 'newton-ma', 'quincy-ma', 
'revere-ma', 'saugus-ma', 'somerville-ma', 'waltham-ma', 'watertown-ma', 
'winchester-ma', 'winthrop-ma', 'battle-creek-mi', 'bay-city-mi', 'detroit-mi', 
'flint-mi', 'grand-rapids-mi', 'kalamazoo-mi', 'muskegon-mi', 'pontiac-mi', 
'saginaw-mi', 'duluth-mn', 'minneapolis-mn', 'st.louis-mo', 'springfield-mo', 
'st.joseph-mo', 'greater-kansas-city-mo', 'manchester-nh', 'hudson-county-nj', 
'essex-county-nj', 'atlantic-city-nj', 'bergen-co.-nj', 'camden-nj', 
'trenton-nj', 'staten-island-ny', 'bronx-ny', 'manhattan-ny', 'niagara-falls-ny', 
'poughkeepsie-ny', 'queens-ny', 'rochester-ny', 'schenectady-ny', 'brooklyn-ny', 
'syracuse-ny', 'troy-ny', 'utica-ny', 'albany-ny', 'binghamton/johnson-city-ny', 
'buffalo-ny', 'elmira-ny', 'lower-westchester-co.-ny', 'asheville-nc', 
'charlotte-nc', 'durham-nc', 'greensboro-nc', 'winston-salem-nc', 'lorain-oh', 
'akron-oh', 'columbus-oh', 'dayton-oh', 'hamilton-oh', 'lima-oh', 'cleveland-oh', 
'portsmouth-oh', 'springfield-oh', 'toledo-oh', 'warren-oh', 'youngstown-oh', 
'canton-oh', 'oklahoma-city-ok', 'portland-or', 'erie-pa', 'johnstown-pa', 
'new-castle-pa', 'philadelphia-pa', 'pittsburgh-pa', 'altoona-pa', 
'chattanooga-tn', 'knoxville-tn', 'nashville-tn', 'austin-tx', 'dallas-tx', 
'lynchburg-va', 'newport-news-va', 'norfolk-va', 'richmond-va', 'roanoke-va', 
'seattle-wa', 'spokane-wa', 'tacoma-wa', 'charleston-wv', 'wheeling-wv', 
'kenosha-wi', 'madison-wi', 'oshkosh-wi', 'racine-wi', 'milwaukee-co.-wi']


def geojson_by_city(driver_location, city):
	'''
	Pulls GeoJson map file by city using Chrome

	Inputs:
		driver_location (str): locatiion of chromedriver on individual computer
		city (str): city to pull, only those in city_list are valid values

	Returns nothing, downloads a file
	'''
	# Build URL
	url_base = "https://dsl.richmond.edu/panorama/redlining/#city="
	full_url = url_base + city

	driver = webdriver.Chrome(driver_location)
	driver.get(full_url)
	driver.find_element(By.CLASS_NAME, "intro-modal-button").click()
	driver.find_element(By.CLASS_NAME, "intro-modal-button").click()
	WebDriverWait(driver, 10)
	driver.find_element(By.CLASS_NAME, "downloadicon").click()
	driver.find_element(By.LINK_TEXT, "GeoJson").click()
	driver.close()


def geojson_all_cities(driver_location):
	'''
	Pulls GeoJson map files for all available using Chrome

	Inputs:
		driver_location (str): locatiion of chromedriver on individual computer

	Returns nothing, downloads files for all cities
	'''
	driver = webdriver.Chrome('/Users/claire/Downloads/chromedriver')
	driver.get('https://dsl.richmond.edu/panorama/redlining')
	soup = bs4.BeautifulSoup(driver.page_source)

	tag_list_a = soup.find_all("a")

	city_urls = []
	for tag in tag_list_a:
		if "#city" in tag.get("href"):
			city_urls.append(tag.get("href"))

	for city in city_urls:
		driver = webdriver.Chrome(driver_location)
		driver.get("https:" + city)
		driver.find_element(By.CLASS_NAME, "intro-modal-button").click()
		driver.find_element(By.CLASS_NAME, "intro-modal-button").click()
		WebDriverWait(driver, 10)
		driver.find_element(By.CLASS_NAME, "downloadicon").click()
		driver.find_element(By.LINK_TEXT, "GeoJson").click()
		driver.close()





