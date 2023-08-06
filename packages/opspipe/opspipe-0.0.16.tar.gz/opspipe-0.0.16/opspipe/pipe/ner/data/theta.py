# -*- coding: utf-8 -*-
import json,os
from pathlib import Path
from opspipe.utils import read_json 
from ..data.base import Base
from tqdm import tqdm

class Theta(Base):
    def __init__(self, data = None): 
        Base.__init__(self, data)  
        #self.data = data
    
    def read(self,path):  
        train_file='train_data.txt'
        labels_file='labels.txt'
         
        
    def converfrom(self,fun):
        self.data = fun.data
    
    def save(self,path):
        assert self.data == None
        print(path)
        
    