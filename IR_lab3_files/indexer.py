#!/usr/bin/python3

import sys
import re
import json

# global declarations for doclist, doclengths, postings, vocabulary
# depending on how you implement the index, these can be lists or dicts
docids = []
postings = {}
vocab = {} 
doclengths = []

def main():
	# code for testing offline
	if len(sys.argv) != 2:
		print ('usage: ./indexer.py file')
		sys.exit(1)
	filename = sys.argv[1]

	try:
		input_file = open(filename, 'r')
	except (IOError) as ex:
		print('Cannot open ', filename, '\n Error: ', ex)

	else:
		page_contents = input_file.read() # read the input file
		url = 'http://www.'+filename+'/'
		print (url, page_contents)
		make_index(url, page_contents)
		
		filename = "lg002.html" 
		file = open(filename, 'r')
		page = file.read()
		url = 'http://www.lg002.html/'
		make_index(url, page) 
	
	finally:
		input_file.close()

	
def clean_html(html):
	#### your code starts here ####
	
	# replace all whitespace (ie. newlines, tabs) with spaces
	cleaned = re.sub(r'\s+',' ', html)
	
	# remove all html tags 
	cleaned = re.sub(r'<[^>]+>','',cleaned) 
	
	#### your code ends here ####  
	return cleaned
	
def write_index_files():
# 
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclengths
	# open files
	out_d = open('docids.txt', 'w')
	out_v = open('vocab.txt', 'w')
	out_l = open('doclengths.txt', 'w')
	out_p = open('postings.txt', 'w')
	# write to index files: docids, vocab, postings
	# use JSON as it preserves the dictionary structure (read/write treat it as a string)
	json.dump(docids, out_d)
	json.dump(vocab, out_v)
	json.dump(doclengths, out_p)
	json.dump(postings, out_p)
	# close files
	out_d.close()
	out_v.close()
	out_l.close()
	out_p.close()
	
	d = len(docids)
	v = len(vocab)
	p = len(postings)
	print ('===============================================')
	print ('Indexing: ', d, ' docs ', v, ' terms ', p, ' postings written to file')
	print ('===============================================')
	
	return
	
	
def make_index(url, page_contents):
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclengths
	
	#extract the words from the page contents
	
	if (isinstance(page_contents, bytes)): # convert bytes to string if necessary
		page_contents = page_contents.decode('utf-8', ignore)
	page_text = clean_html(page_contents)
	
	print ('make_index: url = ', url)

	### main steps ###
	#### 1. remove http, https, www ####

	#### 2. append the url to the list of documents and get the docid ####
	#		if the doclist is a list, the docid is index of the url 
	
	#### 3. clean and procsss the text into a list of terms ####
	
	#### 4. for each term in the terms list ####
	#		if it is not in vocab, append it
	#		get the termid for the term from vocab
	
	#		if the termid is not in postings, append it
	#		get the postings list for the term
	#		if there is not a posting for the document, add it (a list with docid, count)
	#		increment the count

	#### 5. write to file ####
	#			best to do this after each doc, as then only the current document is lost 
	#			if it crashes in the middle of a crawl
	
	#### your code starts here ####
 
	
	## dealing with docid (steps 1-2) ##
	# remove http, https, www. from url 
	clean_url = re.sub(r'https?:\/\/(www\.)?','',url)
	print ('make_index: clean url = ', clean_url)
	
	# add doc to docids, id is given by length of docids  
	docid = len(docids)
	docids.append(clean_url)
	
	## clean and process terms in doc (steps3-4) ##
	# make text lowercase
	page_text = page_text.lower()
	
	# split text into a list of words (ignoring punctuation) 
	terms = re.findall(r"[a-zA-Z+']+", page_text)
	
	# for each term in doc, add to vocab if necessary and adjust postings 
	for term in terms:
		if term not in vocab:
			vocab[term] = len(vocab) 
		
		termid = vocab[term] 

		if termid not in postings:
			postings[termid] = {docid:1}
		else:
			posting = postings[termid]  
			if docid not in posting:
				posting[docid] = 1
			else:
				posting[docid] += 1 
				
	print('vocab:')
	print(vocab)
	print('postings')
	print(postings) 
	
	f = open("postings_list.txt", "w") 
	f.write("docids\n")
	f.write(str(docids)+'\n')
	f.write("vocab\n")
	f.write(str(vocab)+'\n')
	f.write("postings list\n")
	f.write(str(postings))
	f.close()
	
	#### your code ends here ####  

	return
	
# Standard boilerplate to call the main() function
if __name__ == '__main__':
	main()


	