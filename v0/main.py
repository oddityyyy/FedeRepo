# -*- coding: UTF-8 -*-
import client
import server
import blockchain
import json
import pickle
import hmac
from web3 import Web3
import random
import sys


def test_scheme_honest(lb, ub, state_client, K_s, K_e, map_server, eth_contract, from_account):
    '''
    对方案进行测试，输出测试结果。这里server会诚实的进行搜索并返回结果

    Parameters:
    lb:范围的上界，如'13'
    ub:范围的下界，如'0'
    state_client：client的状态表
    K_s:
    K_e:
    map_server:
    eth_contract:合约对象
    from_account:server/client的账户



    Returns:
    none
    '''
    # client计算令牌ST
    ST, d, WSet = client.token_client(
        lb=lb,
        ub=ub,
        state_client=state_client,
        K_s=K_s
    )

    # server使用令牌进行搜索
    results = server.search_server(
        ST,
        map_server=map_server
    )

    # client对结果进行第一轮的验证
    flag_client = client.verify_client(
        results, d
    )

    print('client think it is ', flag_client)

    # 判断是否通过第一轮验证
    # 若未通过第一轮验证，需要命令区块链进行judge
    if not flag_client:
        # 计算l_w_list
        l_w_list = client.get_lw_list(
            state_client=state_client,
            WSet=WSet,
            K_s=K_s
        )

        # 验证
        flag_blockchain,gas = blockchain.verify(
            results=results,
            eth_contract=eth_contract,
            from_account=from_account,
            l_w_list=l_w_list
        )

        print('blockchain judge: the result is ', flag_blockchain)

        if flag_blockchain:
            print(client.decrypt_client(results=results, K_e=K_e))
    

    # 第一轮验证即通过，解密
    else:
        print(client.decrypt_client(results=results, K_e=K_e))
    
    return client.decrypt_client(results=results, K_e=K_e)









def test_scheme_cheat(lb, ub, state_client, K_s, K_e, map_server, eth_contract, from_account):
    '''
    对方案进行测试，输出测试结果。这里server是不诚实的，会随机生成若干个结果返回

    Parameters:
    lb:范围的上界，如'13'
    ub:范围的下界，如'0'
    state_client：client的状态表
    K_s:
    K_e:
    map_server:
    eth_contract:合约对象
    from_account:server/client的账户

    Returns:
    none
    '''
    # client计算令牌ST
    ST, d, WSet = client.token_client(
        lb=lb,
        ub=ub,
        state_client=state_client,
        K_s=K_s
    )


    # server随机生成若干个结果
    results = []
    for i in range(0,5):
        r=random.randint(-sys.maxsize-1,sys.maxsize)
        r=int(r).to_bytes(32,'big',signed=True)
        results.append(r)



    # client对结果进行第一轮的验证
    flag_client = client.verify_client(
        results, d
    )

    print('client think it is ', flag_client)

    # 判断是否通过第一轮验证
    # 若未通过第一轮验证，需要命令区块链进行judge
    if not flag_client:
        # 计算l_w_list
        l_w_list = client.get_lw_list(
            state_client=state_client,
            WSet=WSet,
            K_s=K_s
        )

        # 验证
        flag_blockchain,gas = blockchain.verify(
            results=results,
            eth_contract=eth_contract,
            from_account=from_account,
            l_w_list=l_w_list
        )

        print('blockchain judge: the result is ', flag_blockchain)

        # 解密
        if flag_blockchain:
            print(client.decrypt_client(results=results, K_e=K_e))
    
    # 第一轮验证即通过，解密
    else:
        print(client.decrypt_client(results=results, K_e=K_e))




def test_scheme_deny(lb, ub, state_client, K_s, K_e, map_server, eth_contract, from_account):
    '''
    对方案进行测试，输出测试结果。这里client是不诚实的，会拒绝接受server的结果

    Parameters:
    lb:范围的上界，如'13'
    ub:范围的下界，如'0'
    state_client：client的状态表
    K_s:
    K_e:
    map_server:
    eth_contract:合约对象
    from_account:server/client的账户

    Returns:
    none
    '''
    # client计算令牌ST
    ST, d, WSet = client.token_client(
        lb=lb,
        ub=ub,
        state_client=state_client,
        K_s=K_s
    )

    # server使用令牌进行搜索
    results = server.search_server(
        ST,
        map_server=map_server
    )

    # client对结果进行第一轮的验证后仍然拒绝接受
    flag_client = client.verify_client(
        results, d
    )
    flag_client=False

    print('client think it is ', flag_client)

    # 判断是否通过第一轮验证
    # 若未通过第一轮验证，需要命令区块链进行judge
    if not flag_client:
        # 计算l_w_list
        l_w_list = client.get_lw_list(
            state_client=state_client,
            WSet=WSet,
            K_s=K_s
        )

        # 验证
        flag_blockchain,gas = blockchain.verify(
            results=results,
            eth_contract=eth_contract,
            from_account=from_account,
            l_w_list=l_w_list
        )

        print('blockchain judge: the result is ', flag_blockchain)

        if flag_blockchain:
            print(client.decrypt_client(results=results, K_e=K_e))
    

    # 第一轮验证即通过，解密
    else:
        print(client.decrypt_client(results=results, K_e=K_e))










############################################ 以太坊账户、合约定义 ####################################
# 从当前目录下的abi.json文件读取abi
with open('./abi.json', 'r', encoding='utf8')as fp:
    contract_abi = json.load(fp)
# print(contract_abi)

# 创建一个Web3对象
w3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8545"))

# client/server的账户from_account
from_account = w3.toChecksumAddress(input('输入server/client的eth账户:'))

# 创建合约对象eth_contract
eth_contract = w3.eth.contract(
    address=w3.toChecksumAddress(input('输入合约账户:')),
    abi=contract_abi
)

str=input("请输入地址：")

def save(str):
    tx_hash = eth_contract.functions.set(str).transact({
        "from": from_account,
        "maxFeePerGas": 1000000001,
        "baseFeePerGas":1000000000,
        "maxPriorityFeePerGas":20000000
        
    })
    print("上传成功！")

def getpath():
    new_str=eth_contract.functions.get().call()
    print(new_str)
    return new_str


save(str)
getpath()




