
from os import system, path, remove
import wave
import pyaudio
import time

class GLaDOSTTS:

    def __init__(self) -> None:
        self.file_path = 'audio/'
        self.voice_line_file = 'required_voice_lines.txt'

        # Check to see if the Required Voice Lines File Exists
        # If it does, download all of the voices lines. If it doesn't you don't need to download anything
        if path.exists(self.voice_line_file):
            self._download_voice_lines(self.voice_line_file)


    '''
        Check if the Audio File Already Exists. This will check in the default audio file for the code
        @param file_name (str): Name of the file
        @return bool: Does the file exist
    '''
    def _check_for_file(self, file_name) -> bool:
        return path.exists(self.file_path + file_name)

    '''
        Download a GLaDOS voice line. This uses the website "glados.c-net.org" to make the tts in GLaDOS's voice.
        This system command should work cross platform when it gets transfered to a Pi
        @param message (str): Line that GLaDOS will say
        @param filename (str): Name to save the file under in the audio dir
    '''
    def download_new_tts_message(self, message, filename) -> None:
        _download_command = 'curl -L --retry 30 --get --fail --data-urlencode "text=' \
                            + message + '" -o "' + self.file_path + filename + '.wav" ' \
                            + '"https://glados.c-net.org/generate"'
        system(_download_command)

    '''
        User PyAudio to play the audio file
        @param filename (str): Name of File to be played
    '''
    # Special Thanks to Nerdaxic
    # https://github.com/Nerdaxic/GLaDOS-Voice-Assistant/blob/main/gladosTTS.py
    def play_file(self, filename) -> None:
        chunk = 1024 # Define chunck size of 1024 samples per data frame
        _file_path = self.file_path + filename
        file = wave.open(_file_path, 'rb') # Open sound file in read binary form

        p = pyaudio.PyAudio() # Initialize PyAudio

        # Creates a Stream where the wav file is written to
        stream = p.open(format = p.get_format_from_width(file.getsampwidth()),
	                channels = file.getnchannels(),
	                rate = file.getframerate(),
	                output = True)

        data = file.readframes(chunk)
        # Play the sound by writing the audio to the stream
        while True:
            data = file.readframes(chunk)
            if not data:
                break
            stream.write(data)
        
        time.sleep(0.1)

        # Stop, Close, and terminate the stream
        stream.stop_stream()
        stream.close()

    '''
        Create a New Message. This will be ran when GLaDOS powers up for the very first time. 
        It will be part of the loading sequence
        It will then delete the file of voice lines to download
        @param filepath (str): Path of the Voice Lines File
    '''
    def _download_voice_lines(self, filepath) -> None:
        print('Downloading Required Voice Lines. Please be Patient')
        _voice_file = open(file=filepath, mode='r') # Open the File as a Read Only
        _lines = _voice_file.read().split(';') # Split the Content at the ';' this will give us all the lines and their file names in a list
        for line in _lines:
            if line == '\nEND':
                break
            new_line = line.replace('"', '').split(':') # This will give you the line and the file name ([0] = line, [1] = file name)
            print('Processing:', new_line)
            if not self._check_for_file(new_line[1]): # Check if the File Name already Exists
                self.download_new_tts_message(new_line[0], new_line[1])
        _voice_file.close() # Close the File Before Remove
        print('Finished Downloading Voice Lines.')
        remove(filepath) # Delete the File
        