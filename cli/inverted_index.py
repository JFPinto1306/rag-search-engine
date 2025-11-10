import pickle
import os


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
    
    def __add_document(self, doc_id, text):
        text = list(set([x for x in text.split(' ') if len(x)>0]))
        for token in text:
            if token not in self.index:
                self.index[token] = [doc_id]
                
            else:
                self.index[token].append(doc_id)
            
    def get_documents(self, term):
        if term in self.index:
            return sorted(self.index[term])
        else:
            return []
    
    def build(self,movies):
        for movie in movies:
            self.docmap[movie['id']] = movie
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(movie['id'],text)
            
        print(len(self.docmap))
            
            
    def save(self):
        cache_path = "../cache"
        if not os.path.isdir(cache_path):
            os.makedirs(cache_path)
            
        with open("../cache/index.pkl", 'wb') as f:  
            pickle.dump(self.index,f)
        with open("../cache/docmap.pkl", 'wb') as f:  
            pickle.dump(self.docmap,f)
            
            
            
            
            
        