################################################
##                                            ##
##         Created by James Camacho           ##
##                                            ##
################################################
##                  Imports                   ##
################################################

import numpy
import math
import itertools

################################################
##                 Constants                  ##
################################################

text="tiefmxoiiprn hltlcefoaiam veshsyefoet ethrprittod" ## Text to decode
alphabet="abcdefghijklmnopqrstuvwxyz"                    ## The letters in the alphabet
baconian_alphabet="abcdefghiklmnopqrstuwxyz"             ## Removes letters j, v (they become i,u)

f=open("dictionary.txt","r")
contents=f.read()
f.close()
english_words=contents.split("\n")                       ## A list of the english words


################################################
##                 Functions                  ##
################################################

def egcd(a,b):
    if a>b:
        a,b=b,a
    c,d=1,1
    while(b%a!=0):
        e=b%a
        


################################################
##            Rotational Ciphers              ##
################################################

##  AtBash Cipher - Switches A-Z, B-Y, C-X, etc.
##  Applying the cipher again will decode it.
def atbash(cipher):
    s=""
    for c in cipher:
        if c.isalpha():
            if c.islower():
                s+=alphabet[25-alphabet.index(c)]
            else:
                s+=alphabet[25-alphabet.index(c.lower())].upper()
        else:
            s+=c
    return s

def decode_atbash(cipher):
    return atbash(cipher)

##  Caesar Cipher - Rotates letters through the alphabet.
def caesar(n,cipher):
    return rot(n,cipher)
def rot(n,cipher):
    s=""
    for c in cipher:
        if c.isalpha():
            if c.islower():
                s+=alphabet[(alphabet.index(c)+n)%26]
            else:
                s+=alphabet[(alphabet.index(c.lower())+n)%26].upper()
        else:
            s+=c
    return s
def decode_caesar(cipher,english=False):
    return decode_rot(cipher,english)
def decode_rot(cipher,english):
    valid=[]
    for n in range(26):
        s=rot(n,cipher)
        if english:
            for w in s.split(" "):
                word=""
                for c in w:
                    if c.isalpha():
                        word+=c.lower()
                if not word in english_words:
                    break
            else:
                valid.append([s,n])
        else:
            valid.append([s,n])
    return valid

##  Vigenere Cipher - Similar to Caesar, but the rotation depends on the letters in a password.
def vigenere(password,cipher):
    s=""
    p=[]
    for c in password:
        if c.isalpha():
            p.append(c.lower())
    password=p
    password_length=len(password)
    i=0
    for c in cipher:
        if c.isalpha():
            k=alphabet.index(password[i%password_length])
            if c.islower():
                s+=alphabet[(alphabet.index(c)+k)%26]
            else:
                s+=alphabet[(alphabet.index(c.lower())+k)%26].upper()
            i+=1
        else:
            s+=c
    return s

##  Reverses Vigenere Cipher given a password.
def reverse_vigenere(password,cipher):
    s=""
    p=[]
    for c in password:
        if c.isalpha():
            p.append(c.lower())
    password=p
    password_length=len(password)
    i=0
    for c in cipher:
        if c.isalpha():
            k=alphabet.index(password[i%password_length])
            if c.islower():
                s+=alphabet[(alphabet.index(c)-k)%26]
            else:
                s+=alphabet[(alphabet.index(c.lower())-k)%26].upper()
            i+=1
        else:
            s+=c
    return s

##  Autokey Cipher - Similar to Vigenere, but the password used is the password joined with the ciphertext.
def autokey(password,cipher):
    return vigenere(password+cipher,cipher)
def reverse_autokey(password,cipher):
    s=""
    passcode=""+password
    password_length=len(password)
    i=0
    for c in cipher:
        if c.isalpha():
            k=alphabet.index(passcode[i])
            if c.islower():
                s+=alphabet[(alphabet.index(c)-k)%26]
                passcode+=alphabet[(alphabet.index(c)-k)%26]
            else:
                s+=alphabet[(alphabet.index(c.lower())-k)%26].upper()
                passcode+=alphabet[(alphabet.index(c.lower())-k)%26]
            i+=1
        else:
            s+=c
    return s

##  Affine Cipher - Multiplies by a constant and adds a constant to shift through the alphabet.
def affine(m,b,cipher):
    s=""
    for c in cipher:
        if c.isalpha():
            if c.islower():
                s+=alphabet[(alphabet.index(c)*m+b)%26]
            else:
                s+=alphabet[(alphabet.index(c.lower())*m+b)%26].upper()
        else:
            s+=c
    return s
def decode_affine(cipher,words=None):
    valid=[]
    for a in range(26):
        if(a%2!=0 and a%13!=0):
            for b in range(26):
                s=affine(a,b,cipher)
                if words!=None:
                    for w in s.split(" "):
                        word=""
                        for c in w:
                            if c.isalpha():
                                word+=c.lower()
                        if not word in words:
                            break
                    else:
                        valid.append([s,a,b])
                else:
                    valid.append(s)
    return valid
                

################################################
##             Rectangle Ciphers              ##
################################################

##  Rail Fence Cipher - Makes a "rail" with a certain number of rails such as:
##  "James is awesome!" is read as
##      J...s... ...s...!
##      .a.e. .s.a.e.o.e.
##      ..m...i...w...m..
##  producing Js s!ae saeoemiwm
##  In this case there are three rows.

def rail_fence(r,cipher):
    lis=[[0 for i in range(len(cipher))] for i in range(r)] ## Makes an array with r rows and large enough.
    x,y,z=0,0,1
    for c in cipher:
        lis[x][y]=c
        if x==r-1:
            z=0
        elif x==0:
            z=1
        y+=1
        if z==1:
            x+=1
        else:
            x-=1
    s=""
    for i in range(r):
        for j in range(len(lis[i])):
            if lis[i][j]!=0:
                s+=lis[i][j]
    return s

def decode_rail_fence(cipher,english=False):
    n=len(cipher)
    valid=[]
    for r in range(2,n):
        lis=[[0 for i in range(n)] for i in range(r)]
        x,y=0,0
        pos=1
        for c in cipher:
            lis[x][y]=c
            if 0<x<r-1:
                if pos==1:
                    y+=2*(r-x)-2
                else:
                    y+=2*(x+1)-2
                pos*=-1
            else:
                y+=2*r-2
            if y>=n:
                pos=1
                x+=1
                y=x
        x,y,z=0,0,1
        s=""
        for i in range(n):
            s+=lis[x][y]
            y+=1
            if x==0:
                z=1
            elif x==r-1:
                z=0
            if z==1:
                x+=1
            else:
                x-=1
        if english:
            for w in s.split(" "):
                word=""
                for c in w:
                    if c.isalpha():
                        word+=c.lower()
                if not word in english_words:
                    break
            else:
                valid.append([s,r])
        else:
            valid.append([s,r])
    return valid

##  Ice Hockey Cipher - Makes a rectangle in a similar method to the rail fence cipher.
##  "James is awesome!" is read as
##      Jeiase
##      asswo!
##      m  em
##  producing Jeiaseasswo!m  em
##  In this case there are three rows.
def ice_hockey(r,cipher):
    n=int((len(cipher)-1)/r)+1
    lis=[[0 for i in range(n)] for i in range(r)]
    x,y=0,0
    for c in cipher:
        lis[x][y]=c
        x+=1
        if x==r:
            x=0
            y+=1
    s=""
    for row in lis:
        for c in row:
            if c!=0:
                s+=c
    return s

##  Returns a list of possibilities
def decode_ice_hockey(cipher,english=False):
    valid=[]
    n=len(cipher)
    for r in range(2,n):
        list_length=int((n-1)/r)+1
        lis=[[0 for i in range(list_length)] for i in range(r)]
        x,y=0,0
        for c in cipher:
            lis[x][y]=c
            y+=1
            if y==list_length:
                y=0
                x+=1
        s=""
        x,y=0,0
        for c in range(n):
            if lis[x][y]==0:
                if(y<list_length-1):
                    continue
            else:
                s+=lis[x][y]
            x+=1
            if x==r:
                x=0
                y+=1
        if english:
            for w in s.split(" "):
                word=""
                for c in w:
                    if c.isalpha():
                        word+=c.lower()
                if not word in english_words:
                    break
            else:
                valid.append([s,r])
        else:
            valid.append([s,r])
    return valid

##  Returns the reverse of using ice_hockey.
def reverse_ice_hockey(r,cipher):
    n=len(cipher)
    list_length=int((n-1)/r)+1
    lis=[[0 for i in range(list_length)] for i in range(r)]
    x,y=0,0
    for c in cipher:
        lis[x][y]=c
        y+=1
        if y==list_length:
            y=0
            x+=1
    s=""
    x,y=0,0
    for c in range(n):
        if lis[x][y]==0:
            if(y<list_length-1):
                continue
        else:
            s+=lis[x][y]
        x+=1
        if x==r:
            x=0
            y+=1
    return s

################################################
##          Linear Algebra Ciphers            ##
################################################

##  Hill Cipher - Encodes letters in a matrix, and then multiplies them by a key (which is also converted to a matrix).
def hill(key,cipher):
    key=key.lower()
    cipher=cipher.lower()
    n=math.sqrt(len(key))
    if int(n)!=n:
        return -1
    n=int(n)
    lis=[[0 for i in range(n)] for i in range(n)]
    x,y=0,0
    for c in key:
        lis[x][y]=alphabet.index(c)
        y+=1
        if y==n:
            y=0
            x+=1
    key_array=numpy.array(lis)
    s=""
    while(cipher!=""):
        lis=[]
        for i in range(n):
            if cipher=="":
                lis.append(0)
            else:
                if cipher[0].isalpha():
                    lis.append(alphabet.index(cipher[0]))
                else:
                    i-=1
                cipher=cipher[1:]
        cipher_array=numpy.array(lis)
        arr=key_array.dot(cipher_array)%26
        for i in arr:
            s+=alphabet[i]
    return s

################################################
##             Word Unscrambler               ##
################################################

## Unscramble - Uses a dictionary to find possible word combinations.
def scramble_recursion(cipher_dict,word_list,count,max_count,words):
    if len(words)==1 and max_count>1:
        print(words)
    if count==max_count:
        for c in alphabet:
            if cipher_dict[c]!=0:
                return []
        return [words]
    valid_combos=[]
    for word in word_list:
        temp_dict={key:value for (key,value) in cipher_dict.items()}
        for c in word:
            temp_dict[c]-=1
            if temp_dict[c]<0:
                break
        else:
            ws=scramble_recursion(temp_dict,word_list,count+1,max_count,words+[word])
            for w in ws:
                w.sort()
                if not w in valid_combos:
                    valid_combos+=[w]
    return valid_combos

def unscramble(cipher,word_list,max_words=None):
    cipher_dict={c:0 for c in alphabet}
    for c in cipher:
        if c.isalpha():
            cipher_dict[c.lower()]+=1
    if max_words==None:
        valid=[]
        for i in range(1,int(len(cipher)/2)):
            valid+=scramble_recursion(cipher_dict,word_list,0,i,[])
    else:
        valid=[]
        for i in range(1,max_words+1):
            valid+=scramble_recursion(cipher_dict,word_list,0,i,[])
    return valid

def scramble_recursion2(character_list,words,word_list):
    if character_list==():
        return words
    valid_combos=[]
    for word in word_list:
        c_list=[c for c in word]
        if(len(c_list)<=len(character_list)):
            for i in range(len(c_list)):
                if c_list[i]!=character_list[i]:
                    break
            else:
                new_character_list=character_list[len(c_list):]
                new_words=words+[word]
                for combo in scramble_recursion2(new_character_list,new_words,word_list):
                    valid_combos.append(combo)
    return valid_combos

def unscramble2(cipher,word_list):
    lis=[]
    for c in cipher:
        if c.isalpha():
            lis.append(c.lower())
    perms=list(itertools.permutations(lis))
    valid_combos=[]
    for perm in perms:
        print(perm)
        combos=scramble_recursion2(perm,[],word_list)
        if combos!=[]:
            valid_combos.append(combos)
    return valid_combos

if __name__=="__main__":
    print(reverse_autokey("programjamesiscool", "Vzjke ta hog fq Rsosg Nguvguh!"))
