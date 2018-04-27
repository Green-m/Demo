require 'socket'
require 'timeout'
require 'date'
require 'thread'

class Scanner

	def initialize
		@hosts,@ports = Array(ARGV)
	end

	def posts_get
		case @ports
		when /^\d+[-]/
			@ports = @ports.split("-")
			@ports = @ports[0].to_i..@ports[1].to_i
		when /^\d+[,]/
			@ports = @ports.split(",")
		when /^\d+/
			@ports = Array(@ports)
		else
			puts "invaid arguments,eg. 100-200 or 10,20,30"
			exit
		end
	end

	def hosts_get
		case @hosts
		when /^\d+[.]+\d+[.]+\d+[.]+\d+$/
			@hosts = Array(@hosts)
		when /^\d+[.]+\d+[.]+\d+[.]+\d+[,].+/
			@hosts = @hosts.split(",")
			#puts @hosts
			#@hosts
		when /^\/+.+/
			#puts ARGV[0]
			tmp = []
			File.open(ARGV[0],"r") do |file|
				while line  = file.gets
					tmp << line if !line.strip!.empty?#打印出文件内容
				end
			end
			@hosts = tmp.uniq
		when /[A-Za-z]:[\\\/].+/
			dir = ARGV[0].gsub(/[\/\\]/,'\\')
			tmp = []
			File.open(dir,"r") do |file|
				while line  = file.gets
					tmp << line if !line.strip!.empty? #打印出文件内容
				end
			end
			@hosts = tmp.uniq
			
		else
			puts "invaid arguments,eg 192.168.1.1 or /root/Desktop/123.txt"
			exit
		end
	end

	def output(host,state,port)
		puts"#{host}:#{port}\t#{state}" 
		sleep(1)
	end

	def scanning(hosts,ports,thread_num = 5,timeout_time = 3)
		result = Hash.new()
		#port_open = Array.new()
		hosts.each{|host|result.merge!({host => []})}
		thread_num = ARGV[2] || thread_num 
		timeout_time = ARGV[3] ||timeout_time
		@queue = Queue.new
		hosts.length.times do |i|
			@queue.push(hosts[i])
		end
		threads = []
		puts "Scanning start"
		$total_time_begin = Time.now.to_f
		thread_num.to_i.times do
			threads << Thread.new do 
				until @queue.empty?
					host = @queue.pop(true) rescue nil
					begin
						ports.each do |port|
							begin
								Timeout::timeout(timeout_time.to_i) do 
									if TCPSocket.open(host, port) 
										sleep(1)
										output(host,"open",port)
										result[host] << port
										#puts "#{host} open port #{result[host]}"
									end
								end
							rescue Timeout::Error
								output(host,"filtered",port)
							rescue Errno::ECONNREFUSED
								output(host,"closed",port)
							rescue SocketError
								puts "invaid host: #{host}"
								break
							end
						end
					end
					#puts "#{host}:#{result[host]}"  if !result[host].empty?
				end
			end
		end
		threads.each{|t|t.join}
		$total_time_end = Time.now.to_f
		puts "Scanning ended"
		puts "Total ip #{@hosts.length}\nTotal ports #{@hosts.length*@ports.length}"
		print "IP\t\tOPEN_PORT\n"
		result.each do |key,value|
			if !value.empty?
				print "#{key}\t" 
				value.each {|x| print ("#{x} ")}
				print "\n"
			end
		end
		puts "Used time：" + ($total_time_end - $total_time_begin).to_s + "s"
	end
end

##################### code start #####################
puts "invaid arguments,correct usage:\nruby #{$0} [hosts] [ports] [threads = 5] [timeout = 3]\n" if ARGV.size < 2
my_scanner = Scanner.new
hosts = my_scanner.hosts_get
ports = my_scanner.posts_get

my_scanner.scanning(hosts,ports)

##################### eof #####################
