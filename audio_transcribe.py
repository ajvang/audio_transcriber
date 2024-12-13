import sounddevice
from scipy.io.wavfile import write
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Loading  OpenAI API key from environment variable config file
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

file_dir = os.path.abspath(__file__)
ffmpeg_filepath = os.path.dirname(file_dir)+r'\ffmpeg\bin\ffmpeg.exe'

#checking cwd is same as script file - change directory if needbe
if os.path.abspath(os.curdir) != os.path.dirname(file_dir):
    os.chdir(os.path.dirname(file_dir))

def transcribe_audio(input_audio_file):
    print("Working out what you said....")
    # Open the openai-audio.mp3 file
    audio_file = open(input_audio_file, "rb")

    # Create a transcript from the audio file
    response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    # Extract and print the transcript text
    print("You said....")
    print(response.text)
    exit_confirm = input("\n \n Press enter to Exit")
    if exit_confirm == "":
        quit()
    else:
        print(exit_confirm)
        quit()

def record_audio():
    # sample_rate
    fs = 44100

    # Asking to enter the recording time
    second = int(input("Enter the Recording Time in seconds: "))
    print("Recording.....\n")

    # Record voice to wav
    record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write("MyRecording2.wav", fs, record_voice)
    print("Recording is done")
  
    #run file transformation from wav to mp3 using ffmpeg (assumption is located in ./ffmpeg/bin. Sets audio bitrate to 192k using '-b:a' and '192k' parameters
    subprocess.run([ffmpeg_filepath, "-i", "MyRecording2.wav", "-b:a", "192k","output.mp3"])
    print("Converted audio to mp3")


record_audio()
transcribe_audio("output.mp3")
