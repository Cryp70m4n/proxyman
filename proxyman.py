#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
from threading import Thread
from queue import Queue
from urllib.parse import unquote
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import signal
import sys
import pyfiglet

from config import *

c = ProxymanConfig.ParseConfig("config.json")

source_timeout = c.source_timeout
proxy_timeout = c.proxy_timeout
threads = c.threads
db = c.db_path
port = c.port

thread_list = []
thread_list2 = []
reggy=r'([0-9.]{7,20})(:[0-9]{2,4})'
reggy2=r'[0-9.]{2,16}\n'

supported_types = ["http", "socks4", "socks5"]


global queue
queue = Queue()


class EnumerationWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.id = 0

    def run(self):
        while True:
            proxy = self.queue.get()
            try:
                proxy_check(proxy)
            finally:
                self.queue.task_done()


def thread_enumeration(proxies):
    for thread in range(threads):
        worker = EnumerationWorker(queue)
        worker.daemon = True
        worker.id = thread
        worker.start()
    for proxy in proxies:
        queue.put(proxy)

    queue.join()

try:
    conn = sqlite3.connect(db, check_same_thread=False)
    cursor = conn.cursor()
except Error as e:
    print(e)

def signal_handler(sig, frame):
    conn.close()
    sys.exit("\nProxyman successfully exited!")

signal.signal(signal.SIGINT, signal_handler)



def http_check(proxy_to_check):
    try:
        proxy = 'http://' + proxy_to_check
        proxies = {
            'http':     proxy,
            'https':    proxy
        }

        check = requests.get("https://api.ipify.org", proxies=proxies, timeout = proxy_timeout)
        sql = "INSERT OR IGNORE INTO http(proxy) VALUES(?)"
        cursor.execute(sql, [proxy_to_check])
        conn.commit()
        #print("Proxy works:", proxy_to_check, " | ", "Proxy type:http", " | ", "Response time:", check.elapsed.total_seconds())
        return "http"
    except:
        return "Unsuccess!"

def socks4_check(proxy_to_check):
    try:
        proxy = 'socks4://' + proxy_to_check
        proxies = {
            'http':     proxy,
            'https':    proxy
        }

        check = requests.get("https://api.ipify.org", proxies=proxies, timeout = proxy_timeout)
        sql = "INSERT OR IGNORE INTO socks4(proxy) VALUES(?)"
        cursor.execute(sql, [proxy_to_check])
        conn.commit()
        #print("Proxy works:", proxy_to_check, " | ", "Proxy type:socks4", " | ", "Response time:", check.elapsed.total_seconds())
        return "socks4"
    except:
        return "Unsuccess!"

def socks5_check(proxy_to_check):
    try:
        proxy = 'socks5://' + proxy_to_check
        proxies = {
            'http':     proxy,
            'https':    proxy
        }

        check = requests.get("https://api.ipify.org", proxies=proxies, timeout = proxy_timeout)
        sql = "INSERT OR IGNORE INTO socks5(proxy) VALUES(?)"
        cursor.execute(sql, [proxy_to_check])
        conn.commit()
        #print("Proxy works:", proxy_to_check, " | ", "Proxy type:socks5", " | ", "Response time:", check.elapsed.total_seconds())
        return "socks5"
    except:
        return "Unsuccess!"


def show_sources():
    cursor.execute("SELECT * FROM sources")
    rows = cursor.fetchall()
    sources = {}
    index = 0
    while index < len(rows):
        for source in rows:
            sources[index] = source[0]
            index+=1
    return sources

def add_source(source):
    sql = "INSERT OR IGNORE INTO sources(source) VALUES(?)"
    cursor.execute(sql, [source])
    conn.commit()
    return f"Successfully added {source} into sources table"


def remove_source(source):
    sql = "DELETE FROM sources WHERE source = ?"
    cursor.execute(sql, [source])
    conn.commit()
    return f"Successfully deleted {source} from sources table"


def proxy_check(proxy_to_check):
    if http_check(proxy_to_check) != "Unsuccess!":
        return "http"
    if socks4_check(proxy_to_check) != "Unsuccess!":
        return "socks4"
    if socks5_check(proxy_check) != "Unsuccess!":
        return "socks5"
    else:
        return f"Proxy doesn't work {proxy_check}"





def refresh_proxies(refreshes):
    if type(refreshes) != int: return "refreshes argument must be an int value"
    if refreshes < 1: return "refreshes argument must be higher than 0"

    refreshes_counter = 0
    while refreshes_counter < refreshes:
        cursor.execute("SELECT * FROM sources");
        rows = cursor.fetchall()
        if rows == []:
            return "There are no sources in database.\nInsert sources into database in order to refresh proxies."

        for link in rows:
            try:
                link = link[0]
                matches = requests.get(unquote(link.replace("\n", "")), timeout=source_timeout)
                matches = matches.text
                if(len(re.findall(reggy, matches)) > 2):
                    proxy = re.findall(reggy,matches)
                    proxy_list_1 = []
                    for found in proxy:
                        found_proxy = found[0]+found[1].replace("\n", "")
                        proxy_list_1.append(found_proxy)
                    thread_enumeration(proxy_list_1)

                elif(len(re.findall(reggy,matches))<2) and (len(re.findall(reggy2,matches))>2):
                    proxy = re.findall(reggy2, matches)
                    for found in range(len(proxy)):
                        proxy_list_2 = []
                        if len(proxy[found]) > 7:
                            found_proxy = proxy[found].replace("\n", "") + ":" + proxy[found+1].replace("\n", "")
                            proxy_list_2.append(found_proxy)
                                
                        thread_enumeration(proxy_list_2)
            except:
                pass

        refreshes_counter+=1
        
    return "Success!"

def get_proxies(proxy_type, proxy_amount):
    if type(proxy_amount) != int: return "proxy_amount argument must be an int value"
    if proxy_amount < 1: return "proxy_amount argument must be higher than 0"

    if proxy_type not in supported_types:
        return "Invalid proxy type\nSupported types:http, socks4, socks5"

    sql = f"SELECT * FROM {proxy_type} LIMIT {proxy_amount}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    proxies = {}
    index = 0
    while index < len(rows):
        for proxy in rows:
            proxies[index] = proxy[0]
            index+=1

    return jsonify(proxies)



app = Flask(__name__)

@app.route('/')
def index():
    return 'Proxyman best proxy scraper!'


@app.route('/api/show_sources', methods=['GET'])
def list_sources():
    return show_sources()

@app.route('/api/add_source', methods=['POST'])
def source():
    source = request.args.get("source")
    return add_source(source)

@app.route('/api/remove_source', methods=['POST'])
def delete_source():
    source = request.args.get("source")
    return remove_source(source)


@app.route('/api/refresh_proxies', methods=['POST'])
def scrap_proxies():
    refreshes = request.args.get("refreshes")
    return refresh_proxies(int(refreshes))

@app.route('/api/get_proxies', methods=['GET'])
def get_proxies_params():
    proxy_type = request.args.get("proxy_type")
    proxy_amount = request.args.get("proxy_amount")
    return get_proxies(proxy_type, int(proxy_amount))



if (__name__ == "__main__"):
    banner = pyfiglet.figlet_format("Proxyman")
    print(banner)
    #app.run(port=port, debug=False,use_reloader=False)
    http_server = WSGIServer(('127.0.0.1', port), app)
    print(f"Starting the webserver on http://127.0.0.1:{port}")
    http_server.serve_forever()
