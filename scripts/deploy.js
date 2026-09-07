import hre from "hardhat";

async function main() {
  const IdentityAnchor =
    await hre.ethers.getContractFactory("IdentityAnchor");

  const contract =
    await IdentityAnchor.deploy();

  await contract.waitForDeployment();

  const address =
    await contract.getAddress();

  console.log("\n======================================");
  console.log("       CONTRACT DEPLOYMENT");
  console.log("======================================");
  console.log("IdentityAnchor deployed to:");
  console.log(address);
  console.log("======================================\n");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});