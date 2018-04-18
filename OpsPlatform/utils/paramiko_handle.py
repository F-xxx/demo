# -*- coding:utf-8 -*-  

import paramiko
from .config import SER_INFO

class Task(object):
    def __init__(self,request):
        self.request = request
        self.plat = self.request.POST.get('platform')
        self.zone = self.request.POST.get('zone')
        self.operate = self.request.POST.get('operate')

    def ssh_conn(self):
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.zone == 'w':
            host = SER_INFO['WA']['host']
            user = SER_INFO['WA']['user']
            pwd = SER_INFO['WA']['pwd']
            port = SER_INFO['WA']['port']
        else:
            host = SER_INFO['LA']['host']
            user = SER_INFO['LA']['user']
            pwd = SER_INFO['LA']['pwd']
            port = SER_INFO['LA']['port']
        s.connect(hostname=host,username=user,password=pwd,port=port,timeout=5)


    def run(self):
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.zone == 'w':
            host = SER_INFO['WA']['host']
            user = SER_INFO['WA']['user']
            pwd = SER_INFO['WA']['pwd']
            port = SER_INFO['WA']['port']
        else:
            host = SER_INFO['LA']['host']
            user = SER_INFO['LA']['user']
            pwd = SER_INFO['LA']['pwd']
            port = SER_INFO['LA']['port']
        s.connect(hostname=host, username=user, password=pwd, port=port, timeout=5)
        if self.plat == 'gp':
            plat = 'google'
        else:
            plat = 'ios'

        if self.operate == 'b':
            cmd = '/usr/bin/python /data/salt/scripts/bxx %s' % plat
        else:
            cmd = '/usr/bin/python /data/salt/scripts/xxx %s' % plat
        print(cmd)
        stdin,stdout,stderr = s.exec_command(cmd)
        result = stdout.read(),stderr.read()
        ret = []
        for line in result:
            ret.append(line.decode('utf-8'))
        return ret


