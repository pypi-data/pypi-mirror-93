#
# This file is part of the Ringbeller CLI for EC25 communications library
#
build:
	g++ -std=c++17 -g -Wall -Werror -fpic -c modem/src/*.cpp -c wrapper/*.cpp -L/usr/local/lib -lwiringPi -lpthread -lrt -lcrypt -lasound -lsndfile -lstdc++fs
	g++ -shared -o lib/libmodemwrapper.so *.o  -lwiringPi -lpthread -lrt -lcrypt -lasound -lsndfile -lstdc++fs
	rm -f *.o
	
clean:
	rm -f *.o
	rm -f lib/*
