/*
This file is part of the Log communications library for Raspberry Pi
*/
#include "../inc/log.h"

//Instantiate modem name variable.
string Log::_modemName = "MODEM";

//Instantiate log level variable.
int Log::_level;

//Constructor.
Log::Log(string modemName)
{
  // Set modem name.
  if (modemName != "")
  {
    _modemName = modemName;
  }
}

//Set verbose logging level.
void Log::setLevel(int level)
{
  _level = level;

  debug("Log::setLevel", "Log verbose level set to <" + to_string(_level) + ">.");
}

//Log debug.
void Log::debug(string fName, string debug)
{
  if (_level > 3)
  {
    _print("\033[36m", fName, "[DEBUG] " + debug);
  }
}

//Log info.
void Log::info(string fName, string info)
{
  if (_level > 2)
  {
    _print("", fName, " " + info);
  }
}

//Log warning.
void Log::warning(string fName, string warning)
{
  if (_level > 1)
  {
    _print("\033[1m\033[33m", fName, "[WARNING] " + warning);
  }
}

//Log error.
void Log::error(string fName, string error)
{
  if (_level > 0)
  {
    _print("\033[1m\033[31m", fName, "[ERROR] " + error);
  }
}

//Print to console.
void Log::_print(string color, string fName, string message)
{
  cout << color << "[" << _modemName << "_LIB::" << fName << "]" << message << "\033[0m" << endl;
}
