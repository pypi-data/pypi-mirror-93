# -*- coding: utf-8 -*-
'''
Created on 2020-12-6
使用 ssh 远程对Docker命令操作
@author: zhys513(254851907@qq.com)
'''

class DockerClient(object): 
    def __init__(self,SSHClient): 
        self.ssh = SSHClient
        
    def build(self,img,memu):
        v_cd = 'cd ' + memu
        v_cmd = 'docker build -t ' + img + ' .'
        if memu:
            v_cmd = v_cd + ' && ' + v_cmd
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
    
    def pull(self,img,usr='',pwd=''):
        v_cmds = 'docker pull ' + img
        if usr:
            v_cmds = ['docker login -u ' + usr + ' -p ' + pwd] + v_cmds
        result = self.ssh.sshExecByMany(v_cmds) 
        return result
        
    def push(self,img,usr='',pwd =''): 
        v_cmds = ['docker push ' + img] 
        if usr:
            v_cmds = ['docker login -u ' + usr + ' -p ' + pwd] + v_cmds
        result = self.ssh.sshExecByMany(v_cmds) 
        return result
     
    def run_cpu(self,img,v_para=''):
        v_cmd = 'docker run -d ' + img + ' ' + v_para
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
    
    def run_gpu(self,img,v_para=''):
        v_cmd = 'nvidia-docker run -d ' + img + ' ' + v_para
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
        
    def start(self,container):
        v_cmd = 'docker start ' + container
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
         
    def ps(self,v_para='-a'):
        v_cmd = 'docker ps ' + v_para 
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
         
    def stop(self,container):
        v_cmd = 'docker stop ' + container
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
    
    def load(self,img):
        v_cmd = 'docker load < ' + img
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
      
    def rm(self,container):
        v_cmd = 'docker rm -f ' + container
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
        
    def rmi(self,img):
        v_cmd = 'docker rmi -f ' + img
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
         
    def logs(self,container,tail = 0):
        v_cmd = 'docker logs ' + container
        if tail > 0: 
            v_cmd = 'docker logs --tail=' + str(tail) + ' ' + container
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
    
    
    def pid(self,container):
        v_cmd = "docker inspect -f '{{.State.Pid}}'" + container 
        result = self.ssh.sshExecByOne(v_cmd) 
        return result
 
        
    
    