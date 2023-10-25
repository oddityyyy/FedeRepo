# 从二进制文件中读取build用的字典数据 inverted_index
with open("data_10.txt", 'rb') as f:  # 打开文件
    inverted_index = pickle.load(f)


# 生成K_e,K_s，使用hmac来生成
K_e = hmac.new(b'hong').digest()
K_s = hmac.new(b'guang').digest()
print('K_e=', K_e.hex())
print('K_s=', K_s.hex())















####################################### Build阶段 ###############################################

# 调用build_client函数，进行build
state_client,map_server,checklist=client.build_client(
                    K_e=K_e, 
                    K_s=K_s, 
                    inverted_index=inverted_index
)


# 输出三个字典容器
# print(state_client)
# print(map_server)
# print(checklist)



# 调用智能合约，将checklist发送至区块链
# 对checklist中每个l_w->digest pair，调用一次智能合约将其写入区块链
for l_w in checklist:
    tx_hash=eth_contract.functions.set(l_w,checklist[l_w]).transact({
        "from":from_account,
        "gas":3000000,
        "gasPrice":1
    })








########################################### 加入新的 w-ind pair #############################################

# 新加入的元素
new_kw_files={'0':['0'],'1':['7'],'4':['2']}

# 将新元素加入
checklist=client.update_client(
    K_e=K_e,
    K_s=K_s,
    new_kw_files=new_kw_files,
    state_client=state_client,
    map_server=map_server
)

# 将新的checklist发送至区块链
for l_w in checklist:
    tx_hash=eth_contract.functions.set(l_w,checklist[l_w]).transact({
        "from":from_account,
        "gas":3000000,
        "gasPrice":1
    })








############################################### 进行范围搜索 #################################################

# 定义下界和上界
lb='0'
ub='4'

# client计算令牌ST
d,ST=client.token_client(
    lb=lb,
    ub=ub,
    state_client=state_client,
    K_s=K_s
)

# server使用令牌进行搜索
results=server.search_server(
    ST,
    map_server=map_server
)


# client对结果进行第一轮的验证
flag=client.verify_client(
    results,d
)
print(flag)