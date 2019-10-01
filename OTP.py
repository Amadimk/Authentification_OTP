#!/usr/bin/python
# coding=utf8
import base64
import time 
import hashlib
import hmac
import subprocess
from hashlib import sha1
from hashlib import sha256
import getpass
import math


def  GoogleAuthenticatorCode(secret):
	args="date +%s"
	p = subprocess.Popen(args, stdout=subprocess.PIPE,shell=True)
	(times,error)= p.communicate()
	times=times.decode('utf-8').replace('\n','') 
	datee = int(int(times)//30)
	key = base64.b32decode(secret)
	# encodage de la date en bytes necessaire pour la fonction hmac python3
	result = bytes(str(datee),'utf-8')
	hash=hmac.new(key, result, sha1)
	octets=hash.digest()
	offset=octets[-1] & 0xf
	truncatedhash= ((octets[offset] & 0x7f) << 24 |(octets[offset + 1] & 0xff) << 16 | (octets[offset + 2] & 0xff) << 8 | (octets[offset + 3] & 0xff))
	code = truncatedhash % 1000000 
	while len(str(code)) < 6:
		code = '0'+str(code)
	return [times,code]

def CalculOTP():
        print("**************Welcome to Certiplus OTP Portal************************")
        print("*                                                                   *")
        print("* Authentification OTP (one time password) Certiplus                *")
        print("*                                                                   *")
        print("**************CertiPlus CopyRight Inc Unilim ************************")
        print("")
        print("")
        secret=getpass.getpass(prompt='Enter your secret : ')
        secret= base64.b32encode(bytes(secret.upper(),'utf-8'))
        client_otp = GoogleAuthenticatorCode(secret)
        print("date utilsée : ",client_otp[0])
        print("OTP : " ,client_otp[1])
        return client_otp

