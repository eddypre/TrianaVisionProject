#!/bin/sh

fecha=`date "+%Y-%m-%d"`
echo $fecha
sleep 1
nohup gedit 'salida.txt'&
#gzip 
