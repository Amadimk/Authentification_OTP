import subprocess,time

def signature(infos):
	f=open(infos[0]+'.fiche','w')
	f.write(infos[0]+'\n')
	f.write(infos[1]+'\n')
	f.write(infos[2])
	f.close()
	privatekeypath = "AC/appli.key.pem"
	subprocess.run('openssl dgst -sha256 -sign '+privatekeypath+' -out AC/signed.'+infos[0]+'.sig ' + infos[0]+'.fiche', shell=True) 
	print('Signature ...Done : AC/signed.'+infos[0]+'.sig')
	return 'AC/signed.'+infos[0]+'.sig'
def verifySign(infos, signer):
	print("Lancement de la procedure de verification de la signature ...")
	f=open(infos[0]+'.verif','w')
	f.write(infos[0]+'\n')
	f.write(infos[1]+'\n')
	f.write(infos[2])
	f.close()
	subprocess.run('openssl x509 -pubkey -noout -in AC/certiplus.crt > AC/appli.publickey.pem', shell=True)
	time.sleep(2)
	p=subprocess.Popen('openssl dgst -sha256 -verify AC/appli.publickey.pem -signature '+signer+' '+infos[0]+'.verif',stdout=subprocess.PIPE, shell=True)
	(response,error) = p.communicate()
	if "OK" in response.decode('utf-8'):
		print("La verification de la signature à reussie avec succèes !!!")
		return True
	else:
		print("Echec verification de la signature")
		return False
#infos=['DIALLO','Amadou','Attestation de Reussite']
