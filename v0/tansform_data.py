import pickle
import json
import random
def transform_data():
    '''
    读取'./dataset_10K'目录下所有的文件，这些文件名为关键字的值，文件内容为倒排索引

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_10K.txt'

    示例：如文件1包含数据23,34；文件2包含数据56,78。那么得到一个普通的倒排索引{'1':['23','34'],'2':['56','78']}

    Parameters:
    none

    Returns:
    none
    '''

    # 普通的倒排索引
    inverted_index={}

    # 循环1000次读取文件
    for i in range(1,1001):
        # 计算文件名
        filename='./dataset_10K/'+str(i)

        # 打开该文件
        with open(filename,'r',encoding='utf-8') as f:
            # 读取所有数据
            s=f.read()
        
        # 按照','将数字分开得到一个list
        l=s.split(',')

        # 加入倒排索引
        inverted_index[str(i)]=l

    # 将倒排索引写入到二进制文件中
    with open ("data_10K.txt", 'wb') as f: #打开文件
        pickle.dump(inverted_index, f)


def get_2K():
    '''
    生成2K数据集。共1K个关键字，每个关键字对应2个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_2K.txt'，且储存在"./data_2K.json"
    '''

    d={}
    for i in range(1,1001):
        # 随机生成两个整数
        a=str(random.randint(0,2000))
        b=str(random.randint(0,2000))
        d[str(i)]=[a,b]
    
    with open ("data_2K.txt", 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open("./data_2K.json", 'w') as json_file:
        json_file.write(json_str)



def get_4K():
    '''
    生成2K数据集。共1K个关键字，每个关键字对应4个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_4K.txt'，且储存在"./data_4K.json"
    '''

    d={}
    for i in range(1,1001):
        # 随机生成4个整数
        l=[]
        for j in range(4):
            s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open ("data_4K.txt", 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open("./data_4K.json", 'w') as json_file:
        json_file.write(json_str)



def get_6K():
    '''
    生成6K数据集。共1K个关键字，每个关键字对应6个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_6K.txt'，且储存在"./data_6K.json"
    '''

    d={}
    for i in range(1,1001):
        # 随机生成6个整数
        l=[]
        for j in range(6):
            s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open ("data_6K.txt", 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open("./data_6K.json", 'w') as json_file:
        json_file.write(json_str)



def get_8K():
    '''
    生成8K数据集。共1K个关键字，每个关键字对应8个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_8K.txt'，且储存在"./data_8K.json"
    '''

    d={}
    for i in range(1,1001):
        # 随机生成8个整数
        l=[]
        for j in range(8):
            s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open ("data_8K.txt", 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open("./data_8K.json", 'w') as json_file:
        json_file.write(json_str)


def get_data_build(dataset_size,pickle_file,json_file):
    '''
    生成指定大小的数据集。共1K个关键字，每个关键字对应dataset_size/1000个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_4K.txt'，且储存在"./data_4K.json"

    Parameters:
    dataset_size:数据集大小
    pickle_file:pickle文件的名称
    json_file: json文件的名称
    '''

    d={}
    for i in range(0,1001):
        # 随机生成4个整数
        l=[]
        for j in range(int(dataset_size/1000)):
            s=str(random.randint(0,2000))
            while s in l:
                s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open (pickle_file, 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open(json_file, 'w') as json_file:
        json_file.write(json_str)



def get_data_update(dataset_size,pickle_file,json_file):
    '''
    生成指定大小的数据集。共200个关键字，每个关键字对应dataset_size/200个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_4K.txt'，且储存在"./data_4K.json"

    Parameters:
    dataset_size:数据集大小
    pickle_file:pickle文件的名称
    json_file: json文件的名称
    '''

    d={}
    for i in range(0,200):
        # 随机生成整数
        l=[]
        for j in range(int(dataset_size/200)):
            s=str(random.randint(0,2000))
            while s in l:
                s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open (pickle_file, 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open(json_file, 'w') as json_file:
        json_file.write(json_str)


def get_data_del(dataset_size,pickle_file,json_file):
    '''
    生成指定大小的数据集。共1000个关键字，每个关键字对应dataset_size/1000个文件id

    将倒排索引转换为普通字符串的形式并用pickle持久化储存为'./data_del.txt'，且储存在"./data_del.json"
    先读取 data_10K，然后在其基础上为每个关键字都生成若干个不重复的的ind，并储存在'./data_del.txt'。
    实验中，先读取./data_del.txt进行add，再对这些数据进行删除实验

    Parameters:
    dataset_size:数据集大小
    pickle_file:pickle文件的名称
    json_file: json文件的名称
    '''

    # 先读取10K数据集
    with open('../data/data_10K.txt', 'rb') as f:  # 打开文件
        inverted_index = pickle.load(f)

    d={}
    for i in range(0,1000):
        # 随机生成整数
        l=[]
        for j in range(int(dataset_size/1000)):
            s=str(random.randint(0,2000))
            while s in l or s in inverted_index[str(i)]:
                s=str(random.randint(0,2000))
            l.append(s)
        
        d[str(i)]=l
    
    with open (pickle_file, 'wb') as f: #打开文件
        pickle.dump(d, f)

    json_str = json.dumps(d,indent=4)
    with open(json_file, 'w') as json_file:
        json_file.write(json_str)






if __name__=='__main__':
    # 用于测试del的数据
    dict1={"0": [
        "1788",
        "1051"
    ]}

    dict2={"0": [
        "1788",
        "1051"
    ],
    "1": [
        "1157",
        "276"
    ]}

    dict3={"0": [
        "1788",
        "1051"
    ],
    "1": [
        "1157",
        "276"
    ],"2": [
        "1795",
        "898"
    ],
    "3": [
        "1926",
        "657"
    ]}

    dict4={
        "0": [
        "1788",
        "1051"
    ],
    "1": [
        "1157",
        "276"
    ],"2": [
        "1795",
        "898"
    ],
    "3": [
        "1926",
        "657"
    ],"4": [
        "457",
        "73"
    ],
    "5": [
        "1489",
        "1461"
    ],
    "6": [
        "136",
        "603"
    ],
    "7": [
        "206",
        "287"
    ]
    }

    dict5={
        "0": [
        "1788",
        "1051"
    ],
    "1": [
        "1157",
        "276"
    ],"2": [
        "1795",
        "898"
    ],
    "3": [
        "1926",
        "657"
    ],"4": [
        "457",
        "73"
    ],
    "5": [
        "1489",
        "1461"
    ],
    "6": [
        "136",
        "603"
    ],
    "7": [
        "206",
        "287"
    ],
    "8": [
        "763",
        "511"
    ],
    "9": [
        "1355",
        "791"
    ],
    "10": [
        "1576",
        "1820"
    ],
    "11": [
        "369",
        "94"
    ],
    "12": [
        "415",
        "357"
    ],
    "13": [
        "979",
        "843"
    ],
    "14": [
        "1770",
        "1545"
    ],
    "15": [
        "327",
        "1981"
    ]
    }
    print(len(dict1),len(dict2),len(dict3),len(dict4),len(dict5))



    # get_data_del(1000,"../data/data_del_1K.txt","../data/data_del_1K.json")
    # get_data_del(1000,"../data/data_del_1K.txt","../data/data_del_1K.json")
    # get_data_del(2000,"../data/data_del_2K.txt","../data/data_del_2K.json")
    # get_data_del(3000,"../data/data_del_3K.txt","../data/data_del_3K.json")
    # get_data_del(4000,"../data/data_del_4K.txt","../data/data_del_4K.json")
    # get_data_del(5000,"../data/data_del_5K.txt","../data/data_del_5K.json")



    #  用于测试build的数据
    # get_data_build(2000,"../data/data_2K.txt","../data/data_2K.json")
    # get_data_build(4000,"../data/data_4K.txt","../data/data_4K.json")
    # get_data_build(6000,"../data/data_6K.txt","../data/data_6K.json")
    # get_data_build(8000,"../data/data_8K.txt","../data/data_8K.json")
    # get_data_build(10000,"../data/data_10K.txt","../data/data_10K.json")

    # 用于测试update的数据
    # get_data_update(400,"../data/data_400.txt","../data/data_400.json")
    # get_data_update(800,"../data/data_800.txt","../data/data_800.json")
    # get_data_update(1200,"../data/data_1200.txt","../data/data_1200.json")
    # get_data_update(1600,"../data/data_1600.txt","../data/data_1600.json")
    # get_data_update(2000,"../data/data_2000.txt","../data/data_2000.json")
    
    # get_data(2000,"./dataset_2K.txt","./dataset_2K.json")

    # transform_data()

    # # 10K数据集
    # with open ("data_10K.txt", 'rb') as f: #打开文件
    #     dict=pickle.load(f)
    
    # json_str = json.dumps(dict,indent=4)
    # with open("./data_10K.json", 'w') as json_file:
    #     json_file.write(json_str)

    
    # print(dict['999'])
    # print(dict['1000'])
    # print(dict)
