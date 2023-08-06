#!/usr/bin/env python
# coding:utf-8
''' 
@attention: ssh客户端使用 
'''
import paramiko
from paramiko.py3compat import u
import time
class SSHClient(object): 
    def __init__(self): 
        self.ssh = None
    
    '''
    @attention: 关闭 ssh 链接 
    @param ssh: ssh链接
    '''
    def close(self):
        self.ssh.close()
    '''
    @attention: 创建 ssh 链接 
    @param v_username: 用户名
    @param v_password: 密码
    @param v_ip: IP
    @param v_port: 端口号
    '''
    def sshConnection(self, v_ip, v_username, v_password,  v_port=22):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=v_ip, port=v_port, username=v_username, password=v_password)
        self.ssh = ssh
        return self
    # endregion
    '''
    @attention: 执行单条命令 
    @param ssh: ssh链接
    @param v_cmd: 需要执行的命令
    '''
    def sshExecByOne(self, v_cmd): 
        assert self.ssh,'ssh is None ,set sshConnection now'
        # 执行
        stdin, stdout, stderr = self.ssh.exec_command(v_cmd)
        result = stdout.read()
         
        if not result:
            result = stderr.read()
        return result.decode()
    '''
    @attention: 执行命令集
    @author: 白瑞钧
    @param s: ssh链接
    @param l_cmd: 需要执行的命令集
    @param exec_wait: 执行命令间隔时间
    @param exit_wait: 退出等待时间
    '''
    def sshExecByMany(self,l_cmd, exec_wait=1, exit_wait=1):
        assert self.ssh,'ssh is None ,set sshConnection now'
        
        ssh = self.ssh.invoke_shell()
        # 执行
        for v_cmd in l_cmd:
            ssh.send(v_cmd)
            ssh.send('\n')
            time.sleep(exec_wait)
            if v_cmd=='exit':
                time.sleep(exit_wait)
        result = u(ssh.recv(9999))
        return result
    

if __name__ == '__main__':
    SSH = SSHClient().sshConnection('192.168.54.22','root', 'yirong123',10022) 
    l_cmd = ['docker ps -a']
    result = SSH.sshExecByMany(l_cmd, 1, 1)
    print(result)
    SSH.close()
    # getClient = SSHClient()
    # ssh = getClient.sshConnection('sys_admin', 'XSW@1qaz', '10.82.28.219')
    # result = getClient.sshExecByOne(ssh,'pwd')
    # print(result)
    # getClient.close(ssh)
''' '''