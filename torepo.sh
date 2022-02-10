#!/bin/bash
echo 
echo "Verify you are running this from the repo root"
echo
echo "If not in repo root break and re-run"
echo
read -n 1 -s
cp -v test/*.py .
cp -vr test/templates .
cp -v test/requirements.txt .
echo "Code copied to repo root"