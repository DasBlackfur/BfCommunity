#!/usr/bin/env bash
FORGE_INSTALLER_URL="https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.0.66/forge-1.19.4-45.0.66-installer.jar"
DEB_DEPENDENCIES=( openjdk-17-jre-headless python3 curl )

sudo apt update

for n in "${DEB_DEPENDENCIES[@]}"
do
  sudo apt install -y "$n"
done

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

cargo install --git https://github.com/Storyyeller/Krakatau.git --branch v2

mkdir -p "ServerInstance"
rm ServerInstance/forge-installer.jar
curl $FORGE_INSTALLER_URL -o ServerInstance/forge-installer.jar
