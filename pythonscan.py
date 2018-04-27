#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libnmap.reportjson import ReportDecoder,ReportEncoder
from libnmap.plugins.mongodb import NmapMongodbPlugin
from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep
import json


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmap_proc = NmapProcess(targets, options)
    nmap_proc.run_background()
    rc = nmap_proc.rc

    if rc != 0:
        print("nmap scan failed: {0}".format(nmap_proc.stderr))
    #print(type(nmap_proc.stdout))

    while nmap_proc.is_running():
        print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,
                                                          nmap_proc.progress))
        sleep(2)

    try:
        parsed = NmapParser.parse(nmap_proc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
    print(nmap_report.summary)

def print_scan_all(nmap_report):
    print nmap_report.hosts
    for host in nmap_report.hosts:
        for serv in host.services:
        	print serv

def connect_db():
    db = NmapMongodbPlugin(host=['localhost:27017'])
    return db

def insertrep_db(nmap_report):
    db = connect_db()
    dbid = db.insert(nmap_report)
    return dbid

def getrep_db(dbid):	
    db = connect_db()
    nmap_report = db.get(dbid)
    return nmap_report

def get_targets():
    targets = None
    #try
    targets = '127.0.0.1,110.201.80.187,10.201.80.242'
    #targets = ['108.61.119.230','108.61.119.111']
    return targets

def get_ports():
    ports = None
    #try
    ports = ['22','80','443','3306','8080']
    ports = ",".join(ports)
    return ports

def generate_option():
    option = None
    ports = get_ports()
    #try
    option = "-sV -T2 -p" + ports 
    return option


if __name__ == "__main__":
    targets = get_targets()
    option = generate_option()
    report = do_scan(targets, option)
    j = json.dumps(report, cls=ReportEncoder)
    report_json = json.loads(j)
    if report:
        #dbid = insertrep_db(report)
        #report = getrep_db(dbid)
        print_scan(report)
        print report_json,type(report_json)
        print j,type(j)
    else:
        print("No results returned")
