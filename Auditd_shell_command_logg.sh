#!/bin/bash
auditctl -b 8192 
auditctl -a always,exclude -F msgtype=PATH
auditctl -a always,exclude -F msgtype!=CWD -F msgtype!=SYSCALL -F msgtype!=EXECVE -F msgtype!=USER_LOGIN
auditctl -a exit,never  -F arch=b64 -F auid=4294967295
auditctl -a exit,always -F arch=b64 -F euid=0 -S execve -k rootact
auditctl -a exit,always -F arch=b32 -F euid=0 -S execve -k rootact
auditctl -a exit,always -F arch=b64 -F euid>=1000 -S execve -k useract
auditctl -a exit,always -F arch=b32 -F euid>=1000 -S execve -k useract
