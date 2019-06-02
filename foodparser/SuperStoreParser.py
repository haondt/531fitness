import urllib.request
import re
import bs4
from bs4 import BeautifulSoup

class Parser:

	def __init__(self):
		pass
	
	def gethtml(self, url):
		fp = urllib.request.urlopen(url)
		return fp.read()

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
		numQty = re.findall('[0-9]+', qty)[0]
		result['Buying Quantity'] = float(numQty)

		# Extract unit
		result['Unit'] = re.findall('[A-Za-z]+', qty)[-1]
		result['alternate unit'] = soup.find('sup', attrs={'class':'reg-price-unit'}).text

		# Extract cost
		cost = soup.find('span', attrs={'class':'reg-price-text'}).text
		cost = re.search('[0-9\.]+', cost)[0]
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
		servingSizeNum = re.findall('[0-9]+', servingSize)[0]
		servingSizeNum = float(servingSizeNum)
		# extract unit
		servingSizeUnit = re.findall('[A-Za-z]+', servingSize)[-1]
		result['Serving Quantity'] = servingSizeNum
		result['serving unit'] = servingSizeUnit


		# find calories per serving
		# find tag
		calories = summary[[i for i in summary if 'CALORIES' in i.upper()][0]]
		# extract value
		calories = re.findall('[0-9]+', calories)[0]
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
			label = [i for i in Tags if i['class'][0] == 'nutrition-label'][0]
			label = label.text.strip()

			# find value
			value = re.findall('[0-9]+', text)[0]
			value = float(value)

			# find unit
			unit = re.findall('[A-Za-z]+', text)[-1]

			# insert into dict
			if unit == 'mg':
				unit = 'g'
				value = value / 1000
			nutDict[label] = value

		# Extract only the stuff we care about
		result['Serving Protein'] = nutDict['Protein']
		result['Serving Carbs'] = nutDict['Total Carbohydrate']
		result['Serving Fat'] = nutDict['Total Fat']

		return result
