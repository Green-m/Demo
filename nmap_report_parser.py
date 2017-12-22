#! -*- coding:utf-8 -*-

from libnmap.parser import NmapParser
import sys
import os.path
import json

class NmapReportParser(object):

    def __init__(self,filename):
        self.filename = filename

    def get_report_xml(self):
        self.nmap_report = NmapParser.parse_fromfile(self.filename) 

    def get_report_json(self):
        json_file = json.load(open(self.filename))
        self.nmap_report = NmapParser.parse_fromdict(json_file) 

    def all_product_list(self):
        return sorted(set([ b.banner for a in self.nmap_report.hosts for b in a.services if 'product' in b.banner]))

    def open_port_hosts_list(self,portnumber):
        return [ a.address for a in self.nmap_report.hosts if (a.get_open_ports()) and portnumber in [b[0] for b in a.get_open_ports()] ]

    def open_product_hosts_list(self,servicename,verbose=False):
        
        if verbose:
            hosts_list =  [ [a.address,  b.port] for a in self.nmap_report.hosts for b in a.services if servicename.lower() in str(b.banner).lower()  ]
        else:
            hosts_list =  [ [a.address,  b.port, str(b.banner)] for a in self.nmap_report.hosts for b in a.services if servicename.lower() in str(b.banner).lower()  ]

        return hosts_list

    def find_fingerprint_hosts_list(self,fingerprint,verbose=False):
        if verbose:
            return [ [a.address, b.port, b.servicefp] for a in self.nmap_report.hosts for b in a.services if b.open() and fingerprint.lower() in (str(b.get_dict()) + str(b.servicefp)).lower() ]
        else:
            return [ ':'.join([a.address,  str(b.port)]) for a in self.nmap_report.hosts for b in a.services if b.open() and fingerprint.lower() in (str(b.get_dict()) + str(b.servicefp)).lower() ]


if __name__ == "__main__":
    nmap_report = NmapReportParser(sys.argv[1])
    extension = os.path.splitext(sys.argv[1])[1][1:]
    if extension == 'xml':
        nmap_report.get_report_xml()
    if extension == 'json':
        nmap_report.get_report_json()

    print "---------------------usage-------------------"
    print "'all' means print all kinds of product"
    print "'80' means print port 80 opened host "
    print "'tomcat'  means print host which has tomcat ,not case sensitive "
    #print "-------------------------------------------------"

    while True:
        print "----------------input command--------------"
        cmd = sys.stdin.readline().rstrip()
        
        if not cmd:
            continue
        try:
            if cmd == 'all':
                print "--------------------All Product-------------------"
                for product in nmap_report.all_product_list():
                    print product.lstrip('product: ')

            elif cmd.isdigit() and int(cmd) > 1 and int(cmd) < 65536:
                print "--------------------Open Port {0}-------------------".format(cmd)
                for host in nmap_report.open_port_hosts_list(int(cmd)):
                    print host

            else:
                print "--------------------Find Product {0}-------------------".format(cmd)
                style = '{0}:{1}\t\t{2}'
                for host in nmap_report.open_product_hosts_list(cmd):
                    print style.format(*host)

        except Exception as err:
            if isinstance(err, KeyboardInterrupt):
                break

            print repr(err)


