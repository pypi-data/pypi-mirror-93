# -*- coding: utf-8 -*-
'''
Created on 2020-12-6

@author: zhys513(254851907@qq.com)
'''
from opspipe.ops.deploy.docker_client import DockerClient 
from opspipe.ops.deploy.ssh_client import SSHClient 


SSH = SSHClient().sshConnection('192.168.54.22','root', 'yirong123',10022)
DOCKER = DockerClient(SSH)
result = DOCKER.build('test111','/root/pack_tmp/aip')
'''
result = DOCKER.stop('ai_special_1.0')
print(result)
result = DOCKER.start('ai_special_1.0')
print(result)
'''
#result = DOCKER.logs('ai_special_1.0',10)
print(result)