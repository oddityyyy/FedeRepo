pragma solidity >=0.4.22 <0.6.0;

contract SavePath{
    string name;
    event onset(string newname);
    constructor() public{
       name = "Hello, World!";
    }

    function get() view public returns(string){
        return name;
    }

    function set(string n) public{
	emit onset(n);
    	name = n;
    }
}
