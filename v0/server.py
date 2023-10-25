from ctypes import c_byte, wstring_at
from web3 import Web3
import random
import sys
import hmac
from Crypto.Cipher import AES
import copy

def search_server(ST,map_server):
    '''
    server端根据搜索令牌查找得到密文

    Parameters:
    ST：搜索令牌，一个list，包含若干个[K_w,gamma_0]
    map_server：server端的储存容器，将addr映射到[P,V]

    Returns:
    results：一个list，储存搜索得到的密文

    '''
    results=[]
    
    # 遍历ST中所有的[K_w,gamma_0]
    for i in ST:
        # 得到K_w,gamma_0
        K_w=i[0]
        gamma_0=i[1]

        # 创建一个AES对象，密钥是K_w，即算法中的PRF G
        PRF_G=AES.new(key=K_w,mode=AES.MODE_ECB)

        # 计算首地址addr_0
        addr_0=PRF_G.encrypt(gamma_0)

        # 遍历找到链上所有的密文 
        addr=addr_0
        while addr in map_server:
            # 找到pos和val
            pos,val=map_server[addr]

            # 将密文val加入结果
            results.append(val)

            # 计算下一个位置的gamma
            gamma_next=bytes(a^b for a,b in zip(pos,addr))
            
            # 计算下一个位置addr
            addr=PRF_G.encrypt(gamma_next)
    return results




