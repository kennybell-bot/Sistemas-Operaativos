#!/bin/bash

es_primo(){
local num=$1
local divisor=$2

if((divisor == 1)); then
echo $1
return
elif(($num%$divisor == 0)); then
echo 0
return
fi
}

imprimir_primos(){
local i=$2
while((i<=100)); do
resultado=$(es_primo $i $(($i - 1)))
if [ $resultado == $1 ]; then
echo $i
fi
((i++))
done
}

imprimir_primos
