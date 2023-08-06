/*
This file is part of the Comms communications library for Raspberry Pi
*/
#include "../inc/comms.h"

//Configure modem communication.
void Comms::configure(bool simulation, string serialPort)
{
  // Set log precursor value.
  const string fName = "Comms::configure";

  // Set modem-communication simulation value.
  _isSimulation = simulation;

  string value = _isSimulation ? "true" : "false";
  _log.debug(fName, "Comms simulation debug value set to <" + value + ">.");

  if (serialPort != "")
  {
    // Set serial port name.
    _serialPortName = serialPort;
  }

  _log.debug(fName, "Serial port set to <" + _serialPortName + ">.");
}

//Get modem connection status.
bool Comms::getConnectionStatus()
{
  return _isConnected;
}

//Initialize modem communication.
bool Comms::init()
{
  // Set log precursor value.
  const string fName = "Comms::init";

  _log.debug(fName, "Begin initializing modem communications.");

  if (!_isSimulation)
  {
    // If disconnected.
    if (!_isConnected)
    {
      // Open serial port.
      if ((_serialPort = serialOpen(_serialPortName.c_str(), BAUD_RATE)) < 0)
      {
        // Serial port failed to open.
        _log.warning(fName, "The serial port <" + _serialPortName + "> did not open correctly: " + (string)strerror(errno));
        return false;
      }
      else
      {
        // Serial port successfully opened.
        _log.debug(fName, "Serial port <" + _serialPortName + "> opened with baud rate <" + to_string(BAUD_RATE) + ">.");

        // Set connected variable to true.
        _isConnected = true;

        return true;
      }
    }
    else
    {
      _log.debug(fName, "Modem connected.");

      return true;
    }
  }
  // Simulate modem communication initialization.
  else
  {
    // Debug simulation delay.
    delay(SIMULATION_DELAY);

    _log.debug(fName, "(SIMULATED) Serial port <" + _serialPortName + "> opened with baud rate <" + to_string(BAUD_RATE) + ">.");

    // Set connected variable to true.
    _isConnected = true;

    return true;
  }
}

//Close modem communication.
void Comms::close()
{
  // Set log precursor value.
  const string fName = "Comms::close";

  _log.debug(fName, "Begin closing modem communications.");

  if (!_isSimulation)
  {
    // Close the serial port.
    serialClose(_serialPort);
    _log.debug(fName, "Serial port <" + _serialPortName + "> closed.");
  }
  else
  {
    // Simulate closing modem communication.
    delay(SIMULATION_DELAY); // Debug simulation delay.
    _log.debug(fName, "(SIMULATED) Serial port <" + _serialPortName + "> closed.");
  }
}

//Send AT command.
bool Comms::sendATCommand(string command, string desiredResponse)
{
  // Set log precursor value.
  const string fName = "Comms::sendATCommand";

  _log.debug(fName, "Begin sending AT Command <" + _utils.escaped(command) + "> with desired response <" + _utils.escaped(desiredResponse) + ">.");

  // Flush serial TX & RX buffers.
  if (!_isSimulation)
  {
    serialFlush(_serialPort);
  }

  // Initialize try count variable.
  int tries = 1;

  // Send command to serial port.
  if (!_isSimulation)
  {
    serialPuts(_serialPort, command.c_str());
    _log.debug(fName, "Try " + to_string(tries++) + ": Command <" + _utils.escaped(command) + "> sent.");
  }
  else
  {
    _log.debug(fName, "(SIMULATED) Try " + to_string(tries++) + ": Command <" + _utils.escaped(command) + "> sent.");
  }

  // If no response needed.
  if (desiredResponse == "")
  {
    return true;
  }
  else
  {
    // Instantiate response variable for AT command.
    char response[AT_RESPONSE_LEN];
    memset(response, 0, AT_RESPONSE_LEN);
    int i = 0; // Initialize response array index.

    // Declare input string variable.
    string input;

    // Set timer to current time.
    uint32_t timer = millis();

    while (true)
    {
      // If send AT command timeout reached.
      if (millis() - timer > AT_COMMAND_TIMEOUT)
      {
        _log.debug(fName, "Input received <" + _utils.escaped(input) + "> does not match desired response <" + _utils.escaped(desiredResponse) + ">.");

        // If maximum number of tries reached.
        if (tries > AT_MAX_TRIES)
        {
          // Abort sending AT command.
          _log.warning(fName, "Did not receive desired response <" + _utils.escaped(desiredResponse) + "> for command <" + _utils.escaped(command) + ">.");
          return false;
          break;
        }

        // Send command to serial port.
        if (!_isSimulation)
        {
          serialPuts(_serialPort, command.c_str());
          _log.debug(fName, "Try " + to_string(tries++) + ": Command <" + _utils.escaped(command) + "> sent.");
        }

        // Reset response array and index.
        memset(response, 0, AT_RESPONSE_LEN);
        i = 0;

        // Reset timer to current time.
        timer = millis();
      }

      if (!_isSimulation)
      {
        // Poll serial port for data.
        while (serialDataAvail(_serialPort))
        {
          // Save character to response array.
          response[i++] = serialGetchar(_serialPort);
          // Convert character array to string.
          input = response;

          // If input matches desired response.
          if (desiredResponse.compare(input) == 0)
          {
            _log.debug(fName, "AT command <" + _utils.escaped(command) + "> sent with response <" + _utils.escaped(input) + ">.");
            return true;
            break;
          }
          else
          {
            // Poll response delay.
            delay(AT_POLL_RESPONSE_DELAY);
          }
        }
      }
      else
      {
        // Simulate sending AT command.
        delay(SIMULATION_DELAY); // Debug simulation delay.
        _log.debug(fName, "(SIMULATED) AT command <" + _utils.escaped(command) + "> sent with response <" + _utils.escaped(desiredResponse) + ">.");
        return true;
        break;
      }
    }
  }
}

//Read AT response.
string Comms::readATResponse(unsigned int timeout)
{
  // Set log precursor value.
  const string fName = "Comms::readATResponse";

  _log.debug(fName, "Begin reading AT response.");

  // Instantiate response variable.
  char response[AT_RESPONSE_LEN];
  memset(response, 0, AT_RESPONSE_LEN);
  int i = 0; // Initialize response array index.

  // Declare input string variable.
  string input;

  // Set timer to current time.
  uint32_t timer = millis();

  while (true)
  {
    // If read AT response timeout reached.
    if (millis() - timer > timeout)
    {
      // Abort reading AT response.
      _log.warning(fName, "Did not receive response.");
      return "NO RESPONSE";
      break;
    }

    if (!_isSimulation)
    {
      // Poll serial port for data.
      while (serialDataAvail(_serialPort))
      {
        // Save character to response array.
        response[i++] = serialGetchar(_serialPort);
        // Convert character array to string.
        input = response;

        // If input contains desired response.
        if (input.find("OK\r\n") != string::npos)
        {
          input.erase(input.end() - 4, input.end()); // Extract response from input.
          _log.debug(fName, "Response <" + _utils.escaped(input) + "> received.");
          return input;
          break;
        }
        else
        {
          // Poll response delay.
          delay(AT_POLL_RESPONSE_DELAY);
        }
      }
    }
    else
    {
      // Simulate reading AT response.
      delay(SIMULATION_DELAY); // Debug simulation delay.
      input = "Responded!";
      _log.debug(fName, "(SIMULATED) Response <" + input + "> received.");
      return input;
      break;
    }
  }
}

//Upload file.
bool Comms::uploadFile(string filePath, string &fileName)
{
  // Set log precursor value.
  const string fName = "Comms::uploadFile";

  _log.debug(fName, "Begin uploading file.");

  // Get file name & size.
#if __has_include(<filesystem>)
  filesystem::path p{filePath};
  fileName = p.filename();
  int fileSize = filesystem::file_size(p);
#else
  experimental::filesystem::path p{filePath};
  fileName = p.filename();
  int fileSize = experimental::filesystem::file_size(p);	
#endif

  // Declare read-file variables.
  FILE *pFile;
  long lSize;
  char *buffer;
  size_t result;

  if (!_isSimulation)
  {
    // Open file.
    pFile = fopen(filePath.c_str(), "rb");
    if (pFile == NULL)
    {
      _log.warning(fName, "File error.");
      return false;
    }

    // Obtain file size.
    fseek(pFile, 0, SEEK_END);
    lSize = ftell(pFile);
    rewind(pFile);

    // Allocate memory to contain the whole file.
    buffer = (char *)malloc(sizeof(char) * lSize);
    if (buffer == NULL)
    {
      _log.warning(fName, "Memory error.");
      return false;
    }

    // Copy the file into the buffer.
    result = fread(buffer, 1, lSize, pFile);
    if (result != (long unsigned int)lSize)
    {
      _log.warning(fName, "Reading error.");
      return false;
    }

    _log.debug(fName, "File <" + fileName + "> loaded into memory buffer.");

    // Upload file to storage (See File application note: 2.4 - AT+QFUPL [page 12]).
    sendATCommand(AT_FILE_UPLOAD + fileName + "\"," + to_string(fileSize) + "\r\n", AT_FILE_CONNECT);

    // Write file binary to modem.
    if (write(_serialPort, buffer, lSize) == -1)
    {
      _log.warning(fName, "Failed to write file binary to modem.");
    }

    // Close file and free buffer.
    fclose(pFile);
    free(buffer);

    // Read file-upload reponse.
    string response = readATResponse();

    // If file-upload response matches desired response.
    if (response.find(AT_FILE_UPLOAD_RESPONSE) != string::npos)
    {
      _log.debug(fName, "File <" + fileName + "> uploaded.");
      return true;
    }
    else
    {
      _log.warning(fName, "File did not complete uploading.");
      return false;
    }
  }
  else
  {
    // Simulate uploading file.
    delay(SIMULATION_DELAY); // Debug simulation delay.
    _log.debug(fName, "(SIMULATED) File <" + fileName + "> uploaded.");
    return true;
  }
}

//Read keypad input value.
bool Comms::readKeypadInput(char &value, unsigned int timeout)
{
  // Set log precursor value.
  const string fName = "readKeypadInput";

  _log.debug(fName, "Begin reading keypad input.");

  // Instantiate response variable.
  char response[IVR_RESPONSE_LEN];
  memset(response, 0, IVR_RESPONSE_LEN);
  int i = 0; // Initialize response array index.

  // Declare input string variable.
  string input;

  // Set timer to current time.
  uint32_t timer = millis();

  while (true)
  {
    // If read keypad input timeout reached.
    if (millis() - timer > timeout)
    {
      // Abort reading kepad input.
      _log.warning(fName, "Did not receive keypad input.");
      return false;
      break;
    }

    if (!_isSimulation)
    {
      // Poll serial port for data.
      while (serialDataAvail(_serialPort))
      {
        // Save character to response array.
        response[i++] = serialGetchar(_serialPort);
        // Convert character array to string.
        input = response;

        // If input contains desired response.
        if (input.find(AT_IVR_KEYPAD_RESPONSE) != string::npos)
        {
          // Get keypad digit values.
          char res[2];
          res[0] = serialGetchar(_serialPort);
          res[1] = serialGetchar(_serialPort);

          // Combine digit values into an integer.
          int val;
          sscanf(res, "%d", &val);

          // Convert integer into an ascii character.
          string resp(1, static_cast<char>(val));
          value = resp.at(0);

          _log.debug(fName, "Keypad input <" + string(1, value) + "> received.");
          return true;
          break;
        }
        else
        {
          // Poll response delay.
          delay(AT_POLL_RESPONSE_DELAY);
        }
      }
    }
    else
    {
      // Simulate reading keypad input.
      delay(SIMULATION_DELAY); // Debug simulation delay.
      value = '0';
      _log.debug(fName, "(SIMULATED) Keypad input <" + string(1, value) + "> received.");
      return true;
    }
  }
}
