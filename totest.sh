#!/bin/bash
# This version of the script works only with GNU sed
# If using a mac, please run setup.sh
echo 
echo "Verify you are running this from the repo root"
echo
echo "If not in repo root break and re-run"
echo
read -n 1 -s
cp -v *.py test/
cp -vr templates test/
cp -v requirements.txt test/
echo "Code copied to test folder"
