#!/usr/bin/bash 

i=0
while [ $i -le 2 ];
do
  echo $i
  ((i++))
  sleep 0.01
done