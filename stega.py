# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 13:39:56 2015

@author: cyril
"""
from __future__ import print_function
from decimal import *
import fpformat


def prcnt(a,b,f):
	a=str(Decimal(((a//((b)*10**-64))+1)*10**-64)*10**2)
	return fpformat.fix(a, f)

def f(x):
    tmp=hashlib.new("md5")
    tmp.update(x)
    return tmp.hexdigest()

def f2(x):
    return x

def f3(x):
    return ""

import mmap
def MEM_F_FIND(fichier,cherche,size_block=1,padding_read=0):
	dta=""
	with open(fichier, "r+b") as f:
		mm = mmap.mmap(f.fileno(), 0)
		r=mm.find(cherche)
	if r!=-1:
		mm.seek(r+padding_read)
		dta = mm.read(size_block)
	
	mm.close()
 	mm=""
	return r,dta

def MEM_F_FIND_n_READ(fichier,cherche,size_block=1,padding_read=0,mode=0):
	dta=""
	e=0
	if mode==0: e=len(cherche)
	with open(fichier, "r+b") as f:
		mm = mmap.mmap(f.fileno(), 0)
		r=mm.find(cherche)
	if r!=-1:
		mm.seek(r+e+padding_read)
		tmp=" "
		while tmp!="":
			tmp = mm.read(size_block)
			dta=dta+tmp	
	mm.close()
 	mm=""
	return r,dta

"""

Début du code principal
 
"""     
import hashlib
import os
from multiprocessing import Pool
import time
import argparse
from operator import *
import random
import getpass

parser = argparse.ArgumentParser(description='Prototype de compression no-limit.')
parser.add_argument('string0', metavar='Fa', type=str,
                   help="Nom du fichier source.")
parser.add_argument('string1', metavar='Fb', type=str,
                   help="Nom du fichier cible.")
parser.add_argument('chiffre', metavar='C', type=str,
                   help="Cryptage (NO/XOR) (NO-PAS DE CRYPTAGE, XOR-OU EXCLUSIF SIMPLE PASSE)")
parser.add_argument('mode', metavar='V', type=str,
                   help="Mode (in/out)")

args = parser.parse_args()
fichier_a=args.string0
fichier_b=args.string1
chiffre= args.chiffre
mode=args.mode
from Crypto.Cipher import AES

r,dta=-1,""

if mode == "in":
		
	if chiffre =="XOR":
		if os.path.exists(fichier_a):
			password=getpass.getpass()
			h_passw=hashlib.new("sha512")
			h_passw.update(password)
			password=""
			random.seed(int(float.fromhex(h_passw.hexdigest())))
			fa=open(fichier_a,"r")
			fb=open(fichier_b,"append")
			tmp= " "			
			fb.write("S-T-E-G-A-"+h_passw.hexdigest())
			while tmp!="":
				tmp=fa.read(1)
				if len(tmp)>0: fb.write(chr(xor(ord(tmp),random.randint(0,255))))
			fa.close()
			fb.close()


	if chiffre == "NO":
		if os.path.exists(fichier_a):
			fa=open(fichier_a,"r")
			fb=open(fichier_b,"append")
			tmp= " "
			fb.write("S-T-E-G-A-")
			while tmp!="":
				tmp=fa.read(1)
				fb.write(tmp)
			fa.close()
			fb.close()
if mode == "out":


	if chiffre =="XOR":
		if os.path.exists(fichier_a):
			password=getpass.getpass()
			h_passw=hashlib.new("sha512")
			h_passw.update(password)
			password=""
			random.seed(int(float.fromhex(h_passw.hexdigest())))


			r,dta=MEM_F_FIND_n_READ(fichier_a,"S-T-E-G-A-"+h_passw.hexdigest())
			if r!=-1:
				print ("mot de passe OK.")
				random.seed(int(float.fromhex(h_passw.hexdigest())))
				#fa=open(fichier_a,"r")
				fb=open(fichier_b,"append")
				e,n=len(dta),1
				while n<e+1:
					tmp=dta[:n][-1:]
					if len(tmp)>0: fb.write(chr(xor(ord(tmp),random.randint(0,255))))
					n=n+1
				#fa.close()
				fb.close()
			else:
				print ("mot de passe incorrect!")


	if chiffre == "NO":
		if os.path.exists(fichier_a):		
			r,dta=MEM_F_FIND_n_READ(fichier_a,"S-T-E-G-A-")
			
			if r!=-1:
				fb=open(fichier_b,"append")
				fb.write(dta)
				fb.close()





