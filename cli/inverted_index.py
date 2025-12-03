import pickle
import os
from utils import *
from collections import Counter
class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
        self.term_frequencies = {}
    
    def __add_document(self, doc_id, text):
        tokens = clean_text(text)
        c = Counter()
        for token in tokens:
            c[token] += 1
            if token not in self.index:
                self.index[token] = [doc_id]
            else:
                self.index[token].append(doc_id)
        
        self.term_frequencies[doc_id]=c
            
    def get_documents(self, term):
        if term in self.index:
            return sorted(self.index[term])
        else:
            return []
        
    def get_tf(self,doc_id,term):
        if doc_id in self.term_frequencies:
            if term in self.term_frequencies[doc_id]:
                return self.term_frequencies[doc_id][term]
            
        return 0

    
    def build(self,movies):
        for movie in movies:
            self.docmap[movie['id']] = movie
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(movie['id'],text)

    def save(self):
        cache_path = "./cache"
        if not os.path.isdir(cache_path):
            os.makedirs(cache_path)
            
        with open("./cache/index.pkl", 'wb') as f:  
            pickle.dump(self.index,f)
        with open("./cache/docmap.pkl", 'wb') as f:  
            pickle.dump(self.docmap,f)
        with open("./cache/term_frequencies.pkl", 'wb') as f:  
            pickle.dump(self.term_frequencies,f)
            
    def load(self):
        def load_pickle(path):
            file = open(path,'rb')
            pkl = pickle.load(file)
            file.close() 
            
            return pkl     
        
        try:
            self.index = load_pickle("./cache/index.pkl")
            self.docmap = load_pickle("./cache/docmap.pkl")
            self.term_frequencies = load_pickle("./cache/term_frequencies.pkl")
        except:
            raise ValueError("Pickle Objects do not exist. Use build method to generate before loading.")

    
            
