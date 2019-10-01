#! /usr/bin/python3
import hmac
import base64
import binascii
import struct
import smtplib 
import subprocess
from hashlib import sha1
from OTP import GoogleAuthenticatorCode
from Signature import *
from Qrcode import *
import getpass
from stegano import *

SECRET="CERTIPLUS"
def Mail(exp,file,dst):
	print("Envoi du mail en cours ...!!!")
	f=open('piece.txt','w')
	f2=open(file, 'rb')
	file = f2.read()
	f2.close()
	f.write('Content-Type: image/png\r\n')
	f.write('Content-Transfer-Encoding: base64\r\n\r\n')
	piece=binascii.b2a_base64(file, newline=True)
	f.write(piece.decode('ascii'))
	f.close()
	server = smtplib.SMTP_SSL('smtp.unilim.fr',465)
	args = "openssl cms -sign -in piece.txt -signer AC/certiplus.crt -inkey AC/appli.key.pem -from "+exp+" -to "
	args+= dst+ " -subject \"Certiplus - Diplome signer \" -out mail.msg" 
	#| openssl cms -encrypt -out mail.msg -aes256 unilim.fr.cert"
	#args2 ="openssl cms -sign -in piece.txt -signer AC/certiplus.crt -inkey AC/appli.key.pem -from 'amadou-oury.diallo@etu.unilim.fr' -to 'amadimk@gmail.com' -subject 'Certiplus Diplome signer' -out mail.msg"
	subprocess.run(args,shell=True)
	time.sleep(1)
	f=open('mail.msg','r')
	Message =f.read()
	ident = input("Votre identifiant Unilim pour l'envoi du mail : ")
	mdp = getpass.getpass(prompt='votre mot de passe : ')
	server.login(ident,mdp)
	server.sendmail(exp, dst,Message )
	server.quit()
	print("Mail envoyé...!!!")

def Horodatage(file, infos):
	query="openssl ts -query -data "+file+" -no_nonce -sha512 -out TSA/"+infos[0]+".tsq"
	subprocess.run(query,shell=True)
	request="curl -H \"Content-Type: application/timestamp-query\" --data-binary '@TSA/"+infos[0]+".tsq' https://freetsa.org/tsr > TSA/"+infos[0]+".tsr"
	subprocess.run(request,shell=True)
	verify ="openssl ts -verify -data "+file+" -in TSA/"+infos[0]+".tsr  -CAfile TSA/cacert.pem -untrusted TSA/tsa.crt"
	p = subprocess.Popen(verify, stdout=subprocess.PIPE,shell=True)
	(response,error)= p.communicate()
	if "OK" in response.decode('utf-8'):
		print("Horodatage effectué")
	else:
		print("Un erreur est survenue avec le serveur d'horodatage")
	return "TSA/"+infos[0]+".tsr"

def IntegreTexte(texte):
	 subprocess.run('curl -o texte.png "http://chart.apis.google.com/chart" --data-urlencode "chst=d_text_outline" --data-urlencode "chld=000000|56|h|FFFFFF|b|'+texte+'"', shell=True)
	 time.sleep(2)
	 subprocess.run('mogrify -resize 1000x600 texte.png', shell=True)
	 print('Integration texte....Done : texte.png')
	 time.sleep(1)
	 return 'texte.png'

def CombinaisonTexte(file1, file2):
	subprocess.run('composite -gravity center '+file1+' '+file2+' combinaison.png',shell=True)
	print('Combinaison des fichiers : '+file1+' et ' +file2)
	return  'combinaison.png'

#saisie des informations users # 
def Saisie():
	
	OTP=None
	if  2 != len(sys.argv) :
		print("Usage : python3 "+sys.argv[0]+ " 0255466")
		exit(1)
	OTP=sys.argv[1]
	app_secret = base64.b32encode(bytes(SECRET.upper(),'utf-8'))
	app_otp = GoogleAuthenticatorCode(app_secret)
	if int(OTP) == app_otp[1] :
		print("**************Welcome to Certiplus Portal************************")
		print("*       	                           						        *")
		print("* application destiné à la certification des diplômes certiplus  *")
		print("*                                                                *")
		print("**************CertiPlus CopyRight Inc Unilim ********************")
		print("")
		print("")
		name = input("Nom : ")
		lastname = input("Prenom : ")
		description = input("Intitulé [Certification delivré à]: ")
		mail = input("Mail : ")
		texte = "Certificat delivré | à | "+lastname.capitalize()+" "+name.upper()
		infos = [name.upper(),lastname.capitalize(),description.lower()]
		sig=signature(infos)
		filefond="fond_attestation.png"
		filetexte=IntegreTexte(texte)
		fileqr=IntegreQrcode(sig)
		combine=CombinaisonTexte(filetexte,filefond)
		attestation=combinaisonQrcode(fileqr,combine)
		bloc_infos = name.upper()+'@'+lastname.capitalize()+':'+description.lower()
		if len(bloc_infos) < 64 :
			i = 64 - len(bloc_infos)
			bloc_infos+=":"
			for x in range(i-1):
				bloc_infos+="."
		timestamp=Horodatage(attestation,infos)
		#timestamp="TSA/file.tsr"
		f = open(timestamp,"rb")
		timestamp = f.read()
		timestamp=binascii.b2a_base64(timestamp, newline=True)
		bloc = bloc_infos+":"+timestamp.decode('utf-8')
		mon_image = Image.open(attestation)
		cacher(mon_image, bloc)
		print ("Traitement de l'image .....  ")
		mon_image.save("final_"+attestation)
		print ("Insertion des données complétés...!")
		Mail("bonnefoi@unilim.fr","final_attestation.png", mail)
	else:
		print("Votre OTP ne correspond pas veillez reessayer")


#CalculOTP()
Saisie()

