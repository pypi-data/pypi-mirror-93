"""
Ringbeller IoT - Cellular library Python bindings
"""

# includes
import ctypes
import os

# globals
modem = False


def initialize(verbose, debug, serial_port, audio_device):
    """
    Initialize modem library
    verbose: Log verbose level (0-4)
    debug: Debug simulation is enabled if true
    serial_port: Serial port name
    audio_device: (Optional) Audio input/output device name
    returns 1 if modem initialized successfully
    """
    global modem
    modem = ctypes.CDLL(os.path.dirname(__file__) + "/src/lib/libmodemwrapper.so")
    modem.initialize.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
    modem.initialize.restype = ctypes.c_int
    return modem.initialize(verbose, debug, serial_port.encode('ascii'),
	                        audio_device.encode('ascii'))


def on():
    """
    Turn on modem
    returns 1 if modem turned on successfully
    """
    modem.on.restype = ctypes.c_int
    return modem.on()


def off():
    """
    Turn off modem
    """
    modem.off.restype = ctypes.c_int
    modem.off()


def restart():
    """
    Restart modem
    returns 1 if modem restarted successfully
    """
    modem.restart.restype = ctypes.c_int
    return modem.restart()


def connect():
    """
    Connect to modem
    returns 1 if connected successfully
    """
    modem.connect.restype = ctypes.c_int
    return modem.connect()


def disconnect():
    """
    Disconnect from modem
    """
    modem.disconnect.restype = ctypes.c_int
    modem.disconnect()


def configure():
    """
    Configure modem
    returns 1 if modem configured successfully
    """
    modem.configure.restype = ctypes.c_int
    return modem.configure()


def send_sms(number, message):
    """
    Send SMS
    number: Number to send SMS to
    message: SMS message to be sent
    returns 1 if SMS successfully sent, 0 if otherwise
    """
    modem.sendSMS.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    modem.sendSMS.restype = ctypes.c_int
    return modem.sendSMS(number.encode('ascii'), message.encode('ascii'))


def receive_sms():
    """
    Receive SMS
    returns retrieved unread message if any, FALSE otherwise
    """
    modem.receiveSMS.restype = ctypes.c_char_p
    result = modem.receiveSMS()
    if result:
        return result.decode('ascii')
    return False


def place_voice_call(number):
    """
    Place voice call
    number: Number to place voice call to
    returns 1 if voice call placed
    """
    modem.placeVoiceCall.argtypes = [ctypes.c_char_p]
    modem.placeVoiceCall.restype = ctypes.c_int
    return modem.placeVoiceCall(number.encode('ascii'))


def receive_voice_call():
    """
    Receive voice call
    returns 1 if voice call received
    """
    modem.receiveVoiceCall.restype = ctypes.c_int
    return modem.receiveVoiceCall()


def get_call_status():
    """
    Get call status
    returns 1 if call ended, 0 otherwise
    """
    modem.getCallStatus.restype = ctypes.c_int
    return modem.getCallStatus()


def end_call():
    """
    Hang up active voice call
    """
    modem.endCall()


def begin_audio_playback(playback_file):
    """
    Begin playing audio to voice call
    playback_file: Audio output playback file name
    """
    modem.beginAudioPlayback.argtypes = [ctypes.c_char_p]
    modem.beginAudioPlayback.restype = ctypes.c_int
    modem.beginAudioPlayback(playback_file.encode('ascii'))


def wait_for_audio_playback():
    """
    Wait for voice-call audio-playback to end
    """
    modem.waitForAudioPlayback()


def end_audio_playback():
    """
    End playing audio to voice call
    """
    modem.endAudioPlayback()


def begin_audio_recording(record_file):
    """
    Begin recording audio from voice call
    record_file: Audio input recording file name
    """
    modem.beginAudioRecording.argtypes = [ctypes.c_char_p]
    modem.beginAudioRecording.restype = ctypes.c_int
    modem.beginAudioRecording(record_file.encode('ascii'))


def end_audio_recording():
    """
    End recording audio from voice call
    """
    modem.endAudioRecording()


def send_mms(recipient, cc, bcc, title, attachment, protocol, apn, username, password,
            authentication, mmsc, proxy, port):
    """
    Send MMS
    recipient: MMS recipient
    cc: MMS cc recipient
    bcc: MMS bcc recipient
    title: Title of MMS
    attachment: Name of attachment-file to be sent
    protocol: Protocol (MMS configuration settings)
    apn: APN (MMS configuration settings)
    username: Username (MMS configuration settings)
    password: Password (MMS configuration settings)
    authentication: Authentication (MMS configuration settings)
    mmsc: Mmsc (MMS configuration settings)
    proxy: Proxy (MMS configuration settings)
    port: Port (MMS configuration settings)
    returns 1 if MMS successfully sent, 0 if otherwise
    """
    modem.sendMMS.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
	                        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
	                        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
							ctypes.c_int]
    modem.sendMMS.restype = ctypes.c_int
    return modem.sendMMS(recipient.encode('ascii'), cc.encode('ascii'), bcc.encode('ascii'),
	                    title.encode('ascii'), attachment.encode('ascii'), protocol,
						apn.encode('ascii'), username.encode('ascii'), password.encode('ascii'),
                        authentication, mmsc.encode('ascii'), proxy.encode('ascii'), port)


def get_keypad_input(length, audio_file):
    """
    Get keypad input
    length: (Optional) Length of desired keypad input
    audio_file: (Optional) Audio file to be played
    returns IVR keypad input if any, False otherwise
    """
    modem.getKeypadInput.argtypes = [ctypes.c_int, ctypes.c_char_p]
    modem.getKeypadInput.restype = ctypes.c_char_p
    result = modem.getKeypadInput(length, audio_file.encode('ascii'))
    if result:
        return result.decode('ascii')
    return False
