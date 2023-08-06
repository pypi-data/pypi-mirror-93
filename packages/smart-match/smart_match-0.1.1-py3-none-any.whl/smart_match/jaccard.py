class Jaccard:
        
    def similarity(self, s, t):
        if not s and not t:
            return 1.0
        
        if not s or not t:
            return 0.0
        
        s_set = set(s)
        t_set = set(t)
        
        intersection = s_set.intersection(t_set)
        intersection_size = len(intersection)
                
        return intersection_size / (len(s_set) + len(t_set) - intersection_size)
    
    def dissimilarity(self, s, t):
        return 1 - self.similarity(s, t)
    
    def __repr__(self):
        return 'Jaccard'