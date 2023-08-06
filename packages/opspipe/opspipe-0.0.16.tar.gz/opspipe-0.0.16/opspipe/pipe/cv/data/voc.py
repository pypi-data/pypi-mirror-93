# -*- coding: utf-8 -*-
'''
Created on 2021-1-10

@author: zhys513(254851907@qq.com)
'''

from opspipe.pipe.cv.data.conver.base import Base

class Voc(Base): 
    def __init__(self, data = None): 
        Base.__init__(self, data)  
        self.images = [] 
        self.annotations = []
        self.categories = []
    
    def read(self,path):  
        train_file='train_data.txt'
        labels_file='labels.txt'
        
        
    def converfrom(self,fun):
        self.data = fun.data
    
    def save(self,path):
        assert self.data == None
        print(path)