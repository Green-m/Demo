#!/bin/bash
# install snort
sudo yum check-update
sudo yum -y install gcc flex bison zlib libpcap pcre libdnet tcpdump wireshark libnghttp2 git libtool mysql-devel libpcap-devel daq-devel libdnet-devel python-devel python2-pip
sudo yum -y install https://www.snort.org/downloads/snort/snort-2.9.11-1.centos7.x86_64.rpm
sudo ln -s /usr/lib64/libdnet.so.1 /usr/local/lib/libdnet.1
mkdir -p /usr/local/lib/snort_dynamicrules
chown -R snort:snort /usr/local/lib/snort_dynamicrules
chmod -R 700 /usr/local/lib/snort_dynamicrules

# download snort rules 
# Before you download the snortrules-snapshot-29110.tar.gz you have to register, otherwise you could download community-rules.tar.gz instead.
sudo cd /etc/snort/
wget https://www.snort.org/downloads/registered/snortrules-snapshot-29110.tar.gz -O /tmp/snortrules-snapshot-29110.tar.gz
sudo tar -xf /tmp/snortrules-snapshot-29110.tar.gz -C /etc/snort/
sudo rm /tmp/snortrules-snapshot-29110.tar.gz
touch /etc/snort/rules/white_list.rules
touch /etc/snort/rules/black_list.rules

#install barnyard2
wget https://github.com/firnsy/barnyard2/archive/master.zip -O /root/barnyard2.zip
unzip /root/barnyard2.zip -d /root/
sudo rm /root/barnyard2.zip
cd /root/barnyard2-master/
./autogen.sh
./configure --with-mysql --with-mysql-libraries=/usr/lib64/mysql
make && make install
mkdir /var/log/barnyard2
touch /var/log/snort/barnyard2.waldo
cp ./rpm/barnyard2 /etc/init.d/
chmod +x /etc/init.d/barnyard2
cp ./rpm/barnyard2.config /etc/sysconfig/barnyard2
chkconfig --add barnyard2
ln -s /usr/local/etc/barnyard2.conf /etc/snort/barnyard.conf
ln -s /usr/local/bin/barnyard2 /usr/bin/
chown snort.snort /var/log/barnyard2
chown -R snort:snort /var/log/snort
chown snort.snort /var/log/snort/barnyard2.waldo
cp /etc/snort/etc/sid-msg.map /etc/snort
