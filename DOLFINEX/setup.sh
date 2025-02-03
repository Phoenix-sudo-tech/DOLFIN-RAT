#!/bin/bash

# Function to check internet connectivity
check_internet() {
    echo "Checking internet connection..."
    if ping -c 1 google.com &> /dev/null; then
        echo "Internet is connected."
        return 0  # Success
    else
        echo "No internet connection. Please check your network."
        return 1  # Failure
    fi
}

# Display "DOLFIN" in ASCII art with neon red color
echo -e "\033[38;5;196m"  # Set color to neon red (using 256-color ANSI)
echo " DDDDD   OOO   L      FFFFF  III  N   N "
echo " D   D  O   O  L      F       I   NN  N "
echo " D   D  O   O  L      FFFF    I   N N N "
echo " D   D  O   O  L      F       I   N  NN "
echo " DDDDD   OOO   LLLLL  FFFFF  III  N   N "
echo -e "\033[0m"  # Reset color

# Check if internet is connected
check_internet
if [ $? -eq 0 ]; then
    # Run apt update and apt upgrade
    echo "Running apt update and apt upgrade..."
    sudo apt update -y
    sudo apt upgrade -y
    echo "System updated successfully."
else
    echo "Skipping system update due to no internet connection."
fi

# Function to verify if Metasploit is installed
check_metasploit() {
    if command -v msfvenom &> /dev/null && command -v msfconsole &> /dev/null; then
        echo "Metasploit is already installed."
    else
        echo "Metasploit is not installed. Installing..."
        install_metasploit
    fi
}

# Function to install Metasploit
install_metasploit() {
    echo "Running installation command for Metasploit..."
    sudo apt install metasploit-framework -y
    echo "Metasploit installation completed."
}

# Verify if Metasploit is installed
check_metasploit
