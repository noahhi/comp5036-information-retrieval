#!/usr/bin/python3	indexer.py -d ./LookingGlass 5

import sys
import os
import re
import json
import math

# global declarations for docids, lengths, postings, vocabulary
docids = []
doclength = {}
postings = {}
vocab = {}


def main():
	# code only for testing offline only - not used for a crawl
	max_files = 64000;
	if len(sys.argv) == 1:
		print ('usage: ./indexer.py file | -d directory [maxfiles]')
		sys.exit(1)
	elif len(sys.argv) == 2:
		filename = sys.argv[1]
	elif len(sys.argv) == 3:
		if re.match('-d', sys.argv[1]):
			dirname = sys.argv[2]
			dir_index = True
		else:
			print ('usage: ./indexer.py file | -d directory [maxfiles]')
			sys.exit(1)
	elif len(sys.argv) == 4:
		if re.match('\d+', sys.argv[3]):
			max_files = int(sys.argv[3])
		else:
			print ('usage: ./indexer.py file | -d directory [maxfiles]')
			sys.exit(1)
	else:
		print ('usage: ./indexer.py file | -d directory [maxfiles]')

	if len(sys.argv) == 2:
		index_file(filename)
	elif re.match('-d', sys.argv[1]):
		for filename in os.listdir(sys.argv[2]):
			if re.match('^_', filename):
				continue
			if max_files > 0:
				max_files -= 1
				filename = sys.argv[2]+'/'+filename
				index_file(filename)
			else:
				break

	write_index_files(1)


def index_file(filename):	# code only for testing offline only - not used for a crawl
		try:
			input_file = open(filename, 'rb')
		except (IOError) as ex:
			print('Cannot open ', filename, '\n Error: ', ex)
		else:
			page_contents = input_file.read() # read the input file
			url = 'http://www.'+filename+'/'
			#print (url, page_contents)
			make_index(url, page_contents)
			input_file.close()


def write_index_files(n):

	# n can be 0,1
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclength
	# decide which files to open
	# there are 2 sets, written to on alternate calls
	nn = n+1
	# open files
	out_d = open('docids'+str(nn)+'.txt', 'w')
	out_l = open('doclength'+str(nn)+'.txt', 'w')
	out_v = open('vocab'+str(nn)+'.txt', 'w')
	out_p = open('postings'+str(nn)+'.txt', 'w')
	# write to index files: docids, vocab, postings
	# use JSON as it preserves the dictionary structure (read/write treat it as a string)
	json.dump(docids, out_d)
	json.dump(doclength, out_l)
	json.dump(vocab, out_v)
	json.dump(postings, out_p)
	# close files
	out_d.close()
	out_l.close()
	out_v.close()
	out_p.close()

	d = len(docids)
	v = len(vocab)
	p = len(postings)
	print ('===============================================')
	print ('Indexing: ', d, ' docs ', v, ' terms ', p, ' postings lists written to file')
	print ('===============================================')

	return

def read_index_files():

	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclength
	nn = 1

	# reads existing data into index files: docids, lengths, vocab, postings
	in_d = open('docids'+str(nn)+'.txt', 'r')
	in_l = open('doclength'+str(nn)+'.txt', 'r')
	in_v = open('vocab.txt'+str(nn)+'', 'r')
	in_p = open('postings'+str(nn)+'.txt', 'r')

	docids = json.load(in_d)
	doclength = json.load(in_l)
	vocab = json.load(in_v)
	postings = json.load(in_p)

	in_d.close()
	in_l.close()
	in_v.close()
	in_p.close()

	return



def clean_html(html):
	##########################################
	#####	remove markup from page		 #####
	#### your code here ####
	# replace all whitespace (ie. newlines, tabs) with single space
	cleaned = re.sub(r'\s+',' ', html)

	# remove all html tags
	cleaned = re.sub(r'<[^>]+>','',cleaned)

	#TODO remove javascript, comments, java, etc..

	#####  end of remove markup from page #####
	###########################################

	return cleaned.strip()



def make_index(url, page_contents):
	# declare refs to global variables
	global docids		# contains URLs + docids
	global postings		# contains wordids + docids, frequencies
	global vocab		# contains words + wordids
	global doclength	# contains docids + lengths

	print ('make_index: url = ', url)
	#print ('make_index1: page_text = ', page_text) # for testing

	#############################################
	#####	add the url to the doclist		#####
	#
	#	need to consider duplicates that only differ in the protocol and www.
	#	as these are not picked up by the crawler
	#### your code here ####

	# remove http, https, www. from url
	clean_url = re.sub(r'https?:\/\/(www\.)?','',url)
	print ('make_index: clean url = ', clean_url)

	# add doc to docids, ID is given by length of docids
	docid = len(docids)
	docids.append(clean_url)

	#####  end of add the url to the doclist #####
	##############################################

	#### extract the words from the page contents ####
	if (isinstance(page_contents, bytes)): # convert bytes to string if necessary
		page_contents = page_contents.decode('utf-8','ignore') # ignore code errors...

	#### page_text is the initial content, transformed to words ####
	words = clean_html(page_contents)


	###################################################
	##### stemming and other processing goes here #####
	#### your code here ####

	# make text lowercase
	page_text = words.lower()

	# split text into a list of words (ignoring punctuation)
	#TODO consider numbers and other non-numeric characters
	terms = re.findall(r"[a-zA-Z+']+", page_text)

	# update doclength for doc based on number of terms
	doclength[docid] = len(terms)


	#####  end of stemming and other processing	  #####
	###################################################


	#######################################
	#####  add entries to the index	   ####
	#
	# split the words string into a list
	# store doclength
	# add the vocab counts and postings
	#### your code here ####

	# for each term in document, update vocab and postings list
	for term in terms:
		if term not in vocab:
			# add term to vocab if never seen before, ID based on number of words in vocab
			vocab[term] = len(vocab)

		# retrieve term ID
		termid = vocab[term]

		if termid not in postings:
			# create new posting if term doesn't yet have one
			postings[termid] = {docid:1}
		else:
			# retrieve posting list for current term
			posting = postings[termid]
			if docid not in posting:
				# this is the first occurance of this term in this doc so count=1
				posting[docid] = 1
			else:
				# term has already occured in this doc, increase count by 1
				posting[docid] += 1



	#####  end of add entries to the index	 #####
	##############################################


	##### save the index after every 100 documents ####
	if (len(doclength)%100 == 0): #
		n = int(len(doclength)/100)%2
		write_index_files(n)

	return

# Standard boilerplate to call the main() function
if __name__ == '__main__':
	main()
