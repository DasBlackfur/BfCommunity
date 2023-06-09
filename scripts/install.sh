#!/usr/bin/env bash
FORGE_INSTALLER_URL="https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.0.66/forge-1.19.4-45.0.66-installer.jar"
DEB_DEPENDENCIES=( openjdk-17-jre-headless python3 curl )

echo "BY RUNNING THIS INSTALLER YOU ACCEPT THE MINECRAFT EULA!"

sudo apt update
for n in "${DEB_DEPENDENCIES[@]}"
do
  sudo apt install -y "$n"
done

command -v rustc >/dev/null 2>&1 || { curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; source "$HOME/.cargo/env"; }
cargo install --git https://github.com/Storyyeller/Krakatau.git --branch v2

rm -rf ~/ServerInstance
mkdir -p ~/ServerInstance

curl $FORGE_INSTALLER_URL -o ~/ServerInstance/forge-installer.jar
java -jar ~/ServerInstance/forge-installer.jar --installServer ~/ServerInstance

echo "eula=true" > ~/ServerInstance/eula.txt