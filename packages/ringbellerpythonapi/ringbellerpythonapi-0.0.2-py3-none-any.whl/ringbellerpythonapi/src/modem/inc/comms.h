/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef COMMS_H
#define COMMS_H

/*********************Includes*************************/
#include <wiringPi.h>
#include <wiringSerial.h>
#include <cstring>
#if __has_include(<filesystem>)
#include <filesystem>
#else
#include <experimental/filesystem>
#endif
#include <unistd.h>
#include "utils.h"
#include "log.h"
/******************************************************/

// Define default baud rate.
#define BAUD_RATE 115200

// Disable modem-communication simulation.
#define COMMS_SIMULATION false
// Define debug simulation delay in milliseconds.
#define SIMULATION_DELAY 100

#define AT_RESPONSE_LEN 5000               // AT command response max length
#define AT_MAX_TRIES 4                     // Max number of AT command tries
#define AT_COMMAND_TIMEOUT (uint16_t)2000  // AT command timeout in milliseconds
#define AT_RESPONSE_TIMEOUT (uint16_t)4000 // AT command response timeout in milliseconds
#define AT_POLL_RESPONSE_DELAY 2           // Poll serial port delay in milliseconds
#define AT_FILE_UPLOAD "AT+QFUPL=\""       // Upload file to storage
#define AT_FILE_CONNECT "\r\nCONNECT\r\n"  // File upload connected
#define AT_FILE_UPLOAD_RESPONSE "+QFUPL: " // File upload response

#define IVR_RESPONSE_LEN 500                        // IVR response max length
#define IVR_KEYPAD_RESPONSE_TIMEOUT (uint16_t)10000 // IVR keypad input response timeout in milliseconds
#define AT_IVR_KEYPAD_RESPONSE "\r\n+QTONEDET: "    // IVR keypad input response

// Define MMS configuration settings struct.
typedef struct
{
    int protocol;
    string apn;
    string username;
    string password;
    int authentication;
    string mmsc;
    string proxy;
    int port;
} MmsConfiguration;

// Modem library communications class.
class Comms
{
public:
    MmsConfiguration mmsConfig; //MMS configuration settings

    /** Configure modem communication
			@param simulation	Sets modem-communication simulation value
			@param serialPort   Sets serial port name
		 */
    void configure(bool simulation, string serialPort);

    /** Get modem connection status
			@return			Returns true if connection established,
							false if otherwise.
		 */
    bool getConnectionStatus();

    /** Initialize modem communication
			@return			Returns true if successful,
							false if otherwise
		 */
    bool init();

    /** Close modem communication */
    void close();

    /** Send AT command
			@param command	Command to be sent
			@param desired	(Optional) Desired return value
			@return			Returns true if successful,
							false if otherwise
		 */
    bool sendATCommand(string command, string desired = "");

    /** Read AT response
			@param desired	(Optional) Response timeout
			@return			Returns AT response message
		 */
    string readATResponse(unsigned int timeout = AT_RESPONSE_TIMEOUT);

    /** Upload file
			@param filePath	File to be sent
			@param fileName	Stores file name
			@return			Returns true if successful,
							false if otherwise
		 */
    bool uploadFile(string filePath, string &fileName);

    /** Read keypad input value
			@param input	Stores keypad input value
			@param timeout	(Optional) Response timeout
			@return			Returns true if successful,
							false if otherwise
		 */
    bool readKeypadInput(char &value, unsigned int timeout = IVR_KEYPAD_RESPONSE_TIMEOUT);

private:
    bool _isConnected = false;             //True if connected to modem
    bool _isSimulation = COMMS_SIMULATION; //Debug simulation on/off
    string _serialPortName;                //Serial port name
    Utils _utils;                          //Utilities instance
    Log _log;                              //Log instance
    int _serialPort;                       //Serial port instance
};

#endif // COMMS_H