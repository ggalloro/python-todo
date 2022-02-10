#!/bin/bash
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
