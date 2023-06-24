#!/usr/bin/env bash
FORGE_INSTALLER_URL="https://maven.minecraftforge.net/net/minecraftforge/forge/1.20-46.0.14/forge-1.20-46.0.14-installer.jar"
BF_MOD_URL="https://mediafilez.forgecdn.net/files/4598/682/BlockFront-1.20.1-0.2.0.1a-RELEASE.jar"
DEB_DEPENDENCIES=( openjdk-17-jdk python3 curl )

echo "BY RUNNING THIS INSTALLER YOU ACCEPT THE MINECRAFT EULA!"

sudo apt update
for n in "${DEB_DEPENDENCIES[@]}"
do
  sudo apt install -y "$n"
done

command -v rustc >/dev/null 2>&1 || { curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; source "$HOME/.cargo/env"; }
cargo install --git https://github.com/Storyyeller/Krakatau.git --branch v2

command -v minecraft-world-splicer >/dev/null 2>&1 || { curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash; export NVM_DIR="$HOME/.nvm"; [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"; nvm install node; npm install -g https://github.com/DasBlackfur/minecraft-world-splicer.git; }

rm -rf ~/ServerInstance
mkdir -p ~/ServerInstance

curl $FORGE_INSTALLER_URL -o ~/ServerInstance/forge-installer.jar
java -jar ~/ServerInstance/forge-installer.jar --installServer ~/ServerInstance

echo "eula=true" > ~/ServerInstance/eula.txt
rm ~/ServerInstance/run.sh
echo 'java @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.20-46.0.14/unix_args.txt nogui $@' > ~/ServerInstance/run.sh

rm -rf ./tmp
mkdir -p ./tmp

cd ./world_repo/ || exit 1
python3 ../scripts/world-splice.py

mkdir -p ~/ServerInstance/blockfront/assets/server/
cp -r tmp/assets/* ~/ServerInstance/blockfront/assets/server/

cp -r tmp/world ~/ServerInstance/world

curl $BF_MOD_URL -o ../tmp/bf.jar
cd ../tmp || exit 1
python3 ../scripts/patch.py
mkdir -p ~/ServerInstance/mods
cp ./bf.jar ~/ServerInstance/mods/

cp ../config/server.properties ~/ServerInstance/

echo "INSTALLATION FINISHED YOU CAN RUN THE run.sh FILE NOW!"