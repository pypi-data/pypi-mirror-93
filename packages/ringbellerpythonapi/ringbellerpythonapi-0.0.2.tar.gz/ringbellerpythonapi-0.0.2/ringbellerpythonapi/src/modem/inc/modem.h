/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef MODEM_H
#define MODEM_H

/*********************Includes*************************/
#include "utils.h"
#include "log.h"
#include "hardware.h"
#include "comms.h"
#include "audio.h"
/******************************************************/

#define MODEM_CONFIGURE_MAX_ATTEMPTS 3 // Set maximum attempts to configuring modem

#define AT_RESPONSE_OK "\r\nOK\r\n"												 // AT OK response
#define AT_FACTORY_SETTINGS "AT&F\r\n"											 // Set modem to factory settings
#define AT_ECHO_MODE "ATE0\r\n"													 // Set Command Echo Mode: OFF
#define AT_ECHO_RESPONSE_OK "ATE0\r\r\nOK\r\n"									 // Echo mode OK response
#define AT_UAC_ENABLE_DEVICE "AT+QCFG=\"usbcfg\",0x2C7C,0x125,1,1,1,1,1,1,1\r\n" // Enable UAC audio device
#define AT_UAC_ENABLE_FUNCTION "AT+QPCMV=1,2\r\n"								 // Enable UAC audio function
#define AT_DTMF_ENABLE "AT+QTONEDET=1\r\n"										 // Enable DTMF detection
#define AT_PING "AT\r\n"														 // Ping modem
#define AT_SHUT_DOWN "AT+QPOWD\r\n"												 // Shut modem down

#define AT_SMS_FORMAT "AT+CMGF=1\r\n"			   // Set SMS format: text mode
#define AT_SMS_CHARACTER_SET "AT+CSCS=\"GSM\"\r\n" // Set character-set: GSM
#define AT_SMS_SEND "AT+CMGS=\""				   // Send SMS
#define AT_SMS_DELIMITER "\u001A"				   // SMS delimeter (Ctrl-Z)
#define AT_SMS_RESPONSE_OK "\r\n+CMGS: "		   // AT SMS OK response
#define AT_SMS_PARAMETERS "AT+CSDH=0\r\n"		   // Do not show SMS header values
#define AT_SMS_READ "AT+CMGL=\"REC UNREAD\"\r\n"   // Read unread SMS
#define AT_SMS_DELETE "AT+CMGD=1,2\r\n"			   // Delete read SMS

#define AT_CALL_PLACE "ATD"									// Place call
#define AT_CALL_ANSWER "ATA\r\n"							// Answer call
#define AT_CALL_HANGUP "ATH\r\n"							// Hang up call
#define AT_CALL_STATUS "AT+CPAS\r\n"						// Check call status
#define AT_CALL_IN_PROGRESS_RESPONSE "\r\n+CPAS: 4\r\n\r\n" // Call in progress response

#define AT_MMS_CONFIGURE_CONTEXT "AT+QICSGP=1,"								  // Configure TCP/IP context parameters
#define AT_MMS_ACTIVATE_CONTEXT "AT+QIACT=1\r\n"							  // Activate PDP context
#define AT_MMS_DEACTIVATE_CONTEXT "AT+QIDEACT=1\r\n"						  // Deactivate PDP context
#define AT_MMS_CONFIGURE_CONTEXT_ID "AT+QMMSCFG=\"contextid\",1\r\n"		  // Configure MMS context ID
#define AT_MMS_CONFIGURE_MMSC "AT+QMMSCFG=\"mmsc\",\""						  // Configure MMSC
#define AT_MMS_CONFIGURE_PROXY "AT+QMMSCFG=\"proxy\",\""					  // Configure MMS proxy
#define AT_MMS_CONFIGURE_SENDPARAM "AT+QMMSCFG=\"sendparam\",6,2,0,0,2,4\r\n" // Configure MMS send param
#define AT_MMS_CONFIGURE_CHARSET "AT+QMMSCFG=\"character\",\"ASCII\"\r\n"	  // Configure MMS character set
#define AT_MMS_ADD_RECIPIENT "AT+QMMSEDIT=1,1,\""							  // Add MMS recipient
#define AT_MMS_ADD_CC "AT+QMMSEDIT=2,1,\""									  // Add MMS CC recipient
#define AT_MMS_ADD_BCC "AT+QMMSEDIT=3,1,\""									  // Add MMS BCC recipient
#define AT_MMS_EDIT_TITLE "AT+QMMSEDIT=4,1,\""								  // Edit MMS title
#define AT_MMS_ADD_ATTACHMENT "AT+QMMSEDIT=5,1,\""							  // Add MMS attachment
#define AT_MMS_CLEAR "AT+QMMSEDIT=0\r\n"									  // Clear MMS content
#define AT_MMS_SEND "AT+QMMSEND=100\r\n"									  // Send MMS
#define AT_MMS_RESPONSE_OK "\r\nOK\r\n\r\n+QMMSEND: 0,200\r\n"				  // AT MMS OK response

#define AT_FILE_DELETE "AT+QFDEL=\"" // Delete file from storage

// Modem class.
class Modem
{
public:
	/** Constructor */
	Modem();

	/** Deconstructor */
	~Modem();

	/** Initialize modem library
			@param verbose		Log verbose level (0-4)
			@param debug		Debug simulation is enabled if true
			@param serialPort	Serial port name
			@param audioDevice	(Optional) Audio input/output device name
		 */
	bool initialize(int verbose, bool debug, string serialPort, string audioDevice = "");

	/** Turn on modem
			@return			Returns true if modem turned on successfully
		 */
	bool on();

	/** Turn off modem */
	void off();

	/** Restart modem
			@return			Returns true if modem restarted successfully
		 */
	bool restart();

	/** Connect to modem
			@return			Returns true if connected successfully
		 */
	bool connect();

	/** Disconnect from modem */
	void disconnect();

	/** Configure modem
			@return			Returns true if modem configured successfully
		 */
	bool configure();

	/** Send SMS
			@param number	Number to send SMS to
			@param message	SMS message to be sent
			@return			Returns true if SMS successfully sent,
							false if otherwise
		 */
	bool sendSMS(string number, string message);

	/** Receive SMS
			@param sms		Stores retrieved unread messages
			@return			Returns true if successful, false otherwise
		 */
	bool receiveSMS(string &sms);

	/** Place voice call
			@param number			Number to place voice call to
			@return					Returns true if voice call placed
		 */
	bool placeVoiceCall(string number);

	/** Receive voice call
			@return					Returns true if voice call received
		 */
	bool receiveVoiceCall();

	/** Get call status
			@param isCallEnded	Stores call status
		 */
	void getCallStatus(bool &isCallEnded);

	/** Hang up active voice call */
	void endCall();

	/** Begin playing audio to voice call
			@param playbackFile	Audio output playback file name
		 */
	void beginAudioPlayback(string playbackFile);

	/** Wait for voice-call audio-playback to end */
	void waitForAudioPlayback();

	/** End playing audio to voice call */
	void endAudioPlayback();

	/** Begin recording audio from voice call
			@param recordFile	Audio input recording file name
		 */
	void beginAudioRecording(string recordFile);

	/** End recording audio from voice call */
	void endAudioRecording();

	/** Send MMS
			@param mmsConfig		MMS configuration settings
			@param recipient		MMS recipient
			@param cc				MMS cc recipient
			@param bcc				MMS bcc recipient
			@param title			Title of MMS
			@param attachment		Name of attachment-file to be sent
			@return					Returns true if MMS successfully sent,
									false if otherwise
		 */
	bool sendMMS(MmsConfiguration mmsConfig, string recipient, string cc, string bcc, string title, string attachment);

	/** Get keypad input
			@param input		Stores IVR keypad input
			@param length		(Optional) Length of desired keypad input
			@param audioFile	(Optional) Audio file to be played
			@return				Returns true if keypad input successfully received
		 */
	bool getKeypadInput(string &input, int length = 1, string audioFile = "");

protected:
	Log _log; //Log instance

private:
	Utils _utils;		//Utilities instance
	Hardware _hardware; //Hardware instance
	Comms _comms;		//Modem communications instance
	Audio _audio;		//Audio instance
};

#endif // MODEM_H