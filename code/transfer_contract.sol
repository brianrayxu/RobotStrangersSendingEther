pragma solidity ^0.4.10;

contract StoreIntegerValue {
    address owner;
            int locationData;

    function StoreIntegerValue() {
                owner = msg.sender;
		                }

    function setLocationData(int _locationData) {
                require(msg.sender == owner);
		                    locationData = _locationData;
				                    }

    function getLocationData() public constant returns (int) {
                //require(msg.sender == owner);
		                    return locationData;
				                    }
						            }
