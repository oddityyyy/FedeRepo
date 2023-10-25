import hmac
from web3 import Web3


def verify(results,eth_contract,from_account,l_w_list):
    '''
    调用智能合约函数，完成第二轮验证

    Parameters:
    results:server返回的密文
    eth_contract:智能合约对象
    from_account:server/client的地址
    l_w_list：一个list容器，储存BRC集合对应的l_w


    Returns:
    is_correct：区块链judge的结果。若密文正确返回True
    gas: 验证中花费的gas
    '''

    gas=0
    # 创建一个Web3对象
    w3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8545"))

    # 先对搜索结果进行分组，每组100个密文
    # 示例：若results有321个，那么batch_num1=3，batch_last=21
    batch_size=100
    # batch_num1是包含100个密文的分组的数量
    batch_num1=int(len(results)/batch_size)
    # batch_last是不足100个密文的分组中的密文数
    batch_last=int(len(results)%batch_size)

    # 调用智能合约计算每个分组的digest
    for i in range(0,len(results),batch_size):

        # 是最后一个分组
        if len(results)-i < batch_size:
            # 最后一个分组的内容
            partition=results[i:i+batch_last]

            # 调用智能合约计算这个分组的digest
            tx_hash=eth_contract.functions.batch_cal_hash(partition,len(results)-i,int(i/batch_size)).transact({
                "from":from_account,
                "gas":3000000,
                "gasPrice":1
            })

        # 不是最后一个分组，分组中的密文数量是满的
        else:
            # 分组的内容
            partition=results[i:i+batch_size]

            # 调用智能合约计算这个分组的digest
            tx_hash=eth_contract.functions.batch_cal_hash(partition,batch_size,int(i/batch_size)).transact({
                "from":from_account,
                "gas":3000000,
                "gasPrice":1
            })
        
        # 根据交易的哈希值查找花费的gas
        rp=w3.eth.getTransactionReceipt(tx_hash)
        gas=gas+rp['gasUsed']



    # 调用智能合约，将前面所有分组的digest组合起来计算最终的digest
    # 计算总的分组数量
    total_num=0
    if batch_last==0:
        total_num=batch_num1
    else:
        total_num=batch_num1+1

    eth_contract.functions.cal_digest(total_num).transact({
                "from":from_account,
                "gas":3000000,
                "gasPrice":1
    })
    # 根据交易的哈希值查找花费的gas
    rp=w3.eth.getTransactionReceipt(tx_hash)
    gas=gas+rp['gasUsed']


    # 进行judge
    eth_contract.functions.judge(l_w_list,len(l_w_list)).transact({
                "from":from_account,
                "gas":3000000,
                "gasPrice":1
    })
    # 根据交易的哈希值查找花费的gas
    rp=w3.eth.getTransactionReceipt(tx_hash)
    gas=gas+rp['gasUsed']


    # 读取judge的结果
    return eth_contract.functions.get_is_equal().call(),gas
