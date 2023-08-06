# -*- coding: utf-8 -*-
'''
Created on 2021-1-10

@author: zhys513(254851907@qq.com)
'''
import os,json
from pycocotools.coco import COCO
from functools import reduce

from opspipe.pipe.cv.data.base import Base

class MsCoco(Base): 
    def __init__(self,images=[],annotations = [],categories = []): 
        Base.__init__(self,images,annotations,categories)  
    
    def load(self,path,data_types=['train'],newId = True):  
        annotations_path = os.path.join(path,'annotations')
        images_path = os.path.join(path,'images')
        # annid重新生成 imgId默认重新生成，根据newId可以配置不重新生成，起始ID为1
        newimgId = 1
        newannId = 1
        # 支持多个数据集进行合并,data_types为空读取annotations下所有数据集
        if data_types:
            pass
        for datatype in data_types:
            annFile = '{}.json'.format(datatype)
            annpath = os.path.join(annotations_path,annFile)
            coco = COCO(annpath) 
            imgIds = coco.getImgIds()
            for imgId in imgIds:
                annIds = coco.getAnnIds(imgIds=[imgId],  iscrowd=None)
                anns = coco.loadAnns(annIds) 
                img = coco.loadImgs(imgId)[0] 
                if newId:
                    imgpath = os.path.join(images_path,datatype)
                    img['id'] = newimgId
                    img['path'] = imgpath
                    newimgId = newimgId + 1
                self.images.append(img)
                for ann in anns:    
                    ann['id'] = newannId
                    newannId = newannId + 1
                    ann['image_id'] = img['id'] 
                    self.annotations.append(ann)
            # cats累加
            self.categories = self.categories + coco.dataset['categories'] 
        # 去重
        self.categories = reduce(lambda x, y: x if y in x else x + [y], [[], ] + self.categories)


    def generator(self,save_path,data_types=['train','val','test']):
        assert len(self.splitdatas) != len(data_types) ,'splitdatas != data_types len'
        for datas in zip(self.splitdatas,data_types):
            print(datas)
        
