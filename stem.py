import json
import nltk

def main():
    # load in unprocessed vocab
    vocab = json.load(open('final_vocab.txt', 'r'))
    new_vocab = {}
    map = {}
    #ps = nltk.stem.PorterStemmer()
    #ps = nltk.stem.LancasterStemmer()
    #ps = nltk.stem.SnowballStemmer("english")
    #nltk.download('wordnet')
    ps = nltk.stem.WordNetLemmatizer()
    for term in vocab:
        # apply stemming to each term using PorterStemer from nltk
        stemmed_term = ps.lemmatize(term)
        # record mapping of original term --> stem
        map[term] = stemmed_term
        if stemmed_term not in new_vocab:
            # add stemmed term to new vocab if not already there along with root
            new_vocab[stemmed_term] = [term]
        else:
            # append new root to stem
            new_vocab[stemmed_term].append(term)
    print(len(new_vocab))
    # save new (stemmed) vocab to file
    vocab_file = open('stemmed_vocab.txt', 'w')
    json.dump(new_vocab, vocab_file)
    vocab_file.close()

    # save map to file
    map_file = open('map.txt', 'w')
    json.dump(map, map_file)
    map_file.close()

if __name__ == "__main__":
    main()
