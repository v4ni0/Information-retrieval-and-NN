import nltk
from nltk.corpus import PlaintextCorpusReader
import sys
import math
import os
from trie import Trie

corpus_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JOURNALISM.BG', 'C-MassMedia')
nltk.data.path.append(corpus_root)  # NLTK 3.10+ only reads from whitelisted data dirs
myCorpus = PlaintextCorpusReader(corpus_root, r'.*\.txt')
fileNames = myCorpus.fileids()

def printDocuments(myCorpus,fileNames,docIDs):
    for docID in docIDs:
        text = myCorpus.words(fileNames[docID])
        print('Document ID: '+str(docID))
        for word in text:
            print(word,end=' ')
        print('\n')


class InvertedIndex:
    def __init__(self, corpus: PlaintextCorpusReader, n = None):
        self._index = {}
        self._number_of_documents = len(corpus.fileids()[:n])
        self._create_index(corpus)

    def _create_index(self, corpus: PlaintextCorpusReader):
        for docID, filename in enumerate(corpus.fileids()[:self._number_of_documents]):
            text = corpus.words(filename)
            for token in text:
                if not token.isalpha():
                    continue 

                term = token.lower()
                if not term in self._index:
                    self._index[term] = [docID]

                else:
                    last_docID = self._index[term][-1]
                    if last_docID < docID:
                        self._index[term].append(docID)

    def _intersection(self, list1, list2):
        i1 = 0
        i2 = 0
        answer = []
        while i1 < len(list1) and i2 < len(list2):
            if list1[i1] == list2[i2]:
                answer.append(list1[i1])
                i1 += 1
                i2 += 1
            elif list1[i1] < list2[i2]:
                i1 += 1
            else:
                i2 += 1

        return answer

    def intersect(self, lists):
        if not lists:
            return []

        sorted_lists = sorted(lists, key = lambda x: len(x))
        answer = sorted_lists[0]
        for i in range(1, len(sorted_lists)):
            answer = self._intersection(answer, sorted_lists[i])

        return answer
    
    def intersect_terms(self, termList):
        dicItems = [ self._index[term] for term in termList if term in self._index]
        return self.intersect(dicItems)


def main():
    # n = 1000
    # index = InvertedIndex(myCorpus, n = n)
    # terms = ['културен','обмен','театър']
    # docIDs = index.intersect_terms(terms)
    # printDocuments(myCorpus,fileNames,docIDs)
    trie = Trie()
    filename = myCorpus.fileids()[0]
    words = [token.lower() for token in myCorpus.words(filename) if token.isalpha()]
    for word in words:
        trie.add_word(word)
    words = trie.find_words_with_prefix('к')
    print(words)


if __name__ == "__main__":
    main()