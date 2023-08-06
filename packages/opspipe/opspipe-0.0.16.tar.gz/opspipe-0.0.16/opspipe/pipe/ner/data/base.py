# -*- coding: utf-8 -*-
class Base():
    def __init__(self, data = None): 
        self.data = data
    
    def read(self,path): 
        raise NotImplementedError
        
    def converfrom(self,fun):
        raise NotImplementedError
    
    def save(self,path):
        raise NotImplementedError