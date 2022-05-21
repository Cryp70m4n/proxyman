#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

pip = ""
res = os.system("pip --version")
if res == 0:
    pip = "pip"

res2 = os.system("pip3 --version")
if res2 == 0:
    pip = "pip3"

else:
    print("Please install pip and run setup again in order to run Proxyman")

try:
    os.system("pip3 --version")
    pip = "pip3"
except:
    print("Please install pip and run setup again in order to use Proxyman")
    exit()

if "requests" not in sys.modules:
    os.system(f"{pip} install requests")
if "sqlite" not in sys.modules:
    os.system(f"{pip} install sqlite")
if "flask" not in sys.modules:
    os.system(f"{pip} install flask")
if "gevent" not in sys.modules:
    os.system(f"{pip} install gevent")
if "pyfiglet" not in sys.modules:
    os.system(f"{pip} install pyfiglet")

os.system(f"{pip} install -U 'requests[socks]'")

try:
    os.system("sqlite3 proxys.db 'CREATE TABLE sources(source VARCHAR(255) UNIQUE NOT NULL); CREATE TABLE http(proxy VARCHAR(24) UNIQUE NOT NULL); CREATE TABLE socks4(proxy VARCHAR(24) UNIQUE NOT NULL); CREATE TABLE socks5(proxy VARCHAR(24) UNIQUE NOT NULL);'")
except:
    print("Please install sqlite3 and run setup again in order to run Proxyman")

