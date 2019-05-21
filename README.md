# Robot Strangers Collaborating
###### by David Payne and Brian Xu 

## Overview
 Multiple devices implemented with the capability to determine proximity for sensitive actions. Built using smart contracts on the Ethereum Virtual Machine. 

## Evaluation Criteria
 The central problem we are trying to solve is how to get robots to collaborate in an environment where they do not have any reason to trust each other and cannot communicate directly. We are approximating a ‘robot’ as a constrained resource device such as a Raspberry Pi or FRDM board. The expectation is that these won’t be ‘robots’ in terms of having actuators but that what is developed would be applicable. Another historical example we built upon is the idea of multi-key authentication such as happens in movies with launching nuclear warheads in which two people must turn their own key simultaneously at the same panel.

 In order to tie this idea of distributed tasks into the concepts reinforced in class, we will have our ‘robots’ act as agents. This project builds upon previous work and projects done related to swarming, Peer-to-Peer networking such as in botnets and other forms of distributed computing, and blockchain for IoT devices.

In order to classify a success, our solution should have the following capabilities:

1. Upon request, "robot" traders (IoT devices) automatically start trade process.
2. During trade process, automatically determine that both members of the trade are within a reasonable proximity.
3. Confirm in proximity and ready for secure action

## Solution Design

Figure: Overview of Technology Stack. 
![Stack Graphic](/images/Stack.png)

Roughly in three components: smart contracts, processing node, and function.

Figure: Overview of Process. 

![Process Graphic](/images/Process.png)

Each node (computer), periodically fetches its router's public IP address via a call to whatsmyrouterip.com/raw and then passes that IP address to a previously deployed smart contract linked to that node. The smart contract writes that IP address to the blockchain - in Ethereum phrasing, this can be seen as an 'oracle' as it's writing data outside the blockchain to the blockchain. Each node is then able to pull the most recent transaction data for the smart contract for the other node(s) and pull out the other node(s) most recent IP address. If the other router's IP address matches the node's current IP address, it confirms proximity. 

#### 1 : Wallet/Node Setup on RPI
##### A. Initial Software Choices + Decisions
The first step to our solution is to setup the Raspberry Pi to be able to maintain and store funds. The very first step of our solution involves the OS that the Raspberry Pi will run. Instead of using the normal Raspbian distribution, we chose to use Raspbian Stretch (Headless) in order to save space on the SD card. Not having a GUI or a full OS gives us more space to use for storing the blockchain and when choosing an OS to use, it was unclear how much memory the blockchain was to take so every precaution was taken.

Next, we needed to pick how we were going to communicate to the blockchain and which blockchain to pick. We use the Go-ethereum client and Ethereum cryptocurrency as the framework for the transactions. The reason we chose Ethereum is due to the fact that Ethereum was created specifically for deploying smart contracts that are able to execute a wide variety of code beyond just money transfer. Ethereum differs in other cryptos such as its popular cousin BitCoin because of its use of Solidity, a smart contract language with Javascript based syntax. Bitcoin runs smart contracts using its own scripting language but Solidity offers developers full control over their smart contracts, giving them more freedom on the usage and creation of their contracts. 

Within Ethereum, there are many different individual networks ranging from the main network to numerous test networks with fake cryptocurrency for developers to use to test their contracts and programs. Given that we are experimenting and developing features, we chose to use the Rinkeby TestNet. The Rinkeby TestNet is one of a handful of testnets which Ethereum provides. It is only supported by the go-eth client and is the smallest chain to date. This makes it optimal for the scope of our project because it means faster sync times as well as smaller memory requirements to hold the blockchain's data.

##### B. Geth + Light Sync
In order to interact with the Ethereum blockchain, we chose to use Go-eth(geth), due to its popular use in the community as well as its light sync function. The light sync function is vital to our project due to the fact that it uses minimal data and time to store the information of the entire blockchain. With the chain reaching over 4 million blocks, doing a full sync would not be possible on the specs of an Raspberry Pi because there is no reasonable SD card that could store the over 1TB of data the blockchain boasts. In addition, the RAM and processing power of the Pi would mean that our sync would take months to complete.

After setting up our Raspberry Pis as nodes, we added fake currency from an online ethereum faucet provided by Rinkeby and started deploying our first smart contracts.

#### 2. Smart Contract Setup
##### A. Remix Online IDE
In our implementation, we use two smart contracts to accomplish the verification and transfer of the trade process. Each contract is based on a particular node and is used to store IP information for verification of proximity within a python script. As mentioned before, the language used to write smart contracts is Solidity, a language with syntax based on Javascript. We use the Remix IDE as our environment of choice because of its ease of use when it comes to writing, testing, and deploying smart contracts. On the IDE, which is browser based, you are able to compile using any release of the solc compiler and afterwards, test and deploy your contract all within the same web-page.

##### B. MetaMask
MetaMask, a wallet client, was used due to its integration with Remix. This integration allowed for a straightforward deployment process as the smart contract on Remix could be deployed with gas provided by the MetaMask wallet.

#### 3. Function
##### Etherscan (Scraping)
A key part of this project was fetching data stored on the Rinkeby blockchain by our smart contracts. Etherscan, a website, provides an interface for watching actions on the blockchain, including smart contract transactions. Chose Etherscan over other options due to initial belief that their APIs were well suited for what we wanted. After many hours of work, we determined that their APIs would not work reliably for what we wanted (pulling the most recent transaction data on a given smart contract). Both our own testing and reading of forums showed that a lot of the Etherscan API is still experimental, including the part we wanted to use. Etherscan did have another benefit, a standard and static webpage structure. This meant it was easy to just scrape the most recent transaction hash from their website by pulling the page using the requests python library and parsing the text.

##### Web3py
We wanted to both transmit data, an IP address, to a smart contract and pull transaction info from a transaction hash. The Web3py library contained these desired functions. And most importantly, had sample code for accessing transactions that still worked. A consistent problem we ran into with this project was the number of guides and tools we looked at that were deprecated, sometimes within just a couple months of publication. 

##### Python3
We used Python as the scripting language given its ability to work with Web3py library of functions and the relative ease compared to lower-level languages of doing needed functions such as parsing webpage text to pull out a transaction hash.

## Concerns + Issues
 ##### 1. Constantly Changing Community
 Deprecated Mist, Wallet, light client protocols, articles, solc syntax, documentation (all the numerous wikis for each solidity release), lots of conflicting information on bugs and capabilities of smart contracts, 

 ##### 2. Ethereum Light Sync Issues
 As of the time of this implementation, the Ethereum Light Sync feature is a completely experimental part of the Geth client. Due to this fact, we had many troubles doing our sync of the blockchain. For example, the lack of peers on the light network, constant crashing during syncing, chaindata corruption, unsupported account/key viewing
 
 ##### 3. Web3py and Python scripts were buggy on Raspberry Pi
 We ran into timeout issues with the script and web3py functions on the Raspberry Pi. Tried increasing the timeout but the code still wouldn't work reliably. We believe this is due to the aforementioned issues with light sync on the Pis that had a tendency to hang up or crash. We were able to demonstrate reliably our project on laptops and so that is what we used for our video.
 
## Unimplemented Features
#### Alternative Proximity Modules
Image Processing and XBee Shield module. Given that this project was focused on a proof of concept for detecting proximity via data written to a blockchain via smart contracts, we decided to remove focus proximity sensing to focus more on the smart contract/blockchain portion of the project. We therefore substituted in the proximity proxy of IP address as two devices on the same router will have the same public IP address and routers have a limited range so by sharing an IP address, you effectively know you are within a few 10s of meters.

#### Hosting a Private Ethereum Network (Ganache or Docker)
This was more of a design decision as we chose to deploy our smart contracts onto a public testnet, Rinkeby. This led to challenges as we did not have full control over the network. A large issue was working with the parameters set on the testnet that cannot be changed by individual users, such as the gas limit. Getting posts to execute was a large problem. It turns out it was an issue with not everything being on the same network. We got an issue of the gas limit being only 5000 while the default minimum for executing a contract deployed by Remix is 21000. This appeared at one point to be a catch-22. What ended up being the issue was that after originally syncing a rinkeby node with Geth, we hadn't realized we had to add the '--rinkeby' flag everytime we ran Geth console so by default it switched to try to sync the mainnet, which is huge. Our machine was still working at beginning blocks that had such a low gas limit. Once we fixed that, we could successfully execute contracts on the Rinkeby testnet. 


## Conclusion
 This project taught us a lot about how the blockchain and smart contracts work, coming from almost zero knowledge prior. This included funny realizations such as that early smart contract failures were remarkably durable. A key part of a blockchain is the immutability of the past. This includes that any deployed smart contract can't be changed after the fact. Therefore there are now a couple of zombie smart contracts that we tested that will continue to live on Rinkeby testnet.
 We also dicovered how quickly development on Ethereum and related tools is moving. We were consistently amazed at how guides and feature specifications published recently (as in within weeks or months) would be deprecated or otherwise non-functional when we tried them. 
 As a final point, it was interesting how 'centralized' the 'decentralized' Ethereum blockchain can become due to the use of intermediaries to interact with it. For instance, many people, including us, use Etherscan data. If Etherscan changes their APIs (or webiste structure in our case) either just due to natural development or maliciously, apps like ours will break. That bears a similarity to the decentralized internet as almost everyone uses an intermediary, Google, to interact with it. While it's possible to bypass those intermediaries, it is inconvenient. 
 Overall, through this project, we learned a lot and demonstrated a capability that could be built upon for future trustless collaboration projects. 
 
## TOOLS
- geth (https://github.com/ethereum/go-ethereum/wiki/geth)
- RPi (https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
- Solidity (https://github.com/ethereum/solidity)
- Remix IDE (https://remix.ethereum.org/)
- MetaMask (https://remix.ethereum.org/)
- Etherscan (https://etherscan.io/)
- web3.py (https://web3py.readthedocs.io/en/stable/)

## REFERENCES
-https://ethereum.stackexchange.com/questions/38968/how-to-write-a-smart-contract-for-rpi-sensor
-https://ethereum.stackexchange.com/questions/8211/connecting-two-nodes-one-on-rasberry-pi-and-other-on-ethereum
-https://programtheblockchain.com/posts/2017/12/15/writing-a-contract-that-handles-ether/
-https://medium.com/@ConsenSys/a-101-noob-intro-to-programming-smart-contracts-on-ethereum-695d15c1dab4
-https://solidity.readthedocs.io/en/v0.5.3/index.html
-https://medium.com/@ConsenSys/a-101-noob-intro-to-programming-smart-contracts-on-ethereum-695d15c1dab4

## Video
https://youtu.be/_XxAsqZ09z4
