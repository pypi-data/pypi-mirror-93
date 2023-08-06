/*
This file is part of the Hardware communications library for Raspberry Pi
*/
#include "../inc/hardware.h"

//Initialize GPIO pins.
bool Hardware::init()
{
    // Set log precursor value.
    const string fName = "Hardware::init";

    _log.debug(fName, "Begin initializing GPIO pins.");

    // If not debug simulation.
    if (!_isSimulation)
    {
        // Set up wiringpi.
        if (wiringPiSetup() == -1)
        {
            // Wiringpi failed to set up.
            _log.warning(fName, "Failed to set up Wiringpi.");
            return false;
        }
        else
        {
            // Set user-led pin GPIO27 as output.
            pinMode(PIN_USER_LED, OUTPUT);
            // Set hat-power-off pin GPIO26 as output (active low).
            pinMode(PIN_HAT_PWR_OFF, OUTPUT);

            _log.debug(fName, "GPIO pins initialized.");

            // Check if modem is on.
            if (digitalRead(PIN_HAT_PWR_OFF) == LOW)
            {
                _isModemPowerUp = true;
            }
            else
            {
                _log.warning(fName, "Modem not powered up.");
            }
            return true;
        }
    }
    else
    {
        return true;
    }
}

//Power up modem.
void Hardware::powerUp()
{
    // Set log precursor value.
    const string fName = "Hardware::powerUp";

    _log.debug(fName, "Begin powering up modem.");

    // If modem is not powered up.
    if (!_isModemPowerUp)
    {
        // If not debug simulation.
        if (!_isSimulation)
        {
            // Set hat-power-off pin LOW to power modem up.
            digitalWrite(PIN_HAT_PWR_OFF, LOW);

            // Wait for modem to turn on.
            delay(MODEM_ON_DELAY);
        }

        // Set modem-powered-up variable to true.
        _isModemPowerUp = true;

        _log.debug(fName, "Modem powered up.");
    }
    else
    {
        _log.debug(fName, "Modem power is up.");
    }
}

//Power down modem.
void Hardware::powerDown()
{
    // Set log precursor value.
    const string fName = "Hardware::powerDown";

    _log.debug(fName, "Begin powering down modem.");

    // If not debug simulation.
    if (!_isSimulation)
    {
        // Wait for modem to shut down.
        delay(MODEM_OFF_DELAY);

        // Set hat-power-off pin HIGH to turn modem OFF.
        digitalWrite(PIN_HAT_PWR_OFF, HIGH);
    }

    // Set modem-powered-up variable to false.
    _isModemPowerUp = false;

    _log.debug(fName, "Modem powered down.");
}

//Get modem power status.
bool Hardware::getPowerStatus()
{
    return _isModemPowerUp;
}

//Set simulation debug value.
void Hardware::setSimulation(bool simulation)
{
    _isSimulation = simulation;

    string value = _isSimulation ? "true" : "false";
    _log.debug("Hardware::setSimulation", "Hardware simulation debug value set to <" + value + ">.");
}
