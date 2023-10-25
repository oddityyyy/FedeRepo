# -*- coding: UTF-8 -*-
from ctypes import c_byte, wstring_at
from web3 import Web3
import random
import sys
import hmac
from Crypto.Cipher import AES
import copy


def get_string(s, pos):
    '''
    将所给的字符串转换为16字节长的标准字符串，并在pos表示的位置处置为'*'

    Parameters:
    s：待处理的字符串
    pos：'*'的位置，一个负数（表示从后往前数）

    Results:
    s_new：处理后的字符串
    '''
    s_new = list(s.zfill(16))
    s_new[pos] = '*'
    # 将list转换为str
    return ''.join(s_new)


def rshift(s):
    '''
    将字符串逻辑右移一位（一个字节）

    示例：'00100'右移一位得到'00010'

    Parameters:
    s:字符串

    Results:
    s_new：处理后的字符串
    '''
    s_new = '0'+s[0:len(s)-1]
    return s_new


def merge(l1, l2):
    '''
    将两个列表的内容进行合并

    示例：['12','34']与['56','78']合并得到['12','34','56','78']

    Parameters:
    l1,l2：两个列表，其中的元素是str对象或者bytes对象

    Returns:
    l：合并后的列表    
    '''
    l = copy.deepcopy(l1)
    for i in l2:
        l.append(i)
    return l


def construct_inverted_index(inverted_index):
    '''
    将普通的反转索引转换为PTKS上叶结点以及其所有祖先结点的反转索引

    示例：inverted_index中包含w='1',ind=[id1]，那么输出的结果中包含['00000*0000000001',id1],['0000000*000000000',id1]...
    若还包含w='0',ind=[id2]，那么输出的结果中包含的是['00000*0000000000',id2],['00000*0000000001',ind1],
    和['000000*000000000',[id1,ind2]]
    若w='3'，那么会将其转换为'00000*0000000011'

    Parameters:
    inverted_index：一个字典容器，储存w->[ind]，这里w是普通的字符串，如'5'，'8'；ind为一个列表

    Returns:
    kw_files_list：一个字典容器，储存w->[ind]，这里w是16字节长的标准字符串，其中包含'*'
    '''
    kw_files_list = {}

    for w in inverted_index:
        # 先将w转换为01串：计算其数值再转换为01串
        s=bin(int(w)).replace('0b','')

        # 对从叶结点到root的路径上所有的结点进行操作：计算其标准字符串和反转索引
        # 计算叶结点对应的标准字符串
        pos = -11
        s = get_string(s, pos)
        # 对所有结点进行操作
        for i in range(-pos):
            # 将叶结点对应的索引列表并入当前结点的索引列表
            # 使用深拷贝，防止引用复制带来问题
            if (s in kw_files_list):
                # kw_files_list[s].append(copy.deepcopy(inverted_index[w]))
                kw_files_list[s] = merge(kw_files_list[s], inverted_index[w])
            else:
                kw_files_list[s] = copy.deepcopy(inverted_index[w])
            # 字符串右移一字节得到向上一个结点对应的标准字符串
            s = rshift(s)

    return kw_files_list


def get_dec_from_bin(s):
    '''
    根据给定的标准字符串，计算该标准字符串的十进制值

    示例：给定'00000*0000000110'，其十进制为6

    Parameters:
    s:标准字符串

    Results:
    子串的值
    '''
    return int(s.replace('*', '0'), 2)


def get_BRC(lower_bound, upper_bound):
    '''
    根据所给范围计算BRC

    Parameters:
    lower_bound:范围的下界，一个代表数字的字符串，属于[0,1023]，如'123'
    upper_bound:范围的上界，一个代表数字的字符串，属于[0,1023]，如'456
    下界必须小于等于上界

    Results:
    WSet：一个list容器，包含BRC中的所有w，w为标准字符串形式
    '''
    WSet = []

    # 先将上界和下界转换为int型的数据
    lb=int(lower_bound)
    ub=int(upper_bound)


    # 再将上界和下界转换为01串，普通字符串形式
    # 如将5转换为'101'，字符串的一个字节代表二进制的一位
    lb = bin(lb).replace('0b', '')
    ub = bin(ub).replace('0b', '')

    # 将上下界的普通字符串转换为标准字符串
    height = 11       # 二叉树的高度
    lb = get_string(lb, -height)
    ub = get_string(ub, -height)

    # 求解BRC
    i = 0
    # 比较a_0...a_(m-i)和b_0...b_(m-i)的值。通过逻辑右移的方式获取前缀（非叶节点的值）
    while get_dec_from_bin(lb) < get_dec_from_bin(ub):
        # 根据当前前缀的最后一位判断是否将其加入BRC
        if lb[-1] == '1':
            WSet.append(lb)
        if ub[-1] == '0':
            WSet.append(ub)

        # 两个前缀分别加0x1和减0x1
        lb = bin(get_dec_from_bin(lb)+1).replace('0b', '')
        lb = get_string(lb, -height+i)
        ub = bin(get_dec_from_bin(ub)-1).replace('0b', '')
        ub = get_string(ub, -height+i)

        # 对应于算法中的i++，这里使用逻辑右移实现
        lb = rshift(lb)
        ub = rshift(ub)
        i = i+1
    # 判断a_0...a_(m-i)和b_0...b_(m-i)是否相等
    if lb == ub:
        WSet.append(lb)

    return WSet


def build_client(K_e, K_s, inverted_index):
    '''
    client端的Build操作

    Parameters:
    K_e：用于对称加密
    K_s：PRF的密钥
    inverted_index：一个字典，储存若干个关键词kw的倒排索引，kw是普通字符串，其中ind为一个列表

    Returns:
    state_client：client端的状态表，一个字典容器，储存kw->[c,v,gamma_0,h]
    map_server：server端的储存容器，将addr映射到[P,V]
    checklist:一个字典，储存lw->h    
    '''
    state_client = {}
    map_server = {}
    checklist = {}


    # 将普通的反转索引inverted_index转换为标准形式的kw_files_list
    # kw_files_list为PTKS上叶结点以及其所有祖先结点的反转索引，且关键词为标准字符串形式
    kw_files_list=construct_inverted_index(inverted_index)



    # 遍历所有关键词kw
    for kw in kw_files_list:
        # 初始化状态
        c = 0
        v = 0
        h = int(0).to_bytes(32, 'big', signed=True)

        # 随机选择一个gamma_0。先生成一个随机数，然后求这个随机数的哈希
        r = random.randint(-sys.maxsize-1, sys.maxsize)
        gamma_0 = hmac.new(int(r).to_bytes(
            length=16, byteorder='big', signed='True')).digest()

        # 计算w的密钥K_w
        # key为16字节，将kw填充为16字节长
        K_w = AES.new(key=K_s.zfill(16),
                      mode=AES.MODE_ECB).encrypt(kw.zfill(16).encode('utf-8'))

        # 生成一个AES对象，密钥是K_w，即PRF G
        PRF_G = AES.new(key=K_w, mode=AES.MODE_ECB)
        # 生成一个AES对象，密钥是K_e，即用于加密的Enc算法。
        Enc = AES.new(key=K_e, mode=AES.MODE_ECB)

        # 遍历该w对应的所有文件id
        # 当前的gamma
        gamma_now = gamma_0
        for ind in kw_files_list[kw]:

            # 生成新的gamma_next
            r = random.randint(-sys.maxsize-1, sys.maxsize)
            gamma_next = hmac.new(int(r).to_bytes(
                length=16, byteorder='big', signed='True')).digest()

            # 生成当前地址
            addr = PRF_G.encrypt(gamma_now)

            # 密文的第一部分 addr xor gamma_next
            pos = bytes(a ^ b for a, b in zip(addr, gamma_next))

            # 密文的第二部分 Enc(K_w,ind||c)
            ind_bytes = ind.zfill(16).encode('utf-8')
            c_bytes = int(c).to_bytes(16, 'big', signed='True')
            val = Enc.encrypt(ind_bytes)+Enc.encrypt(c_bytes)  # 32字节的密文

            # I.put(addr,(P,V))
            map_server[addr] = [pos, val]

            # 计算哈希值，要用solidity的keccak哈希函数
            h = bytes(a ^ b for a, b in zip(h, Web3.keccak(val)))
            c = c+1

            # 更新gamma_now
            gamma_now=gamma_next

        # 计算l_w，更新checklist
        # H(Kw||v)
        l_w = hmac.new(K_w+int(v).to_bytes(16, 'big', signed=True)).digest()
        # 更新checklist
        checklist[l_w] = h

        # 更新状态表
        state_client[kw] = [c, v, gamma_0, h]

    # 返回三个字典容器
    return state_client, map_server, checklist


def token_client(lb, ub, state_client, K_s):
    '''
    client端的search操作，计算BRC，生成所需的搜索令牌ST

    Parameters:
    lb:lower bound，范围的下界
    ub:upper bound，范围的上界
    state_client：client的状态表
    K_s：密钥

    Returns:
    ST：搜索令牌，一个list，包含若干个[K_w,gamma_0]
    d：client端储存的digest的异或值
    WSet：BRC集合
    '''
    d = int(0).to_bytes(32, 'big', signed=True)
    ST = []

    # 计算BRC得到WSet
    WSet = get_BRC(lb, ub)

    # 根据WSet计算搜索令牌ST
    for kw in WSet:
        c, v, gamma_0, h = state_client[kw]
        d = bytes(a ^ b for a, b in zip(d, h))
        K_w = AES.new(key=K_s,
                      mode=AES.MODE_ECB).encrypt(kw.encode('utf-8'))
        ST.append([K_w, gamma_0])

    return ST, d,WSet










def update_client(K_e, K_s, new_kw_files, state_client, map_server):
    '''
    client端的更新操作

    Parameters:
    K_e：用于对称加密的密钥
    K_s：PRF的密钥
    new_kw_files：字典容器，储存新加入的w-ind pair，为普通的倒排索引，其中ind为一个列表
    state_client：client端的状态表，一个字典容器，储存kw->[c,v,gamma_0,h]
    map_server：server端的储存容器，将addr映射到[P,V]

    Returns:
    checklist：包含新加入的元素对应的l_w和digest
    '''
    checklist = {}


    # 将普通的倒排索引转换为PTKS上叶结点以及其所有祖先结点的反转索引
    new_kw_files=construct_inverted_index(new_kw_files)


    # 对倒排索引new_kw_files中每个w-id pair，将其加入server
    for kw in new_kw_files:

        # 查找状态表得到w对应的状态信息
        # 先判断状态表中是否存在当前的w。若该w是第一次加入，需要初始化状态信息
        if kw in state_client:
            c, v, gamma_0, h = state_client[kw]
            v = v+1
        else:
            c = 0
            v = 0
            h = int(0).to_bytes(32, 'big', signed=True)
            # 随机生成一个gamma_0
            r = random.randint(-sys.maxsize-1, sys.maxsize)
            gamma_0 = hmac.new(int(r).to_bytes(
                length=16, byteorder='big', signed='True')).digest()

        # 计算K_w
        K_w = AES.new(key=K_s.zfill(16),
                      mode=AES.MODE_ECB).encrypt(kw.zfill(16).encode('utf-8'))


        # 对w对应的所有ind，将其加入map_server
        for ind in new_kw_files[kw]:
            # 生成新的gamma
            r = random.randint(-sys.maxsize-1, sys.maxsize)
            gamma_now = hmac.new(int(r).to_bytes(
                length=16, byteorder='big', signed='True')).digest()

            # 计算当前ind的地址addr=G(K_w,gamma_now)
            addr = AES.new(key=K_w, mode=AES.MODE_ECB).encrypt(gamma_now)

            # 计算pos=addr xor gamma_0
            pos = bytes(a ^ b for a, b in zip(addr, gamma_0))

            # 计算val=Enc(K_e,id||c)
            id_bytes = ind.zfill(16).encode('utf-8')
            c_bytes = int(c).to_bytes(16, 'big', signed=True)
            val = AES.new(key=K_e, mode=AES.MODE_ECB).encrypt(id_bytes+c_bytes)

            # 更新server的储存
            map_server[addr] = [pos, val]

            # 更新digest值=h xor H(val)，使用solidity的keccak哈希函数来计算
            h = bytes(a ^ b for a, b in zip(Web3.keccak(val), h))

            # 更新c
            c = c+1

            # 更新gamma_0
            gamma_0=gamma_now


        # 计算l_w
        l_w = hmac.new(K_w+int(v).to_bytes(16, 'big', signed=True)).digest()

        # 更新checklist
        checklist[l_w] = h

        # 更新状态表
        state_client[kw] = [c, v, gamma_0, h]

    return checklist











def verify_client(results, d):
    '''
    client端进行第一轮验证

    Parameters:
    results：一个list容器，储存server搜索得到的密文
    d：client端储存的标准结果


    Returns:
    iscorrect：结果是否通过第一轮验证


    '''
    iscorrect = False

    # 计算results中所有val的digest
    # 初始化digest值
    v = int(0).to_bytes(32, 'big', signed=True)
    for val in results:
        # v=v xor H(val)
        v = bytes(a ^ b for a, b in zip(v, Web3.keccak(val)))
    
    # 判断v==d?
    if v==d:
        iscorrect=True
    else:
        iscorrect=False

    return iscorrect





def get_lw_list(state_client,WSet,K_s):
    '''
    计算验证时提供给区块链的l_w_list

    Parameters:
    state_client:client端的状态表
    WSet：BRC集合
    K_s：密钥

    Returns:
    l_w_list：一个list容器，储存WSet中关键词对应的checklist的l_w
    '''

    l_w_list=[]

    # PRF_F，密钥为K_s，用于计算K_w
    PRF_F=AES.new(
        key=K_s,
        mode=AES.MODE_ECB
    )
    
    for kw in WSet:
        # 找到 w 的v值
        v=state_client[kw][1]

        # 计算K_w=F(K_s,w)
        K_w=PRF_F.encrypt(kw.encode('utf-8'))

        # 计算l_w=H(K_w||v)
        l_w=hmac.new(K_w+int(v).to_bytes(16,'big',signed=True)).digest()

        # 更新结果
        l_w_list.append(l_w)
    
    return l_w_list







def decrypt_client(results,K_e):
    '''
    
    '''

    result_set=set()

    Enc=AES.new(key=K_e,mode=AES.MODE_ECB)
    for ct in results:
        # 解密得到 id||c
        msg=Enc.decrypt(ct)

        # 得到id
        ind=msg[0:16]

        # 将其转换为整数在转换为字符串
        ind=int(ind)
        ind=str(ind)

        # 加入结果集
        result_set.add(ind)

    return result_set






if __name__ == "__main__":
    a = ['12', '34']
    b = ['56', '78']
    print(merge(a, b))

    # print(get_BRC(2, 7))
    # print(get_BRC(2, 2))
    # print(get_BRC(1, 1))
    # print(get_BRC(4, 6))

    # print(get_dec_from_bin('00000*0000000011'))
    # dict1={
    #     '010':['id1'],
    #     '00':['id2']

    # }
    # dic2=construct_inverted_index(dict1)
    # print(dic2)
