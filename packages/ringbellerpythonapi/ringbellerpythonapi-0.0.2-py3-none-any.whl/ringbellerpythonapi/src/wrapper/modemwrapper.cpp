// includes
#include "modemwrapper.h"

// globals
Modem modem;
 
/** Initialize modem library
	@param verbose		Log verbose level (0-4)
	@param debug		Debug simulation is enabled if true
	@param serialPort	Serial port name
	@param audioDevice	(Optional) Audio input/output device name
	@return				Returns 1 if modem initialized successfully
 */
int initialize(int verbose, int debug, const char *serialPort, const char *audioDevice) {
	if (!serialPort)
		return 0;
	if (!audioDevice)
		audioDevice = "";
	if (!modem.initialize(verbose, debug, serialPort, audioDevice))
		return 0;
	return 1;
}

/** Turn on modem
	@return	Returns 1 if modem turned on successfully
 */
int on() {
	if (!modem.on())
		return 0;
	return 1;
}

/** Turn off modem */
void off() {
	modem.off();
}

/** Restart modem
	@return	Returns 1 if modem restarted successfully
 */
int restart() {
	if (!modem.restart())
		return 0;
	return 1;
}

/** Connect to modem
	@return	Returns 1 if connected successfully
 */
int connect() {
	if (!modem.connect())
		return 0;
	return  1;
}

/** Disconnect from modem */
void disconnect() {
	modem.disconnect();
}

/** Configure modem
	@return	Returns 1 if modem configured successfully
 */
int configure() {
	if (!modem.configure())
		return 0;
	return 1;
}

/** Send SMS
	@param number	Number to send SMS to
	@param message	SMS message to be sent
	@return			Returns 1 if SMS successfully sent, 0 if otherwise
 */
int sendSMS(const char *number, const char *message) {
	if (!number || !message)
		return 0;
	if (!modem.sendSMS(number, message))
		return 0;
	return 1;
}

/** Receive SMS
	@return	Returns retrieved unread message
 */
char *receiveSMS() {
	string sms;
	if (!modem.receiveSMS(sms))
		return NULL;
	int len = sms.size();
	if (len<=0)
		return NULL;
	char *response = (char *)malloc(sizeof(char)*(len+1));
	strcpy(response, sms.c_str());
	return response;
}

/** Place voice call
	@param number	Number to place voice call to
	@return			Returns 1 if voice call placed
 */
int placeVoiceCall(const char *number) {
	if (!number)
		return 0;
	if (!modem.placeVoiceCall(number))
		return 0;
	return 1;	
}

/** Receive voice call
	@return	Returns 1 if voice call received
 */
int receiveVoiceCall() {
	if (!modem.receiveVoiceCall())
		return 0;
	return 1;
}

/** Get call status
	@return	Returns 1 if call ended, 0 otherwise
*/
int getCallStatus() {
	bool isCallEnded = false;
	modem.getCallStatus(isCallEnded);
	if (!isCallEnded)
		return 0;
	return 1;
}

/** Hang up active voice call */
void endCall() {
	modem.endCall();
}

/** Begin playing audio to voice call
	@param playbackFile	Audio output playback file name
 */
void beginAudioPlayback(const char *playbackFile) {
	if (!playbackFile)
		return;
	modem.beginAudioPlayback(playbackFile);
}

/** Wait for voice-call audio-playback to end */
void waitForAudioPlayback() {
	modem.waitForAudioPlayback();
}

/** End playing audio to voice call */
void endAudioPlayback() {
	modem.endAudioPlayback();
}

/** Begin recording audio from voice call
	@param recordFile	Audio input recording file name
 */
void beginAudioRecording(const char *recordFile) {
	if (!recordFile)
		return;
	modem.beginAudioRecording(recordFile);
}

/** End recording audio from voice call */
void endAudioRecording() {
	modem.endAudioRecording();
}

/** Send MMS	
	@param recipient		MMS recipient
	@param cc				MMS cc recipient
	@param bcc				MMS bcc recipient
	@param title			Title of MMS
	@param attachment		Name of attachment-file to be sent
	@param protocol			Protocol (MMS configuration settings)
	@param APN				APN (MMS configuration settings)
	@param username			Username (MMS configuration settings)
	@param password			Password (MMS configuration settings)
	@param authentication	Authentication (MMS configuration settings)
	@param mmsc				Mmsc (MMS configuration settings)
	@param proxy			Proxy (MMS configuration settings)
	@param port				Port (MMS configuration settings)
	@return					Returns 1 if MMS successfully sent, 0 if otherwise
 */
int sendMMS(const char *recipient, const char *cc, const char *bcc, const char *title, const char *attachment,
		    int protocol, const char *apn, const char *username, const char *password, int authentication,
		    const char *mmsc, const char *proxy, int port) {
	MmsConfiguration mmsConfig;
	mmsConfig.protocol = protocol;
	mmsConfig.apn = apn;
	mmsConfig.username = username;
	mmsConfig.password = password;
	mmsConfig.authentication = authentication;
	mmsConfig.mmsc = mmsc;
	mmsConfig.proxy = proxy;
	mmsConfig.port = port;
	if (!modem.sendMMS(mmsConfig, recipient, cc, bcc, title, attachment))
		return 0;
	return 1;
}

/** Get keypad input
	@param length		(Optional) Length of desired keypad input
	@param audioFile	(Optional) Audio file to be played
	@return				Returns IVR keypad input if any, NULL otherwise
 */
const char *getKeypadInput(int length, const char *audioFile) {
	if (!audioFile)
		audioFile = "";
	string input;
	if (!modem.getKeypadInput(input, length, audioFile))
		return NULL;
	int len = input.size();
	if (len<=0)
		return NULL;
	char *response = (char *)malloc(sizeof(char)*(len+1));
	strcpy(response, input.c_str());
	return response;
}

