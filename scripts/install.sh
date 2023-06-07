export FORGE_INSTALLER_URL="https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.0.66/forge-1.19.4-45.0.66-installer.jar"
export DEB_DEPENDENCIES=(
  "openjdk-17-jre-headless"
  "python3"
  "cargo"
)

curl $FORGE_INSTALLER_URL -o ServerInstance/forge-installer.jar
