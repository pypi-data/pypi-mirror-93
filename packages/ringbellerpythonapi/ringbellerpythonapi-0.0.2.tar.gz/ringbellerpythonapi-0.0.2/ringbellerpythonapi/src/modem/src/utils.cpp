/*
This file is part of the Utils communications library for Raspberry Pi
*/
#include "../inc/utils.h"

//Convert escaped characters.
string Utils::escaped(const string &input)
{
  string output;
  output.reserve(input.size());
  for (const char c : input)
  {
    switch (c)
    {
    case '\r':
      output += "\\r";
      break;
    case '\n':
      output += "\\n";
      break;
    case '\u001A':
      output += "CTRL-Z";
      break;
    default:
      output += c;
      break;
    }
  }

  return output;
}
