#!/usr/bin/env bash
export FORGE_INSTALLER_URL="https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.0.66/forge-1.19.4-45.0.66-installer.jar"
export DEB_DEPENDENCIES=(
  "openjdk-17-jre-headless"
  "python3"
  "cargo"
)

sudo apt update

for n in $(DEB_DEPENDENCIES)
do
  sudo apt install "$n"
done

cargo install --git https://github.com/Storyyeller/Krakatau.git

mkdir "ServerInstance"
curl $FORGE_INSTALLER_URL -o ServerInstance/forge-installer.jar
