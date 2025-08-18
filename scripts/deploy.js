async function main() {
  const EventLogger = await ethers.getContractFactory("EventLogger");
  const logger = await EventLogger.deploy();

  await logger.waitForDeployment(); // méthode correcte depuis Hardhat 2.12+

  console.log(" EventLogger deployed to:", await logger.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
