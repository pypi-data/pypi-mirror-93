#ifdef _MSC_VER
    #define EXPORT_SYMBOL __declspec(dllexport)
#else
    #define EXPORT_SYMBOL
#endif

#include "../modem/inc/modem.h"


#ifdef __cplusplus
extern "C"
{
#endif

	/** Initialize modem library
		@param verbose		Log verbose level (0-4)
		@param debug		Debug simulation is enabled if true
		@param serialPort	Serial port name
		@param audioDevice	(Optional) Audio input/output device name
		@return				Returns 1 if modem initialized successfully
	 */
	EXPORT_SYMBOL int initialize(int verbose, int debug, const char *serialPort, const char *audioDevice = NULL);

	/** Turn on modem
		@return		Returns 1 if modem turned on successfully
	 */
	EXPORT_SYMBOL int on();

	/** Turn off modem */
	EXPORT_SYMBOL void off();

	/** Restart modem
		@return		Returns 1 if modem restarted successfully
	 */
	EXPORT_SYMBOL int restart();

	/** Connect to modem
		@return		Returns 1 if connected successfully
	 */
	EXPORT_SYMBOL int connect();

	/** Disconnect from modem */
	EXPORT_SYMBOL void disconnect();

	/** Configure modem
		@return		Returns 1 if modem configured successfully
	 */
	EXPORT_SYMBOL int configure();

	/** Send SMS
		@param number	Number to send SMS to
		@param message	SMS message to be sent
		@return			Returns 1 if SMS successfully sent, 0 if otherwise
	 */
	EXPORT_SYMBOL int sendSMS(const char *number, const char *message);

	/** Receive SMS
		@return			Returns retrieved unread message
	 */
	EXPORT_SYMBOL char *receiveSMS();

	/** Place voice call
		@param number	Number to place voice call to
		@return			Returns 1 if voice call placed
	 */
	EXPORT_SYMBOL int placeVoiceCall(const char *number);

	/** Receive voice call
		@return			Returns 1 if voice call received
	 */
	EXPORT_SYMBOL int receiveVoiceCall();

	/** Get call status
		@return			Returns 1 if call ended, 0 otherwise
	*/
	EXPORT_SYMBOL int getCallStatus();

	/** Hang up active voice call */
	EXPORT_SYMBOL void endCall();

	/** Begin playing audio to voice call
		@param playbackFile	Audio output playback file name
	 */
	EXPORT_SYMBOL void beginAudioPlayback(const char *playbackFile);

	/** Wait for voice-call audio-playback to end */
	EXPORT_SYMBOL void waitForAudioPlayback();

	/** End playing audio to voice call */
	EXPORT_SYMBOL void endAudioPlayback();

	/** Begin recording audio from voice call
		@param recordFile	Audio input recording file name
	 */
	EXPORT_SYMBOL void beginAudioRecording(const char *recordFile);

	/** End recording audio from voice call */
	EXPORT_SYMBOL void endAudioRecording();

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
	EXPORT_SYMBOL int sendMMS(const char *recipient, const char *cc, const char *bcc, const char *title, const char *attachment,
							  int protocol, const char *apn, const char *username, const char *password, int authentication,
							  const char *mmsc, const char *proxy, int port);

	/** Get keypad input
		@param length		(Optional) Length of desired keypad input
		@param audioFile	(Optional) Audio file to be played
		@return				Returns IVR keypad input if any, NULL otherwise
	 */
	EXPORT_SYMBOL const char *getKeypadInput(int length = 0, const char *audioFile = NULL);

#ifdef __cplusplus
}
#endif