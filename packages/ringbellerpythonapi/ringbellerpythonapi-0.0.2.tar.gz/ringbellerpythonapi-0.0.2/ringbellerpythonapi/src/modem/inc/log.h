/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef LOG_H
#define LOG_H

/*********************Includes*************************/
#include <iostream>
#include <string>
using namespace std;
/******************************************************/

// Modem library log class.
class Log
{
public:
	/** Constructor
			@param modemName	(Optional) Name of the modem
		 */
	Log(string modemName = "");

	/** Set log level
			@param verbose	Log verbose level (0-4)
		 */
	void setLevel(int verbose);

	/** Log debug events
			@param fName	Function name
			@param message	Message to be logged
		 */
	void debug(string fName, string message);

	/** Log warnings
			@param fName	Function name
			@param error	Warnings to be logged
		 */
	void warning(string fName, string error);

	/** Log info
			@param fName	Function name
			@param info		Info to be logged
		 */
	void info(string fName, string info);

	/** Log error
			@param fName	Function name
			@param error	Error to be logged
		 */
	void error(string fName, string error);

private:
	static int _level;		  //Log level
	static string _modemName; //Modem name

	/** Print to console
			@param color	Output color
			@param fName	Function name
			@param log		Log value
		 */
	void _print(string color, string fName, string log);
};

#endif // LOG_H