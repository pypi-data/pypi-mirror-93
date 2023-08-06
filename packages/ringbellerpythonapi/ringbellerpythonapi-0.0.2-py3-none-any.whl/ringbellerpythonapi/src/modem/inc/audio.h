/*
This file is part of the modem communications library for Raspberry Pi
*/
#ifndef AUDIO_H
#define AUDIO_H

/*********************Includes*************************/
#include <alsa/asoundlib.h>
#include <sndfile.h>
#include "log.h"
/******************************************************/

// Define audio parameters struct.
typedef struct
{
	pthread_t id;		   //Thread id
	string device;		   //Audio device
	string file;		   //Audio file
	volatile bool isEnded; //True if audio ended
	string error;		   //Audio error
} AudioParam;

// Modem library audio class.
class Audio
{
public:
	AudioParam playbackParameters; //Audio playback parameters variable
	AudioParam recordParameters;   //Audio recording parameters variable

	/** Configure audio parameters
			@param simulation	Sets audio simulation value
			@param device		Sets audio input/output device name
		 */
	void configure(bool simulation, string device = "");

	/** Get audio device name
			@return	Returns audio input/output device name
		 */
	string getDevice();

	/** Audio output playback thread */
	static void *playback_thread(void *playbackParams);

	/** Audio input recording thread */
	static void *record_thread(void *recordParams);

private:
	static bool _isSimulation; //Debug simulation on/off
	string _device = "";	   //Audio device sound card name
	static Log _log;		   //Log instance
};

#endif // AUDIO_H