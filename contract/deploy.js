const hardhat = require("hardhat");

async function main() {
    const solAMM = await hardhat.ethers.getContractFactory("solAMM");
    
    console.log("Deploying solAMM...");

    TestALpha = "0x82357Fb36B13E4a5e13FB4e292fCa01260cA7E7E"
    TestBeta = "0xd0018302138E8fb982b44C7c008b9BC83A2C8d6a"

    const contract = await solAMM.deploy(TestALpha,TestBeta);

    console.log(contract.target)
}

main();