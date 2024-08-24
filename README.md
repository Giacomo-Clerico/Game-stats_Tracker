# Game-stats_Tracker
Simple, customizable UI to input your game stats, and get back charts and other data about your gameplay


# How to use

## Linux
for linux you can just download the Release-Linux.zip from the latest release, unzip it and execute it with ./main

## Execute from source code 
downloade the source code and execute it with python3 main.py

## Build your own
the releases are currently made with pyinstaller, you can replicate it but keep in mind that fields.json and graphs.json are required in the same directory for it to run

# Customization

## To add more fields
just modify the fields.json file to include the name of the field and the SQL type

## To add more options to the graph maker
modify the graphs.json file with an object containing the name in the button and the two fields.
