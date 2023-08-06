# -*- coding: utf-8 -*-
'''
Created on 2021-1-28

@author: zhys513(254851907@qq.com)
'''

class GitClient(object): 
    def __init__(self,SSHClient): 
        self.ssh = SSHClient
    
    def login(self,url,usr='',pwd=''):
        pass
        
    def clone(self,url):
        v_cmds = 'git clone ' + url
        result = self.ssh.sshExecByOne(v_cmds) 
        return result
    
    def pull(self,url):
        v_cmds = 'git pull ' + url
        result = self.ssh.sshExecByOne(v_cmds) 
        return result
