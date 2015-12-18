#!/bin/bash
#file   : travis.sh
#author : ipapapa
#date   : 2015-10-20


if [ -n "$TRAVIS" ]; then
    #sudo apt-get install socat

    #python libs
    sudo pip install redis
    sudo pip install git+https://github.com/andymccurdy/redis-py.git@2.10.3
    #sudo pip install git+https://github.com/idning/python-memcached.git#egg=memcache
fi

#build Dynomite
CFLAGS="-ggdb3 -O0" autoreconf -fvi && ./configure --enable-debug=log && make 

mkdir test/_binaries
ln -s `pwd`/src/nutcracker  test/_binaries/
cp `which redis-server` test/_binaries/
cp `which redis-cli` test/_binaries/
cp `which memcached` test/_binaries/

cd test

#./func_test.py


