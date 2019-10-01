#!/usr/bin/python3
import hmac
import base64
import binascii
import struct
import smtplib 
import subprocess,sys
from hashlib import sha1
from Signature import *
from stegano import *
from Qrcode import *
#from CreerAttestation import *
stat=[]
def extraireInfos(file):
	mon_image = Image.open(file)
	taille = 1846
	message =""
	message = recuperer(mon_image,taille)
	return  message

def VerifyHorodatage(datas,infos):
	print("Lancement de la verification de l'horodatage ...!!!")
	data =binascii.a2b_base64(datas)
	f = open("horodate.tsr","wb")
	f.write(data)
	f.close()
	verify ="openssl ts -verify  -in "+f.name+" -queryfile TSA/"+infos[0]+".tsq -CAfile TSA/cacert.pem -untrusted TSA/tsa.crt"
	p = subprocess.Popen(verify, stdout=subprocess.PIPE,shell=True)
	(response,error)= p.communicate()
	time.sleep(2)
	if "OK" in response.decode('utf-8'):
		print("La verification de l'horodatage à reussie avec succèes !!!")
		stat.append("timestamp")
	else:
		print("La verification de l'horodatage à echoué")
	return "TSA/"+infos[0]+".tsr"

def extraction(file):
	data=extraireInfos(file)
	infos=data[:64]
	datas=data[64:]
	infos=infos.split('.')
	infos=infos[0].split(':')
	perso = infos[0].split('@',1)
	intitule = infos[1]
	infos=[perso[0],perso[1],intitule]
	signature = extraire(file)
	s=verifySign(infos,signature)
	if s==True:
		stat.append("signature")
	VerifyHorodatage(datas,infos)

if 2 != len(sys.argv):
	print("Usage : python3 "+ sys.argv[0] + " file.png")
	exit(1)
extraction(sys.argv[1])
if len(stat)==2:
	print("L'image est verifié et est valide")
#extraire("final_attestation.png")
