/*
This file is part of the Log communications library for Raspberry Pi
*/
#include "../inc/audio.h"

//Instantiate debug simulation static variable.
bool Audio::_isSimulation;

//Instantiate log static variable.
Log Audio::_log;

//Configure audio parameters.
void Audio::configure(bool simulation, string device)
{
  // Set log precursor value.
  const string fName = "Audio::configure";

  // Set audio simulation value.
  _isSimulation = simulation;

  string value = _isSimulation ? "true" : "false";
  _log.debug(fName, "Audio simulation debug value set to <" + value + ">.");

  if (device != "")
  {
    // Set audio input/output device name.
    _device = device;
  }

  _log.debug(fName, "Audio input/output device set to <" + _device + ">.");
}

//Get audio device name.
string Audio::getDevice()
{
  return _device;
}

//Play audio output.
void *Audio::playback_thread(void *playbackParams)
{
  // Set log precursor value.
  const string fName = "Audio::playback_thread";

  // Initialize playback parameters variable.
  AudioParam params = *(AudioParam *)playbackParams;

  // Instantiate audio playback device variables.
  snd_pcm_t *playback_handle;
  snd_pcm_hw_params_t *playback_params;
  snd_pcm_uframes_t playback_frames;
  int dir, err, pcmrc, readcount;

  // Instantiate audio playback info variable.
  SF_INFO playback_sfinfo;

  // Set playback format.
  snd_pcm_format_t playbackFormat = SND_PCM_FORMAT_S16_LE;

  // Initialize audio playback file variable.
  SNDFILE *playbackFile = NULL;

  // Initialize audio playback buffer.
  short *playback_buffer = NULL;

  _log.debug(fName, "Begin playing output audio.");

  // Open audio playback file.
  playbackFile = sf_open(params.file.c_str(), SFM_READ, &playback_sfinfo);

  _log.debug(fName, "Audio playback file <" + params.file + "> opened.");

  if (!_isSimulation)
  {
    // Open PCM audio device in playback mode.
    if ((err = snd_pcm_open(&playback_handle, params.device.c_str(), SND_PCM_STREAM_PLAYBACK, 0)) < 0)
    {
      (*(AudioParam *)playbackParams).error = "Cannot open audio device <" + params.device + ">: " + (string)snd_strerror(err) + ".";
      pthread_exit((void *)false);
    }
    else
    {
      _log.debug(fName, "Audio device <" + params.device + "> opened.");
    }

    // Allocate hardware parameter structure.
    snd_pcm_hw_params_alloca(&playback_params);

    // Fill hardware parameter object.
    snd_pcm_hw_params_any(playback_handle, playback_params);

    // Set access type.
    if ((err = snd_pcm_hw_params_set_access(playback_handle, playback_params, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0)
    {
      _log.warning(fName, "Cannot set access type <" + to_string(SND_PCM_ACCESS_RW_INTERLEAVED) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set sample format.
    if ((err = snd_pcm_hw_params_set_format(playback_handle, playback_params, playbackFormat)) < 0)
    {
      _log.warning(fName, "Cannot set sample format <" + to_string(playbackFormat) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set sample rate.
    if ((err = snd_pcm_hw_params_set_rate(playback_handle, playback_params, playback_sfinfo.samplerate, 0)) < 0)
    {
      _log.warning(fName, "Cannot set sample rate <" + to_string(playback_sfinfo.samplerate) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set channel count.
    if ((err = snd_pcm_hw_params_set_channels(playback_handle, playback_params, playback_sfinfo.channels)) < 0)
    {
      _log.warning(fName, "Cannot set channel count <" + to_string(playback_sfinfo.channels) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Write playback parameters.
    if ((err = snd_pcm_hw_params(playback_handle, playback_params)) < 0)
    {
      _log.warning(fName, "Cannot write playback parameters: " + (string)snd_strerror(err) + ".");
    }

    // Allocate audio playback buffer.
    snd_pcm_hw_params_get_period_size(playback_params, &playback_frames, &dir);
    playback_buffer = (short *)malloc(playback_frames * playback_sfinfo.channels * sizeof(short));

    // Read audio playback frame from file.
    while ((readcount = sf_readf_short(playbackFile, playback_buffer, playback_frames)) > 0)
    {
      // Write audio playback frame to device.
      pcmrc = snd_pcm_writei(playback_handle, playback_buffer, readcount);

      if (pcmrc == -EPIPE)
      {
        _log.warning(fName, "Underrun!");
        snd_pcm_prepare(playback_handle);
      }
      else if (pcmrc < 0)
      {
        _log.warning(fName, "Error writing to PCM device: " + (string)snd_strerror(pcmrc) + ".");
      }
      else if (pcmrc != readcount)
      {
        _log.warning(fName, "PCM write differs from PCM read.");
      }
      if ((*(AudioParam *)playbackParams).isEnded)
      {
        break; // End playback.
      }
    }

    // Free playback buffer.
    free(playback_buffer);

    // Close audio playback device.
    snd_pcm_drain(playback_handle);
    if ((err = snd_pcm_close(playback_handle)) < 0)
    {
      _log.warning(fName, "Cannot close audio playback device: " + (string)snd_strerror(err) + ".");
    }
    else
    {
      _log.debug(fName, "Audio playback device closed.");
    }
  }

  (*(AudioParam *)playbackParams).isEnded = true;

  pthread_exit((void *)true);
}

//Record audio input.
void *Audio::record_thread(void *recordParams)
{
  // Set log precursor value.
  const string fName = "Audio::record_thread";

  // Initialize playback parameters variable.
  AudioParam params = *(AudioParam *)recordParams;

  // Instantiate audio recording device variables.
  snd_pcm_t *record_handle;
  snd_pcm_hw_params_t *record_params;
  snd_pcm_uframes_t record_frames;
  int dir, err;

  // Instantiate audio recording info variable.
  SF_INFO record_sfinfo;

  // Set recording info parameters.
  record_sfinfo.channels = 1;
  record_sfinfo.samplerate = 8000;
  record_sfinfo.sections = 1;
  record_sfinfo.format = 65538;
  snd_pcm_format_t format = SND_PCM_FORMAT_S16_LE;

  // Initialize audio record file variable.
  SNDFILE *recordFile = NULL;

  // Initialize audio recording buffer.
  short *record_buffer = NULL;

  _log.debug(fName, "Begin recording audio input.");

  if (!_isSimulation)
  {
    // Open PCM audio device in capture mode.
    if ((err = snd_pcm_open(&record_handle, params.device.c_str(), SND_PCM_STREAM_CAPTURE, 0)) < 0)
    {
      (*(AudioParam *)recordParams).error = "Cannot open audio device <" + params.device + ">: " + (string)snd_strerror(err) + ".";
      pthread_exit((void *)false);
    }
    else
    {
      _log.debug(fName, "Audio device <" + params.device + "> opened.");
    }

    // Allocate hardware parameter structure.
    snd_pcm_hw_params_alloca(&record_params);

    // Initialize hardware parameter structure.
    if ((err = snd_pcm_hw_params_any(record_handle, record_params)) < 0)
    {
      _log.warning(fName, "Cannot initialize hardware parameter structure: " + (string)snd_strerror(err) + ".");
    }

    // Set access type.
    if ((err = snd_pcm_hw_params_set_access(record_handle, record_params, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0)
    {
      _log.warning(fName, "Cannot set access type <" + to_string(SND_PCM_ACCESS_RW_INTERLEAVED) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set sample format.
    if ((err = snd_pcm_hw_params_set_format(record_handle, record_params, format)) < 0)
    {
      _log.warning(fName, "Cannot set sample format <" + to_string(format) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set sample rate.
    if ((err = snd_pcm_hw_params_set_rate(record_handle, record_params, record_sfinfo.samplerate, 0)) < 0)
    {
      _log.warning(fName, "Cannot set sample rate <" + to_string(record_sfinfo.samplerate) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Set channel count.
    if ((err = snd_pcm_hw_params_set_channels(record_handle, record_params, record_sfinfo.channels)) < 0)
    {
      _log.warning(fName, "Cannot set channel count <" + to_string(record_sfinfo.channels) + ">: " + (string)snd_strerror(err) + ".");
    }

    // Write recording parameters.
    if ((err = snd_pcm_hw_params(record_handle, record_params)) < 0)
    {
      _log.warning(fName, "Cannot write recording parameters: " + (string)snd_strerror(err) + ".");
    }

    // Prepare audio interface.
    if ((err = snd_pcm_prepare(record_handle)) < 0)
    {
      _log.warning(fName, "Cannot prepare audio interface for use: " + (string)snd_strerror(err) + ".");
    }

    // Allocate audio recording buffer.
    snd_pcm_hw_params_get_period_size(record_params, &record_frames, &dir);
    record_buffer = (short *)malloc(record_frames * record_sfinfo.channels * sizeof(short));

    // Open audio record file.
    recordFile = sf_open(params.file.c_str(), SFM_WRITE, &record_sfinfo);

    _log.debug(fName, "Audio recording file <" + params.file + "> opened.");

    // While call is ongoing.
    while (!(*(AudioParam *)recordParams).isEnded)
    {
      // Read audio record frame from device.
      if ((err = snd_pcm_readi(record_handle, record_buffer, record_frames)) != (int)record_frames)
      {
        _log.warning(fName, "Read from audio interface failed: " + (string)snd_strerror(err) + ".");
      }
      // Save audio record frame to file.
      sf_writef_short(recordFile, record_buffer, record_frames);
    }

    // Free record buffer.
    free(record_buffer);

    // Write file to disk.
    sf_write_sync(recordFile);

    // Close file.
    sf_close(recordFile);

    _log.debug(fName, "Audio recording file written to disk and closed.");

    // Close audio recording device.
    if ((err = snd_pcm_close(record_handle)) < 0)
    {
      _log.warning(fName, "Cannot close audio recording device: " + (string)snd_strerror(err) + ".");
    }
    else
    {
      _log.debug(fName, "Audio recording device closed.");
    }
  }

  (*(AudioParam *)recordParams).isEnded = true;

  pthread_exit((void *)true);
}
