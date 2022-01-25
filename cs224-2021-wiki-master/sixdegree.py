#Aaron Laferty, CS 224, Due 3/31/2021

import requests
from bs4 import BeautifulSoup
import re
from collections import deque

def get_random_page_url():
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r.url

def filter_links(href):
	if href:
		if re.compile('^/wiki/').search(href):
			if not re.compile('/\w+:').search(href):
				if not re.compile('#').search(href):
					return True
	return False 

#This function will be used to find the path using link and path IDs after we have distinctively found star wars from the last path
def findPath(dq, lastID, depthTaken, r, wiki): #dq = structure of all links checked, lastID = pID of last link to star wars,
	#r = original link, wiki is link to last before star wars
	if (depthTaken == 1): #if star wars is on original page
		path = {0: [r], 1: ["https://en.wikipedia.org/wiki/Star_Wars"]}
		printPath(path, depthTaken) #print just original and star wars
	if (lastID == None): #if ID = none, no path was found
		page = BeautifulSoup(requests.get(link).text, 'html.parser')
		print("There is no path from " + page.find("h1", id="firstHeading").string + " and Star Wars")
		exit()
	path = {0: [r], 1: [], 2: [], 3: [], 4: [], 5: [wiki], 6: ["https://en.wikipedia.org/wiki/Star_Wars"]} #else, a path exists bigger than 1
	index = 4 #used to place values in path
	iD = lastID
	while iD != 0: #while id does not reach 0 or original link
		for i in dq: #for every value in dq
			if (i[1] == iD): #if its linkID is equal to the path ID, it is the link in which we got that one from
				path[index].append(i[0]) #so append it behind it
				iD= i[3] #set ID to its pathID
				index -= 1
				i = 0 #reset I
	printPath(path, depthTaken) #path is found, so print I

def printPath(path, hops):
	if(hops == 1): #if only original to star wars
		for key in range(0, 2): 
			val = requests.get(path[key][0]); #request the page
			page = BeautifulSoup(val.text, 'html.parser') #parse it with BS
			mainBody = page.find(id="bodyContent") #find the contents
			pageTitle = page.find('h1', id="firstHeading").string #get page title
			print(pageTitle + " (" + val.url + ")\n", end = "") #print the links in order with title and url
		exit() #exit
	for key in range(0, 7): #else, path is deeper than 1
		if not path[key]: #if the current path is empty, just skip to the next
			continue
		val = requests.get(path[key][0]); #
		page = BeautifulSoup(val.text, 'html.parser')
		mainBody = page.find(id="bodyContent")
		pageTitle = page.find('h1', id="firstHeading").string
		print(pageTitle + " (" + val.url + ")\n", end = "")
	exit()

def BFS():
	r = get_random_page_url() #start with a random url from wiki
	visited = set([r]) #Keeps track of all the pages we visited to prevent loops
	dq = deque([[r, 0, 1, None]]) #Used to keep track of the paths as we scrape the pages
	max_depth = 7 #max depth of how many hops we are willing to take
	queCount = 0 #used to keep track of place of current link we are checking inside deque
	while dq: #while something is inside the deque
		link = dq[queCount][0] #do not pop because we might need to link back
		lID = dq[queCount][1]
		depth = dq[queCount][2]
		pID = dq[queCount][3]
		if depth < max_depth: #if we are not too far in depth
			page = BeautifulSoup(requests.get(link).text, "html.parser") #parce the page
			mainBody = page.find(id="bodyContent") #parce its body
			oPID = pID #use original pID in case we find it on the current page
			pID = lID #also change pID to lID to keep track of the paths that we came from (will only be necessary if we dont find star wars here
			#for every wiki link on the current page
			for currentLink in mainBody.find_all("a",href=filter_links):
				href = currentLink.get("href")
				if href not in visited: #if we havent visited it before
					lID += 1 #update lID by 1
					visited.add(href) #add it to visited
					if href == "/wiki/Star_Wars": #if this link is star wars
						findPath(dq, oPID, depth, r, link) #automatically find path and print
					else: 
						href = "https://en.wikipedia.org" + href
						dq.append([href, lID, depth + 1, pID]) #add href to dq to examine later in case we need to search it
			queCount += 1 #update queCount so we check the next link
		else: #if depth is too far, there is no path
			break #break out of while loop
	findPath(dq, None, 0, r, None) #and print no path
		

def main():
	BFS() 
		
    
    
if __name__ == "__main__":
    main()
