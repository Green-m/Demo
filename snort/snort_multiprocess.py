#! -*- coding:utf-8 -*-
import glob
import subprocess
from time import sleep
import psutil
import timeit
import os
import json
import logging
import ConfigParser 
import threadpool
import math

logging.basicConfig(filename='./snort.log',level=logging.DEBUG,format='[%(levelname)s]%(asctime)s:%(message)s', datefmt='%Y%m%d%I%M')

snort_command = 'snort -c /etc/snort/snort.conf -q -l /var/log/snort --pcap-list '
DIR_TMP = './snort.tmp'
config=ConfigParser.ConfigParser() 


def process_openfiles(processname):
    opening_files = []
    for proc in psutil.process_iter():
        try:
            if processname in proc.name():
                flist = proc.open_files()
                for file in flist:
                    opening_files.append(file.path)
        except psutil.NoSuchProcess as err:
            logging.info("****",err) 

    return opening_files


def call_snort(pcaplist_tohandle):
    snort_command = 'snort -c /etc/snort/snort.conf -q -l /var/log/snort --pcap-list '
    snort_option = snort_command + '"{}"'.format(" ".join(pcaplist_tohandle))

    command = subprocess.Popen(snort_option,shell=True)
    command.wait()

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


if __name__ == "__main__":

    pcaplist_handled = []
    pcaplist_tohandle = []

    if os.path.exists(DIR_TMP):
        with open(DIR_TMP, 'r') as the_file:
            pcaplist_handled = json.load(the_file)
            logging.info("Loading tmp file..")


    cycletime = 1
    while True:

        pcaplist_total = []
        opening_files = []
        opening_files = process_openfiles('dumpcap')


        with open('./snort.conf','r') as cfgfile: 
            config.readfp(cfgfile) 

        dir_pcap_list = config.get('config','dir_pcap_list').split(',')

        try:
            for dir_pcap in dir_pcap_list:
                pcaplist_total += glob.glob(dir_pcap + '/*.pcap')
        except Exception as e:
            logging.error(e.message)

        pcaplist_total = list(set(pcaplist_total) - set(opening_files))
        pcaplist_tohandle = list(set(pcaplist_total) - set(pcaplist_handled))


        if len(pcaplist_tohandle) < 3:
            logging.info("Waiting for more pcap files for {} times...".format(cycletime))
            sleeptime = 10*cycletime
            if sleeptime > 600:
                sleep(600)
            else:
                sleep(sleeptime)
            cycletime +=1
            continue

        cycletime=1
        snort_option = snort_command + '"{}"'.format(" ".join(pcaplist_tohandle))

        logging.info("Snort is starting to analyze {} pcap files...".format(len(pcaplist_tohandle)))

        # chunks array to 8 chunks
        pcaplist_tohandle_chunked = chunks(pcaplist_tohandle,8)

        start_time = timeit.default_timer()
        pool = threadpool.ThreadPool(8) # most 8 processes 
        reqs = threadpool.makeRequests(call_snort, pcaplist_tohandle_chunked)
        [pool.putRequest(req) for req in reqs]
        pool.wait()
        
        stop_time = timeit.default_timer()
        logging.info("Snort analyze end")
        logging.info("Total time {}s,{} files, {}s/file".format(round(stop_time-start_time,2),len(pcaplist_tohandle),round((stop_time-start_time)/len(pcaplist_tohandle),2)))

        pcaplist_handled += pcaplist_tohandle


        # writing temp files
        with open(DIR_TMP, 'w') as the_file:
            the_file.truncate()
            json.dump(pcaplist_handled,the_file)

        #sleep(1)

