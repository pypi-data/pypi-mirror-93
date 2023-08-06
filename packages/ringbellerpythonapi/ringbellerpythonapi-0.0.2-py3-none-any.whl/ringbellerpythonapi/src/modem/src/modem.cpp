/*
This file is part of the modem communications library for Raspberry Pi
*/
#include "../inc/modem.h"

//Constructor.
Modem::Modem() {}

//Deconstructor.
Modem::~Modem()
{
  // Disconnect from modem.
  disconnect();

  _log.debug("~Modem", "Modem library deconstructed.");
}

//Initialize modem library.
bool Modem::initialize(int verbose, bool simulation, string serialPort, string audioDevice)
{
  // Set log precursor value.
  const string fName = "initialize";

  // Set verbose logging level.
  _log.setLevel(verbose);

  _log.debug(fName, "Begin initializing modem library.");

  // Set device-gpio simulation value.
  _hardware.setSimulation(simulation);

  // Configure modem-communication settings.
  _comms.configure(simulation, serialPort);

  // Configure audio input/output device.
  _audio.configure(simulation, audioDevice);

  // Initialize hardware.
  if (_hardware.init())
  {
    _log.info(fName, "Modem library initialized.");

    return true;
  }
  else
  {
    _log.error(fName, "Error initializing modem library");

    return false;
  }
}

//Turn modem on.
bool Modem::on()
{
  // Set log precursor value.
  const string fName = "on";

  _log.debug(fName, "Begin turning on modem.");

  // Power up modem.
  _hardware.powerUp();

  _log.info(fName, "Modem turned on.");

  // Connect to modem.
  return connect();
}

//Turn modem off.
void Modem::off()
{
  // Set log precursor value.
  const string fName = "off";

  _log.debug(fName, "Begin turning off modem.");

  // If modem power is up.
  if (_hardware.getPowerStatus())
  {
    // Shut modem down.
    _comms.sendATCommand(AT_SHUT_DOWN);

    // Power down modem.
    _hardware.powerDown();

    _log.info(fName, "Modem turned off.");
  }
  else
  {
    _log.info(fName, "Modem power is down.");
  }
}

//Restart modem.
bool Modem::restart()
{
  off(); // Off modem.

  return on(); // On modem.
}

//Connect to modem.
bool Modem::connect()
{
  // Set log precursor value.
  const string fName = "connect";

  _log.debug(fName, "Begin connecting to modem.");

  // Initialize modem communication & ping modem.
  if (_comms.init() && _comms.sendATCommand(AT_PING, AT_RESPONSE_OK))
  {
    _log.info(fName, "Connected to modem.");

    return true;
  }
  else
  {
    _log.error(fName, "Failed to connect to modem.");

    return false;
  }
}

//Disconnect from modem.
void Modem::disconnect()
{
  // Set log precursor value.
  const string fName = "disconnect";

  _log.debug(fName, "Begin disconnecting from modem.");

  // Close modem library communications.
  _comms.close();

  _log.info(fName, "Disconnected from modem.");
}

//Configure modem.
bool Modem::configure()
{
  // Set log precursor value.
  const string fName = "configure";

  _log.debug(fName, "Begin configuring modem.");

  // If modem power is down.
  if (!_hardware.getPowerStatus())
  {
    // Turn modem on.
    on();
  }

  // Initialize configure-attempts variable.
  int attempt = 1;

  // While modem has not been configured.
  while (true)
  {
    // If maximum attempts reached.
    if (attempt > MODEM_CONFIGURE_MAX_ATTEMPTS)
    {
      // Failed to configure modem.
      _log.error(fName, "Failed to configure modem.");

      return false;
      break;
    }

    _log.debug(fName, "Attempt " + to_string(attempt++) + ":");

    // Configure modem.
    if (_comms.sendATCommand(AT_FACTORY_SETTINGS, AT_RESPONSE_OK)       // Set factory settings (See AT manual: 2.10 - AT&F [page 17]).
        && _comms.sendATCommand(AT_ECHO_MODE, AT_ECHO_RESPONSE_OK)      // Set command echo mode to OFF (See AT manual: 2.16 - ATE [page 22]).
        && _comms.sendATCommand(AT_UAC_ENABLE_DEVICE, AT_RESPONSE_OK)   // Enable UAC audio device (See UAC application note: 4.1 - AT+QCFG [page 10]).
        && _comms.sendATCommand(AT_UAC_ENABLE_FUNCTION, AT_RESPONSE_OK) // Enable UAC audio function (See UAC application note: 3 - AT+QPCMV [page 8]).
        && _comms.sendATCommand(AT_DTMF_ENABLE, AT_RESPONSE_OK)         // Enable DTMF detection (See AT manual: 12.13 - AT+QTONEDET [page 200]).
        && _comms.sendATCommand(AT_PING, AT_RESPONSE_OK))               // Ping modem.
    {
      // Modem configured.
      _log.info(fName, "Modem configured.");

      return true;
      break;
    }
    // If failed to configure modem.
    else
    {
      // Restart modem.
      restart();
    }
  }
}

//Send SMS.
bool Modem::sendSMS(string number, string message)
{
  // Set log precursor value.
  const string fName = "sendSMS";

  _log.debug(fName, "Begin sending <" + number + "> an SMS: <" + message + ">.");

  // Set SMS format to text mode (See AT manual: 9.2 - AT+CMGF [page 117]).
  _comms.sendATCommand(AT_SMS_FORMAT, AT_RESPONSE_OK);

  // Set character-set to GSM (See AT manual: 2.24 - AT+CSCS [page 28]).
  _comms.sendATCommand(AT_SMS_CHARACTER_SET, AT_RESPONSE_OK);

  // Send SMS (See AT manual: 9.8 - AT+CMGS [page 129]).
  string command = AT_SMS_SEND + number + "\"\r\n";
  _comms.sendATCommand(command, "\r\n> "); // Send phone number command.
  _comms.sendATCommand(message);           // Send message.

  // Send message delimiter CTRL-Z (See AT manual: 9.8 - AT+CMGS Example [page 130]).
  if (_comms.sendATCommand(AT_SMS_DELIMITER, AT_SMS_RESPONSE_OK))
  {
    _log.info(fName, "SMS with message <" + message + "> sent to <" + number + ">.");
    return true;
  }
  else
  {
    _log.error(fName, "SMS not sent.");
    return false;
  }
}

//Receive SMS.
bool Modem::receiveSMS(string &sms)
{
  // Set log precursor value.
  const string fName = "receiveSMS";

  _log.debug(fName, "Begin receiving unread SMS.");

  // Set SMS parameter (See AT manual: 9.15 - AT+CSDH [page 140]).
  _comms.sendATCommand(AT_SMS_PARAMETERS, AT_RESPONSE_OK);

  // Set SMS format to text mode (See AT manual: 9.2 - AT+CMGF [page 117]).
  _comms.sendATCommand(AT_SMS_FORMAT, AT_RESPONSE_OK);

  // Retrieve unread SMS (See AT manual: 9.6 - AT+CMGL [page 122]).
  _comms.sendATCommand(AT_SMS_READ);

  // Read response.
  string response = _comms.readATResponse();

  // If no reponse from modem.
  if (response == "NO RESPONSE")
  {
    _log.error(fName, "SMS not received.");

    return false;
  }
  else
  {
    // Set sms variable to response.
    sms = response;

    // If no unread messages retrieved.
    if (sms == "\r\n")
    {
      // Set sms variable to NONE.
      sms = "NONE";

      _log.info(fName, "No unread messages.");
    }
    else
    {
      _log.info(fName, "Unread SMS <" + _utils.escaped(sms) + "> received.");

      // Delete read messages (See AT manual: 9.5 - AT+CMGD [page 121]).
      if (_comms.sendATCommand(AT_SMS_DELETE, AT_RESPONSE_OK))
      {
        _log.debug(fName, "Read messages deleted.");
      }
      else
      {
        _log.warning(fName, "Failed to delete read messages.");
      }
    }

    return true;
  }
}

//Place voice call.
bool Modem::placeVoiceCall(string number)
{
  // Set log precursor value.
  const string fName = "placeVoiceCall";

  _log.debug(fName, "Begin placing voice call to <" + number + ">.");

  // Place outgoing call (See AT manual: 7.2 - ATD [page 90]).
  if (_comms.sendATCommand(AT_CALL_PLACE + number + ";\r\n", AT_RESPONSE_OK))
  {
    _log.info(fName, "Outgoing call placed.");
    return true;
  }
  else
  {
    _log.error(fName, "Voice call not placed.");
    return false;
  }
}

//Receive voice call.
bool Modem::receiveVoiceCall()
{
  // Set log precursor value.
  const string fName = "receiveVoiceCall";

  _log.debug(fName, "Begin receiving voice call.");

  // Answer incoming call (See AT manual: 7.1 - ATA [page 89]).
  if (_comms.sendATCommand(AT_CALL_ANSWER, AT_RESPONSE_OK))
  {
    _log.info(fName, "Incoming call answered.");
    return true;
  }
  else
  {
    _log.error(fName, "Voice call not received.");
    return false;
  }
}

//Get call status.
void Modem::getCallStatus(bool &isCallHungUp)
{
  // Set log precursor value.
  const string fName = "getCallStatus";

  // Send check call status AT command (See AT manual: 4.1 - AT+CPAS [page 37]).
  _comms.sendATCommand(AT_CALL_STATUS);

  // Instantiate call-in-progress variable.
  static string inProgress;

  // If call still in progress.
  if (_comms.readATResponse() == AT_CALL_IN_PROGRESS_RESPONSE)
  {
    // Update call-in-progress variable.
    inProgress += ".";

    _log.info(fName, "Call in progress" + inProgress);
  }
  else
  {
    // Reset call-in-progress variable.
    inProgress = "";

    // Set call-hung-up variable to true.
    isCallHungUp = true;

    _log.info(fName, "Call ended.");
  }
}

//End active voice call.
void Modem::endCall()
{
  // Set log precursor value.
  const string fName = "endCall";

  _log.debug(fName, "Ending active voice call.");

  // Hang up call (See AT manual: 7.3 - ATH [page 92]).
  if (_comms.sendATCommand(AT_CALL_HANGUP, AT_RESPONSE_OK))
  {
    _log.debug(fName, "Call hung up.");
  }
  else
  {
    _log.warning(fName, "Failed to hang up call.");
  }
}

//Begin playing audio to voice-call.
void Modem::beginAudioPlayback(string file)
{
  // Set log precursor value.
  const string fName = "beginAudioPlayback";

  _log.debug(fName, "Beginning audio playback.");

  // Set audio output device name.
  _audio.playbackParameters.device = _audio.getDevice();

  // Set audio playback file name.
  _audio.playbackParameters.file = file;

  // Set audio-playback-ended to false.
  _audio.playbackParameters.isEnded = false;

  // Initialize audio-playback-error variable.
  _audio.playbackParameters.error = "";

  // Create audio playback thread.
  (void)pthread_create(&_audio.playbackParameters.id, 0, _audio.playback_thread, &_audio.playbackParameters);

  _log.debug(fName, "Audio playback <" + (string)file + "> begun.");
}

//Wait for voice-call audio-playback to end.
void Modem::waitForAudioPlayback()
{
  // Set log precursor value.
  const string fName = "waitForAudioPlayback";

  _log.debug(fName, "Waiting for audio playback to end.");

  // Instantiate thread-return-ok variable.
  void *isThreadReturnOk;

  // Terminate audio playback thread.
  (void)pthread_join(_audio.playbackParameters.id, &isThreadReturnOk);

  // If error playing output audio.
  if (!(bool)isThreadReturnOk)
  {
    _log.warning(fName, "Error playing audio output to voice call: " + _audio.playbackParameters.error);
  }
  else
  {
    _log.debug(fName, "Audio playback ended.");
  }
}

//End playing audio to voice-call.
void Modem::endAudioPlayback()
{
  // Set log precursor value.
  const string fName = "endAudioPlayback";

  _log.debug(fName, "Ending audio playback.");

  // Set playback-ended variable to true.
  _audio.playbackParameters.isEnded = true;

  // Wait for audio playback to end.
  waitForAudioPlayback();
}

//Start recording audio from voice call.
void Modem::beginAudioRecording(string file)
{
  // Set log precursor value.
  const string fName = "beginAudioRecording";

  _log.debug(fName, "Beginning audio recording.");

  // Set audio input device name.
  _audio.recordParameters.device = _audio.getDevice();

  // Set audio recording file name.
  _audio.recordParameters.file = file;

  // Set audio-record-ended to false.
  _audio.recordParameters.isEnded = false;

  // Initialize audio-record-error variable.
  _audio.recordParameters.error = "";

  // Create audio recording thread.
  (void)pthread_create(&_audio.recordParameters.id, 0, _audio.record_thread, &_audio.recordParameters);

  _log.debug(fName, "Audio recording <" + file + "> begun.");
}

//Stop recording audio from voice call.
void Modem::endAudioRecording()
{
  // Set log precursor value.
  const string fName = "stopRecord";

  _log.debug(fName, "Ending audio recording.");

  // Set record-ended variable to true.
  _audio.recordParameters.isEnded = true;

  // Instantiate thread-return-ok variable.
  void *isThreadReturnOk;

  // Terminate audio recording thread.
  (void)pthread_join(_audio.recordParameters.id, &isThreadReturnOk);

  // If audio successfully recorded.
  if ((bool)isThreadReturnOk)
  {
    _log.debug(fName, "Audio recording from voice call ended.");
  }
  else
  {
    _log.warning(fName, "Error recording audio from voice call: " + _audio.recordParameters.error);
  }
}

//Send MMS.
bool Modem::sendMMS(MmsConfiguration mmsConfig, string recipient, string cc, string bcc, string title, string attachmentFile)
{
  // Set log precursor value.
  const string fName = "sendMMS";

  _log.debug(fName, "Begin sending MMS to <" + recipient + ">.");

  // Set MMS configuration settings.
  _comms.mmsConfig = mmsConfig;

  // Configure TCP/IP context parameters (See TCP/IP application note: 2.1.1 - AT+QICSGP [page 10]).
  _comms.sendATCommand(AT_MMS_CONFIGURE_CONTEXT + to_string(_comms.mmsConfig.protocol) + ",\"" + _comms.mmsConfig.apn + "\",\"" + _comms.mmsConfig.username + "\",\"" + _comms.mmsConfig.password + "\"," + to_string(_comms.mmsConfig.authentication) + "\r\n", AT_RESPONSE_OK);

  // Activate PDP context (See TCP/IP application note: 2.1.2 - AT+QIACT [page 11]).
  _comms.sendATCommand(AT_MMS_ACTIVATE_CONTEXT, AT_RESPONSE_OK);

  // Configure MMS parameters (See MMS AT manual: 2.1 - AT+QMMSCFG [page 7]).
  _comms.sendATCommand(AT_MMS_CONFIGURE_CONTEXT_ID, AT_RESPONSE_OK);
  _comms.sendATCommand(AT_MMS_CONFIGURE_MMSC + _comms.mmsConfig.mmsc + "\"\r\n", AT_RESPONSE_OK);
  _comms.sendATCommand(AT_MMS_CONFIGURE_PROXY + _comms.mmsConfig.proxy + "\"," + to_string(_comms.mmsConfig.port) + "\r\n", AT_RESPONSE_OK);
  _comms.sendATCommand(AT_MMS_CONFIGURE_SENDPARAM, AT_RESPONSE_OK);
  _comms.sendATCommand(AT_MMS_CONFIGURE_CHARSET, AT_RESPONSE_OK);

  // Add MMS recipient (See MMS AT manual: 2.2.1 - AT+QMMSEDIT=1 [page 11]).
  _comms.sendATCommand(AT_MMS_ADD_RECIPIENT + recipient + "\"\r\n", AT_RESPONSE_OK);

  if (cc != "")
  {
    // Add MMS CC recipient (See MMS AT manual: 2.2.2 - AT+QMMSEDIT=2 [page 12]).
    if (_comms.sendATCommand(AT_MMS_ADD_CC + cc + "\"\r\n", AT_RESPONSE_OK))
    {
      _log.debug(fName, "MMS CC recipient <" + cc + "> added.");
    }
  }

  if (bcc != "")
  {
    // Add MMS BCC recipient (See MMS AT manual: 2.2.2 - AT+QMMSEDIT=3 [page 12]).
    if (_comms.sendATCommand(AT_MMS_ADD_BCC + bcc + "\"\r\n", AT_RESPONSE_OK))
    {
      _log.debug(fName, "MMS BCC recipient <" + bcc + "> added.");
    }
  }

  if (title != "")
  {
    // Edit MMS title (See MMS AT manual: 2.2.3 - AT+QMMSEDIT=4 [page 12]).
    if (_comms.sendATCommand(AT_MMS_EDIT_TITLE + title + "\"\r\n", AT_RESPONSE_OK))
    {
      _log.debug(fName, "MMS title <" + title + "> edited.");
    }
  }

  // Declare attachment-file-name variable;
  string attachmentFileName;

  if (attachmentFile != "")
  {
    // Upload file to storage.
    _comms.uploadFile(attachmentFile, attachmentFileName);

    // Add MMS attachment (See MMS AT manual: 2.2.4 - AT+QMMSEDIT=5 [page 13]).
    if (_comms.sendATCommand(AT_MMS_ADD_ATTACHMENT + attachmentFileName + "\"\r\n", AT_RESPONSE_OK))
    {
      _log.debug(fName, "MMS attachment <" + attachmentFile + "> added.");
    }
  }

  // Send MMS (See MMS AT manual: 2.3 - AT+QMMSEND [page 15]).
  bool isSentSuccess = _comms.sendATCommand(AT_MMS_SEND, AT_MMS_RESPONSE_OK);

  // Clear MMS content (See MMS AT manual: 2.2.5 - AT+QMMSEDIT=0 [page 14]).
  _comms.sendATCommand(AT_MMS_CLEAR, AT_RESPONSE_OK);

  // Deactivate PDP context (See TCP/IP application note: 2.1.3 - AT+QIDEACT [page 12]).
  _comms.sendATCommand(AT_MMS_DEACTIVATE_CONTEXT, AT_RESPONSE_OK);

  if (attachmentFile != "")
  {
    // Delete attachment file from storage (See File application note: 2.3 - AT+QFDEL [page 11]).
    if (_comms.sendATCommand(AT_FILE_DELETE + attachmentFileName + "\"\r\n", AT_RESPONSE_OK))
    {
      _log.debug(fName, "Attachment file <" + attachmentFile + "> deleted from storage.");
    }
  }

  if (isSentSuccess)
  {
    _log.info(fName, "MMS sent to <" + recipient + ">.");
    return true;
  }
  else
  {
    _log.error(fName, "MMS not sent.");
    return false;
  }
}

//Get keypad input.
bool Modem::getKeypadInput(string &input, int length, string audioFile)
{
  // Set log precursor value.
  const string fName = "getKeypadInput";

  _log.debug(fName, "Begin reading <" + to_string(length) + "> digit keypad input.");

  if (audioFile != "")
  {
    // Begin playing audio.
    beginAudioPlayback(audioFile);

    // Wait for audio playback.
    waitForAudioPlayback();
  }

  // Initialize keypad-input-success variable.
  bool success = true;

  // For each key to be read.
  for (int i = 0; i < length; i++)
  {
    // Instantiate input-key variable.
    char key;

    // Read keypad input.
    if (_comms.readKeypadInput(key, 20000))
    {
      // If successful, append to input string.
      input.push_back(key);
    }
    else
    {
      // If unsuccessful, abort getting keypad input.
      success = false;
      break;
    }
  }

  if (success)
  {
    _log.debug(fName, "Keypad input <" + input + "> received.");
  }
  else
  {
    _log.warning(fName, "Failed to receive <" + to_string(length) + "> digit keypad input.");
  }

  return success;
}
