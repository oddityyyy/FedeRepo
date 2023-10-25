pragma solidity >=0.4.22 <0.6.0;

contract DSSE_Judge {
    // checklist，储存l_w->digest的映射
    mapping(bytes16 => bytes32) private checklist;
    // 第二轮的验证结果
    bool private is_equal;
    // 储存每个分组block的digest
    mapping(uint=>bytes32) private blockxor;
    // 总的digest
    bytes32 private digest;




    // 将1个(l_w,digest) pair加入checklist
    function set(bytes16 l_w, bytes32 digest_new) public {
        checklist[l_w] = digest_new;
    }




    // 给定一个block，其中含有多个val，计算其 H(val1) xor H(val2) xor...，并储存在blockxor状态中
    // block：数据块，包含多个val
    // len：数据块中元素的个数
    // blocknum：第几个block分组
    function batch_cal_hash(
        bytes32[] memory my_block,
        uint256 len,
        uint256 blocknum
    ) public {
        // 储存计算中的异或值
        bytes32 xor;

        for (uint256 i = 0; i < len; i++) {
            if (i == 0) {
                // 使用非标准打包模式进行编码
                xor = keccak256(abi.encodePacked(my_block[i]));
            } else {
                bytes32 d=keccak256(abi.encodePacked(my_block[i]));
                xor=xor ^ d;
            }
        }

        blockxor[blocknum]=xor;
    }


    // 将前面所有分组的digest组合起来计算最终的digest，并储存在digest状态中
    // totalnumber：总的分组数量
    function cal_digest(uint totalnumber) public{
        bytes32 xor;

        for(uint i=0;i<totalnumber;i++){
            if(i==0){
                xor=blockxor[i];
            }else{
                xor=xor^blockxor[i];
            }
        }

        digest=xor;
    }




    // 第二轮验证，智能合约之前根据server返回的结果计算出一个digest，然后根据储存在checklist中的数据算出正确的digest，
    // 判断两个digest是否相等，并将判断结果储存在is_equal状态中
    // l_w_list：储存BRC对应所有w的l_w
    // len：l_w_list的长度
    function judge(bytes16[] memory l_w_list,uint len) public{
        bytes32 xor;

        // 根据checklist和l_w计算出正确的digest
        for(uint i=0;i<len;i++){
            if(i==0){
                xor=checklist[l_w_list[i]];
            }else{
                xor=xor^checklist[l_w_list[i]];
            }         
        }

        //进行比较
        if(xor==digest){
            is_equal=true;
        }
        else{
            is_equal=false;
        }
    }




    // 返回is_equal状态，通过call调用即可，不产生交易
    function get_is_equal() public view returns (bool){
        return is_equal;
    }

}
