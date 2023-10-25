from hashlib import sha256
import hashlib
import hmac
from Crypto.Cipher import AES
import random
import hmac
import sys
from web3 import Web3
import pickle

# secreat_key=hmac.new(b'chen')
# secreat_key=hmac.new(b'chen',b'1',digestmod=sha1).digest()

# print(secreat_key.hex())
# print(len(secreat_key))
# print(secreat_key.name)
# secret_key=hashlib.sha256(b'1').digest()
# secret_key=hashlib.sha256(b'1').hexdigest()()
# print(secret_key)

# model = AES.MODE_ECB
# print(AES.block_size)
# aes=AES.new(b'0123456789012345', mode=model)
# msg=b'abcdefghigklmnop'
# cipher=aes.encrypt(msg)
# print(cipher)



# def test():
#     l=[1,2,3,4,5]
#     return l

# a=[]
# a=test()
# print(a)


# r=random.randint(-sys.maxsize-1,sys.maxsize)
# gamma_0=hmac.new(int(r).to_bytes(length=16,byteorder='big',signed='True')).digest()
# print(gamma_0)

# kw='123456'
# K_s='zhao'
# K_w=AES.new(key=K_s.zfill(16).encode('utf-8'),mode=AES.MODE_ECB).encrypt(kw.zfill(16).encode('utf-8'))
# print(K_w)


# addr=int(2).to_bytes(length=16,byteorder='big',signed=True)
# gamma_next=int(3).to_bytes(length=16,byteorder='big',signed=True)
# pos=bytes(a ^ b for a, b in zip(addr, gamma_next))
# print(pos)

# kw='123456'
# K_s='zhao'
# K_w=AES.new(key=K_s.zfill(16).encode('utf-8'),mode=AES.MODE_ECB).encrypt(kw.zfill(16).encode('utf-8'))
# IV=int(1).to_bytes(16,'big',signed=True)
# K_w2=AES.new(key=K_s.zfill(16).encode('utf-8'),mode=AES.MODE_CBC,iv=IV).encrypt(kw.zfill(16).encode('utf-8'))
# print(K_w)
# print(K_w2)

# ind='00001'
# print(int(ind[4]))
# ind_bytes=ind.zfill(16).encode('utf-8')
# print(ind_bytes[0])

# ind='00001'
# ind2='00002'
# b=ind2.encode('utf-8')
# a=ind.encode('utf-8')
# print(a+b)

# val=0
# print(len(Web3.keccak(val)))

# s='12345'
# print(s[-1:-3:-1])

# def get_string(s,pos):
#     '''
#     将所给的字符串转换为16字节长的标准字符串，并在pos表示的位置处置为'*'

#     Parameters:
#     s：待处理的字符串
#     pos：'*'的位置，一个负数（表示从后往前数）

#     Results:
#     s_new：处理后的字符串
#     '''
#     s_new=s.zfiil(16)
#     s_new[pos]='*'
#     return s_new


# print(get_string('11',-11))

# s='abc'
# s1=list(s)
# s1[0]='A'
# s=''.join(s1)
# print (s)

# l1=[1,2,3]
# l2=[4]
# l1.extend(l2)
# print(l1)
# l2=[5]
# print(l1)

# a=bin(5)
# print(a)
# print(type(a))
# a=10
# print(a)
# a=[123,456]
# print(a)
# a='123'
# print(a)

# a='0101'
# b=a
# a='00'
# print(b)
# a='00'
# b='00'
# l=[a,b]
# print(l)
# l.extend('123')
# print(l)


# a=[]
# a.append(['a',1])
# a.append(['b',2])
# print(a)
# x,y=a[1]
# print(x)
# print(y)
# for i in a:
#     print(i)

# a='123'.encode('utf-8')
# b='456'.encode('utf-8')
# l=[a,b]
# print(l)
# l2=['789']
# l2=[l2,l]
# print(l2)
# l=[]
# l.append([a,b])
# print(l)

# a=int(1).to_bytes(16,'big',signed=True)
# b=int(1).to_bytes(16,'big',signed=True)
# print(a==b)

# import json

# file = open('data_10.txt', 'r') 
# js = file.read()
# dic = json.loads(js)   
# print(dic) 
# file.close() 


# dic={
#     '0':['1','2','3'],
#     '1':['1','2','3'],
#     '2':['2','3'],
#     '3':['0','4'],
#     '6':['4','1'],
#     '9':['6','0','2']
# }
# with open ("data_10.txt", 'wb') as f: #打开文件
#     pickle.dump(dic, f)

# with open ("data_10.txt", 'rb') as f: #打开文件
#     dic = pickle.load(f)

# print(dic)

# a=b'1234'
# b=a.zfill(16)
# print(b)

# print(int('011'))

# def func():
#     if True:
#         h=2
#     print(h)
#     return


# func()

# print(str(10))


def f():
    i=1

i=10
f()
print(i)