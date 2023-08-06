/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef EC25_H
#define EC25_H

/*********************Includes*************************/
#include "modem.h"
/******************************************************/

// Define modem name.
#define MODEM_NAME "EC25"

// EC25 modem class.
class EC25 : public Modem
{
public:
    /** Constructor */
    EC25()
    {
        //Initialize logger with modem name.
        _log = Log(MODEM_NAME);
    }
};

#endif // EC25_H