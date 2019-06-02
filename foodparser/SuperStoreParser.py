import urllib.request
import re
import bs4
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Parser:

	driver = None

	def __init__(self):
		print('Building webdriver...')
		self.driver = webdriver.Firefox(executable_path='./geckodriver')
		print('Loading superstore homepage...')
		self.driver.get('https://www.realcanadiansuperstore.ca/')
		button = None

		print('waiting for button to appear...')
		while(button == None):
			try:
				button = self.driver.find_element_by_xpath('//button[text()="Alberta"]')
			except:
				button = None

		print('clicking button...')
		result = None
		while(result == None):
			try:
				button.click()
				result = True
			except:
				result = None
	
	def closeWindow(self):
		self.driver.close()
	
	def gethtml(self, url):
		#r = requests.get(url, allow_redirects=False)
		#print(r.status_code)
		#print(r.status_code, r.headers['Location'])
		#data = r.content
		#print(r.headers)
		#return data
		#fp = urllib.request.urlopen(url)
		#print(fp.geturl())
		#return fp.read()

		self.driver.get(url)
		return self.driver.page_source

	def stdUnit(self, value, unit):
		unit = unit.lower()
		if unit == 'mg':
			unit = 'g'
			value = value / 1000
		elif unit == 'l':
			unit = 'ml'
			value = value * 1000
		elif unit == 'kg':
			unit = 'g'
			value = value * 1000

		return value, unit

	def parse(self, text, url):
		# Heat up the kitchen
		soup = BeautifulSoup(text, features='lxml')
		result = {'Link':url}

		# Extract product name
		name = soup.find('h1',  attrs={'class':'product-name'})

		name = ''.join([i for i in name.contents
			if type(i) == bs4.element.NavigableString]).strip()

		result['Food'] = name

		# Extract product quantity
		qty = soup.find('span', attrs={'class':'product-name-qty'})
		qty = qty.text

		# Extract numeric quantity
		numQty = re.findall('[0-9\.]+', qty)[0]

		# Extract quantity
		# check if quantity is multiplicative
		if re.match('.*[0-9\.]+x[0-9\.]+.*', qty):
			# extract numbers
			nums = qty.split('x')
			nums = [re.findall('[0-9\.]+', i)[0] for i in nums]
			nums = [float(i) for i in nums]
			result['Buying Quantity']  = nums[0]*nums[1]

		else:
			result['Buying Quantity'] = float(numQty)


		result['Unit'] = re.findall('[A-Za-z]+', qty)[-1].lower()

		# standardize result
		result['Buying Quantity'], result['Unit'] = self.stdUnit(
			result['Buying Quantity'], result['Unit'])


		#result['alternate unit'] = soup.find('sup', attrs={'class':'reg-price-unit'}).text

		# Extract cost

		# get pricing model bar

		bar = soup.find('div', attrs={'class':'pricing-module'})

		cost = None
		for c in ['reg-price-text', 'old-price-text', 'sale-price-text']:
			try:
				cost = bar.find('span', attrs={'class':c}).text
				cost = re.search('[0-9\.]+', cost)[0]
				break
			except:
				pass

		assert(cost != None)
		result['Buying Cost'] = cost

		# Extract summary data
		summary = soup.find_all('div', attrs={'class':'nutrition-summary'})
		summary = summary

		# Filter out non-tag contents
		summary = [[j for j in i.contents
			if type(j) == bs4.element.Tag] for i in summary]

		# Map nutrition-summary-label to nutrition-summary-value
		summary = {
			[j.text.strip() for j in i 
				if j['class'][0] == 'nutrition-summary-label'][0]:
			[j.text.strip() for j in i 
				if j['class'][0] == 'nutrition-summary-value'][0]
			for i in summary
		}
		
		# Find serving size
		servingSize = summary[[i for i in summary if 'SIZE' in i.upper()][0]]

		# extract number
		servingSizeNum = re.findall('[0-9\.]+', servingSize)[-1]
		servingSizeNum = float(servingSizeNum)
		# extract unit
		servingSizeUnit = re.findall('[A-Za-z]+', servingSize)[-1].lower()

		# standardize unit
		result['Serving Quantity'], result['Serving Unit'] = self.stdUnit(
			servingSizeNum, servingSizeUnit)


		# find calories per serving
		# find tag
		calories = summary[[i for i in summary if 'CALORIES' in i.upper()][0]]
		# extract value
		calories = re.findall('[0-9\.]+', calories)[0]
		calories = float(calories)
		result['Serving Calories'] = calories
		
		# Extract other nutritional data

		nutData = soup.find_all('div',
			attrs={'class':'main-nutrition-attr first'})

		nutDict = {}
		for item in nutData:
			# find Tag elements
			Tags = [i for i in item.contents if type(i) == bs4.element.Tag]
			# find text elements
			text = [i for i in item.contents
				if type(i) == bs4.element.NavigableString]
			text = (''.join(text)).strip()

			# find nutrition label

			Tags = [i for i in Tags if 'class' in i.attrs]

			label = [i for i in Tags if i['class'][0] == 'nutrition-label']
			# Skip items with no nutrition-label tag
			if len(label) == 0:
				continue
			else:
				label = label[0]
			label = label.text.strip()

			# find value
			value = re.findall('[0-9\.]+', text)[0]
			value = float(value)

			# find unit
			unit = re.findall('[A-Za-z]+', text)[-1].lower()

			# standardize unit
			value, unit = self.stdUnit(value, unit)

			# insert into dict
			nutDict[label] = value

		# Extract only the stuff we care about
		result['Serving Protein'] = nutDict['Protein']
		result['Serving Carbs'] = nutDict['Total Carbohydrate']
		result['Serving Fat'] = nutDict['Total Fat']

		return result
