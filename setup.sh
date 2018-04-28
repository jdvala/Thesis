#!/bin/bash

# A setup script to install necessary programs when I change the operating system, which happens quite ofter

##### NOTE: THIS IS SRICTLY FOR DEBAIN BASED SYSTEMS##################

# Defining Colors:
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`



# Let's update the system

echo "\n\n${red}Let's make this system great again!!\n\n${reset}"

sudo apt-get update

echo $"Update Completed."

echo $"\nDownloading Anaconda..."
cd ~/Downloads

wget https://repo.anaconda.com/archive/Anaconda3-5.1.0-Linux-x86_64.sh

echo "\nDownload Completed."
echo "\n\n\t${green} Installing Anaconda\n${reset}"
sh Anaconda3-5.1.0-Linux-x86_64.sh

echo "\nCreating Environment.."

echo "\nEnter you environment name:"
read envname

echo  "${green}\n\n\n NOTE: THE ENVIRONMENT WILL BE CREATED WITH PYTHON 3.6\n\n\n${reset}"
echo  "\nCreating Environment: "$envname

conda create --name $envname python=3.6

echo "Succesfully Created Environment."
echo "Activating Environment: "$envname

## activating env 

source activate $envname

echo "Environment activated..."

echo "Downloading necessary libraries..."

pip install keras && pip install tensorflow && pip install pandas && pip install skelarn && pip install ipykernal && pip install jupyter

# Everything is set except installing vim and google chrome

echo "Installing Vim..."
sudo apt-get install vim

echo "Installing Google Chrome..." 

echo "Adding Keys"
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

echo "Adding Repository and Setting it..."
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list

echo "Updating Changes..."

sudo apt-get update

echo "Downloading and Installing Chrome Package, stable release"
sudo apt-get install google-chrome-stable

echo "Installing git..."
sudo apt-get install git

echo "Installing VS code"

cd ~/Download
wget https://az764295.vo.msecnd.net/stable/3aeede733d9a3098f7b4bdc1f66b63b0f48c1ef9/code_1.22.2-1523551015_amd64.deb

sudo dpkg -i code_1.22.2-1523551015_amd64.deb

echo "SETUP COMPLETE."
