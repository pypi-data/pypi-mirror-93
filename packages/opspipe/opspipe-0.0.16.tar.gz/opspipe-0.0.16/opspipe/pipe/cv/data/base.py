# -*- coding: utf-8 -*-

from pycocotools.coco import COCO
import random, cv2 
import numpy as np

class Base():
    def __init__(self,images=[],annotations = [],categories = []): 
        self.images = images 
        self.annotations = annotations
        self.categories = categories 
        self.splitdatas = []
    
    '''
        读取原始数据
    '''
    def load(self,path): 
        # TODO categories 转换 
        raise NotImplementedError
         
         
    '''
        将名字和id号建立一个字典
    '''
    def name2catid(self):#
        classes = dict()
        for cat in self.categories:
            name = cat['name']
            if isinstance(name,list):
                name = cat['name'][0]
            classes[name] = cat['id'] 
        return classes
     
    '''
        将名字和id号建立一个字典
    '''
    def catid2name(self):
        classes = dict()
        for cat in self.categories:
            name = cat['name']
            if isinstance(name,list):
                name = cat['name'][0]
            classes[cat['id']] = name 
        return classes

    '''
        将一个数据转换为另一个数据
    '''
    def converfrom(self,fun):
        self.images = fun.images
        self.annotations = fun.annotations
        self.categories = fun.categories 
    
    
    '''
        切分数据,默认7:1:2 切分
    '''
    def split(self,seed=102,division_ratio=[7,1,2]): 
        random.seed(seed)
        coco = self.getcoco()
        imgIds = coco.getImgIds()
        num = len(imgIds) 
        px = self.get_percent(division_ratio)
        splitdatas = []
        for percent in px: 
            data_num = int(num*percent)  
            iids = random.sample(imgIds,data_num) 
            images = coco.loadImgs(iids)
            annotations = coco.loadAnns(iids)
            newcoco = self.getcoco(images,annotations) 
            splitdatas.append(newcoco)
        self.splitdatas = splitdatas
        return splitdatas
    
    '''
        数据生成
    '''
    def generator(self,save_path):
        raise NotImplementedError 
    
    '''
        数据分析
    '''
    def eda(self,savepath,show = False):
        raise NotImplementedError 
    
    
    def getcoco(self,images=None,annotations=None,categories=None): 
        if not images :
            images = self.images
        if not annotations :
            annotations = self.annotations
        if not categories :
            categories = self.categories
            
        dataset = {"images": images, "type": "instances", "annotations": annotations, "categories": categories} 
        coco = COCO() 
        coco.dataset = dataset
        coco.createIndex()
        return coco

    # 数据比例分割
    def get_percent(self,division_ratio):
        ps = []
        p = 0
        for i in division_ratio:
            p = p + i
        for i in division_ratio:
            px = i / p
            ps.append(px) 
        
        return ps


    def imread(self,img_path):
        img = cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)
        '''
        打印异常图片
        try:
            img.shape[2]
        except:
            print(img_path)
        '''
        if len(img.shape) != 3:
            #img = img.unsqueeze(0)
            image  = np.expand_dims(img, axis=2)
            img = np.concatenate((image , image , image ), axis=-1)
        return img
    
class ImageInfo():
    def __init__(self,iid,file_name,height,width): 
        self.id = iid
        self.file_name = file_name
        self.height = height
        self.width = width

class CategorieInfo():
    def __init__(self,cid,name,supercategory=None): 
        self.id = cid
        self.name = name
        self.supercategory = supercategory
        
     
class AnnotationInfo():
    def __init__(self,aid,image_id,category_id,bbox=[],area='',iscrowd = 0,ignore=None,segmentation=[]):  
        self.id = aid
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox
        self.area = area
        self.iscrowd = iscrowd
        self.ignore = ignore
        self.segmentation = segmentation
        