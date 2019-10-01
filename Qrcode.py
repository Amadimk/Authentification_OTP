import pyqrcode
import sys
from PIL import Image
import time
import binascii
#import qrtools
import subprocess
from pyzbar.pyzbar import decode
from PIL import Image

def IntegreQrcode(sign):
	f = open(sign,'rb')
	lines = f.read()
	ascii=binascii.b2a_base64(lines, newline=True)
	qr = pyqrcode.create(ascii.decode('ascii'))
	qr.png("qrcode.png", scale=2)
	print("Generation du Qrcode... done : qrcode.png")
	return "qrcode.png"


def combinaisonQrcode(file1, file2):
	subprocess.run('composite -geometry +1418+934 '+file1+' '+file2+' attestation.png',shell=True)
	print('Combinaison des fichiers : '+file1+' et ' +file2)
	return  'attestation.png'
def extraire(file):
	datas = decode(Image.open(file))
	data = datas[0].data.decode('ascii')
	data =binascii.a2b_base64(data)
	f = open("test.sign","wb")
	f.write(data)
	f.close()
	print("Extraction de la signature dans le Qrcode ...!!!")
	time.sleep(1)
	return f.name

#qrcode=IntegreQrcode("sign.out")
#extraire(qrcode)
