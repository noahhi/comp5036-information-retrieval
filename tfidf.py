#!/usr/bin/python3
#
import sys
import math
import json
import csv
import re

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = {}
stemmed_vocab = {}
doclength = {}
map = {}

title_postings = {}
title_vocab = {}

def main():
    # code for testing offline
    if len(sys.argv) < 2:
        print ('usage: ./tfidf.py term [term ...] OR ./tfidf.py filename')
        sys.exit(1)

    # store all queries in this list
    queries = []

    # if only 1 arg given assume it is a filename
    if len(sys.argv) == 2:
        try:
            file = open(sys.argv[1], 'r')
            # extract queries line by line from file
            for line in file:
                print(line[:-1])
                queries.append(line[:-1])
        except:
            # if file doesn't exist, assume a single term query
            queries.append(sys.argv[1])
    else:
        # if multiple args assume they compose a single query
        queries.append(sys.argv[1:])


    # load in index files (docids, vocab, and postings)
    read_index_files()

    # my student number
    student_no = '100258823'
    # chose from 'basic', 'stemmed', 'weighted', 'relfbk'
    system = 'basic'

    with open('title_results.csv', mode='w', newline='') as results_file:
        writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([student_no])
        writer.writerow(['System', system])
        writer.writerow(['QueryNo', 'Rank', 'URL'])

        # process each query
        query_number = 1
        for query in queries:
            if type(query) == str:
                query_terms = query.split()
            else:
                query_terms = query
            answer = retrieve_vector(query_terms)
            rank = 1
            for docid in answer[:10]:
                url = docids[int(docid)]
                writer.writerow([query_number, rank, url])
                rank += 1
            query_number += 1

    # answer = []
    # answer = retrieve_vector(query_terms)
    # print ('Query: ', query_terms)
    # i = 0
    # for docid in answer:
    #     i += 1
    #     print (i, docids[int(docid)])
    #     if i >= 10:
    #         break

def read_index_files():
    ## reads existing data from index files: docids, vocab, postings
    # uses JSON to preserve list/dictionary data structures
    # declare refs to global variables
    global docids
    global postings
    global vocab
    global stemmed_vocab
    global doclength
    global map
    global title_postings
    global title_vocab
    # open the files
    in_d = open('docids1.txt', 'r')
    in_v = open('vocab1.txt', 'r')
    in_stemv = open('stemmed_vocab.txt', 'r')
    in_p = open('postings1.txt', 'r')
    in_dl = open('doclength1.txt', 'r')
    in_map = open('map.txt', 'r')

    tp = open('title_postings.txt', 'r')
    tv = open('title_vocab.txt', 'r')
    # load the data
    docids = json.load(in_d)
    vocab = json.load(in_v)
    stemmed_vocab = json.load(in_stemv)
    postings = json.load(in_p)
    doclength = json.load(in_dl)
    map = json.load(in_map)

    title_postings = json.load(tp)
    title_vocab = json.load(tv)
    # close the files
    in_d.close()
    in_v.close()
    in_stemv.close()
    in_p.close()
    in_dl.close()
    in_map.close()

    tp.close()
    tv.close()

    return

def retrieve_vector(query_terms):
    ## a function to perform vector model retrieval with tf*idf weighting
    #
    global map          # maps terms to their stem
    global docids       # list of doc names - the index is the docid (i.e. 0-4)
    global doclength    # number of terms in each document
    global vocab        # list of terms found (237) - the index is the termid
    global stemmed_vocab # stemmed vocab (lists of roots for each stem)
    global postings     # postings dictionary; the key is a termid

    global title_postings
    global title_vocab
                        # the value is a list of postings entries,
                        # each of which is a list containing a docid and frequency
    #### your code starts here ####

    num_docs = len(docids)
    # dictionary to store inverse doc frequencies for each term in the query that is also in the vocab
    idfs = {}
    stemming = False
    for term in query_terms:
        term = term.lower()
        # remove punctuation
        term = re.sub(r'[\?\.\!]', '', term)
        if term in vocab:
            if stemming:
                stem = map[term]
                roots = stemmed_vocab[stem]
                for root in roots:
                    termid = vocab[root]
                    # document frequency for a term is given by the length of its postings list
                    docfreq = len(postings[str(termid)])
                    idf = math.log10(num_docs/docfreq)
                    idfs[term] = idf
            else:
                termid = vocab[term]
                # document frequency for a term is given by the length of its postings list
                docfreq = len(postings[str(termid)])
                idf = math.log10(num_docs/docfreq)
                idfs[term] = idf
        else:
            # print a warning for terms in the query which are not in vocab
            print('Note: the query term "', term,  '" does not appear in the corpus')
    print(idfs)
    # stores cumulative weights/scores for each document
    weights = {}
    for term in idfs:
        termid = vocab[term]
        # retrieve postings list for each term
        posting = postings[str(termid)]
        #print(posting)
        for doc,count in posting.items():
            count = int(count)
            # also add count from terms in title (count as double, triple, etc..)
            if doc in weights:
                # compute tf-idf score for current term and doc and add to doc score
                weights[doc] += idfs[term] * (count / doclength[doc])
            else:
                # compute tf-idf score for current term and doc and initialize doc score to this value
                weights[doc] = idfs[term] * (count / doclength[doc])

        if term in title_vocab:
            title_termid = title_vocab[term]
            title_posting = title_postings[str(title_termid)]
            for doc,count in title_posting.items():
                count = int(count) * 3
                # also add count from terms in title (count as double, triple, etc..)
                if doc in weights:
                    # compute tf-idf score for current term and doc and add to doc score
                    weights[doc] += idfs[term] * (count / doclength[doc])
                else:
                    # compute tf-idf score for current term and doc and initialize doc score to this value
                    weights[doc] = idfs[term] * (count / doclength[doc])

    # convert weights dict into a sorted list in ascending order by weight
    answer = sorted(weights, key=weights.get, reverse=True)

    # uncomment to view corresopnding doc scores
    # for docid in answer:
    #     print(docid, ':', weights[docid])

    # TODO also return corresponding doc scores?
    #### your code ends here ####
    return answer


    # Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()
