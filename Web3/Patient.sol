pragma solidity ^0.6.1;

contract Patient{
	string phoneNumber;
	string age;
	string skin_disease_ipfs;
	string bloodGroup;
	string bloodPressure;
	string date;
	string time;
	string state;
	string city;
	constructor(string memory _phoneNumber, string memory _age, string memory _skin_disease_ipfs,
				string memory _bloodGroup, string memory _bloodPressure, string memory _date,
				string memory _time, string memory _state, string memory _city) public {
		phoneNumber = _phoneNumber;
		age = _age;
		skin_disease_ipfs = _skin_disease_ipfs;
		bloodGroup = _bloodGroup;
		bloodPressure = _bloodPressure;
		date = _date;
		time = _time;
		state = _state;
		
		city = _city;
	}
	function getAge() public view returns(string memory){
		return age;
	}
	function getBloodGroup() public view returns (string memory){
		return bloodGroup;
	}
	function getBloodPressure() public view returns (string memory){
		return bloodPressure;
	}
	function getPhoneNumber() public view returns (string memory){
		return phoneNumber;
	}
	function getSkinDiseaseIpfs() public view returns (string memory){
		return skin_disease_ipfs;
	}
	function getDate() public view returns (string memory){
		return date;
	}
	function getTime() public view returns (string memory){
		return time;
	}
	function getState() public view returns (string memory){
		return state;
	}
	function getCity() public view returns (string memory){
		return city;
	}

}