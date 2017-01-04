import json
import urllib, urllib2

def run_query(search_terms):
	#specify the base
	root_url = 'https://api.datamarket.azure.com/Bing/Search/'
	source = 'Web'
	
	#specify how many results we wish to return per page
	#offset specifies where in the results list to start from
	results_per_page = 10
	offset = 0
	
	#wrap quotes around our query terms as specified by the Bing API
	#the query we will then use is stored within the variable query
	query = " '{0}' ".format(search_terms)
	query = urllib.quote(query)
	
	#contruct the latter part of our requested url
	#set the format of our response to json and other properties
	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(root_url, source, results_per_page, offset, query)
	
	#setup authenticaton within the Bing servers
	#The username must be a blank string, and put it in API key
	username = ''
	bing_api_key = '<api_key>'
	
	#create a password manager which handles authenticaton for us
	password_mgr = urllib.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, bing_api_key)
	
	#create our results list which we'll populate
	results = []
	
	try:
		#prepare for connecting to bing servers
		handler = urllib.HTTPBasicAuthHandler(passsword_mgr)
		opener = urllib.build_opener(handler)
		urllib.install_opener(opener)
		
		#connect to the server and rad the response generated
		response = urllib.urlopen(search_url).read()
		#convert the string response to the python dictionary object
		json_response = json.loads(response)
		#loop through each page returned, populating out results list
		for result in json_response['d']['results']:
			results.append({'title': result['Title'], 'link':result['Url'], 'summary':result['Description'])}
			
	except urllib.URLError, e:
		print("Error ocured when querying BING API:", e)
		
	return results
	
	
#HOW IT'S IMPLEMENTED
#1. the function prepares for connexting to Bing by preparing the url that we'll be requesting
#2. the function then prepares authentication, making use of the bing api key
#3. we then connect to the bing api through the command urllib.urlopen(search_url). the results from the server as saved as a string
#4. the string is then paresed into a python dictionary object through the json package
#5. we loop through all results populating the results dictionary
#6. the dictionary is finally returned by a function.
	
