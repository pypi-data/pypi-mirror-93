#
# This file is part of the modem communications library for Raspberry Pi
#

library:
	g++ -std=c++17 -g -Wall -c src/*.cpp
	ar rcs lib/libRbIotModem.a *.o
	rm -f *.o

install: library
	sudo rm -rf /usr/include/rbIotModem
	sudo mkdir /usr/include/rbIotModem
	sudo cp inc/* /usr/include/rbIotModem
	sudo cp lib/libRbIotModem.a /usr/lib

clean:
	rm -f lib/*
