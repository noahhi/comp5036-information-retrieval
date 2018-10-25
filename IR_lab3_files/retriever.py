#!/usr/bin/python3
# needs improving to remove forced type conversions

import sys
import re
import json

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = {}

def main():
	# code for testing offline
	if len(sys.argv) < 2:
		print ('usage: ./retriever.py term [term ...]')
		sys.exit(1)
	query_terms = sys.argv[1:]
	answer = []

	read_index_files()

	print ('Query: ', query_terms)
	answer = retrieve_bool(query_terms)


	i = 0
	for docid in answer:
		i += 1
		print (i, docids[int(docid)])


def read_index_files():
	## reads existing data from index files: docids, vocab, postings
	# uses JSON to preserve list/dictionary data structures
	# declare refs to global variables
	global docids
	global postings
	global vocab
	# open the files
	in_d = open('docids1.txt', 'r')
	in_v = open('vocab1.txt', 'r')
	in_p = open('postings1.txt', 'r')
	# load the data
	docids = json.load(in_d)
	vocab = json.load(in_v)
	postings = json.load(in_p)
	# close the files
	in_d.close()
	in_v.close()
	in_p.close()

	return

#docids = []
#postings = {}
#vocab = {}

def retrieve_bool(query_terms):
	#TODO check for single term, terms not present 

	## a function to perform Boolean retrieval with ANDed terms
	answer = []
	#### your code starts here ####
	doc_lists = []
	for query in query_terms:
		# retrieve termid from vocab dictionary
		queryid = vocab[query]

		# retrieve posting list corresponding to term
		posting = postings[str(queryid)]

		# retrieve documents containing query term
		docs = [doc for doc in posting]
		doc_lists.append(docs)
	doc_lists.sort(key=len)

	index = 1
	list1 = doc_lists[0]
	list2 = doc_lists[1]
	while index < len(doc_lists):
		point1 = 0
		point2 = 0
		intermediate_answer = []
		while point1 < len(list1) and point2 < len(list2):
			if list1[point1] == list2[point2]:
				intermediate_answer.append(list1[point1])
				point1 += 1
				point2 += 1
			elif list1[point1] > list2[point2]:
				point2 += 1
			else:
				point1 += 1
		list1 = intermediate_answer
		index += 1
		if index < len(doc_lists):
			list2 = doc_lists[index]

	answer = intermediate_answer
	print(answer)
	#### your code ends here ####
	return answer

	# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()
