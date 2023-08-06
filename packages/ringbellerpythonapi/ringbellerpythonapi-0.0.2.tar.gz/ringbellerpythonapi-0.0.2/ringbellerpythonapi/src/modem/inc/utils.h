/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef UTILS_H
#define UTILS_H

/*********************Includes*************************/
#include <string>
using namespace std;
/******************************************************/

// Modem library utilities class.
class Utils
{
public:
	/** Convert escaped characters.
			@param input	String to be converted
			@return			Converted string
		 */
	string escaped(const string &input);
};

#endif // UTILS_H