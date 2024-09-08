#!/bin/bash
clear
mkdir -p ./Pablo/{a/f/{j/{p,q/w/y},k/{r,x,z}},b/g,c/h/{l,m/{s,t}},d,e/i/{n,o/v}}
cd ./Pablo/a/f/j/q/w/y
touch archivo1.txt ejemplo.py tarea.txt otros.py taller.txt
cp *.* ~/Pablo/e/i/n
cp *.py ~/Pablo/c/h
cp ???l*.txt ~/Pablo/b
cp -r  ~/Pablo/e/i/n ~/Pablo/a/f/k/z 
chmod a-rwx ~/Pablo/a/f/j/q/w/y/archivo1.txt
chmod u=rw,g=x,o=w ~/Pablo/a/f/j/q/w/y/ejemplo.py
cd ~/Pablo/b
chmod 417 *.*
