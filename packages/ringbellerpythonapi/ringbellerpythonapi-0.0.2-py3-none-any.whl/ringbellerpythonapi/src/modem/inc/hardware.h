/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef HARDWARE_H
#define HARDWARE_H

/*********************Includes*************************/
#include <string>
#include <wiringPi.h>
#include "log.h"
/******************************************************/

#define MODEM_OFF_DELAY 3000 // Define time to wait before powering down modem
#define MODEM_ON_DELAY 15000 // Define time to wait after powering up modem

// Disable Raspberry Pi GPIO hardware simulation.
#define HARDWARE_SIMULATION false

// Define user-led pin GPIO27(pin 2 in wiringpi)
#define PIN_USER_LED 2
// Define hat-power-off pin GPIO26(pin 25 in wiringpi)
#define PIN_HAT_PWR_OFF 25

// Modem library hardware class.
class Hardware
{
public:
    /** Initialize GPIO pins
			@return			Returns true if successful,
							false if otherwise
		 */
    bool init();

    /** Apply power to modem */
    void powerUp();

    /** Cut power to modem */
    void powerDown();

    /** Get modem power status
			@return			Returns true if power applied,
							false if power not applied.
		 */
    bool getPowerStatus();

    /** Set GPIO hardware simulation
			@param simulation	Sets simulation according to flag
		 */
    void setSimulation(bool simulation);

private:
    bool _isModemPowerUp = false;             //True if modem is powered up
    bool _isSimulation = HARDWARE_SIMULATION; //Debug simulation on/off
    Log _log;                                 //Log instance
};

#endif // HARDWARE_H