#!/bin/bash

# Ethan (aka the person writing this) is kinda lazy, and got tired of constantly typing the same commands,
# So I created this script to make commiting easier :P

#Only tested on linux

#TODO: Make Windows port for windows devs

git status

echo "Commit Message:"
read CommitComment

clear

git add .

git commit -m "$CommitComment"

git push origin main
