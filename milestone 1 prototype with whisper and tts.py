import time
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import pyttsx3

# activating the brain
model = WhisperModel("base.en", device="cpu", compute_type="int8")
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
audio_buffer = []
engine = pyttsx3.init()


number_of_calculations = 0
def sums(a,b):
    global number_of_calculations
    number_of_calculations +=1
    result = a + b
    return result
def division(a,b):
    global number_of_calculations
    number_of_calculations +=1
    result = a/b
    return result
def multiply(a,b):
    global number_of_calculations
    number_of_calculations +=1
    result = a*b
    return result
def minus(a,b):
    global number_of_calculations
    number_of_calculations += 1
    result = a-b
    return result

dict_map = {
    "add": sums,
    "plus": sums,
    "sum": sums,
    '+': sums,
    'increased': sums,
    '-': minus,
    "minus": minus,
    "subtract": minus,
    'subtracted': minus,
    'take': minus,
    'decrease': minus,
    'decreased': minus,
    "remove": minus,
    "multiply": multiply,
    "times": multiply,
    'multiplied': multiply,
    '*': multiply,
    "divide": division,
    'divided': division,
    '/': division
}


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_buffer.append(indata.copy())

def solve_math(text):
    text = text.lower()
    words = text.split()
    numbers = []
    action = None
    for word in words:
        clean_word = word.strip(".,?!")
        if clean_word.isdigit():
            numbers.append(int(clean_word))

    if len(numbers) == 2:
        a, b = numbers[0], numbers[1]

        for k in words:
            clean_k = k.strip(".,!?")
            if clean_k in dict_map:
                action = clean_k
                function_to_call = dict_map[action]
                result = function_to_call(a,b)
                return result

    return None

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=audio_callback):
    print('[System]: live and listening, speak......')
    # speedbump number 1
    system_processing = False

    while True:
       if system_processing:
           time.sleep(0.1)
           continue
       if len(audio_buffer) > 0:
            audio_data = np.concatenate(audio_buffer, axis=0).flatten()

            if len(audio_data)>=96000:

                system_processing = True

            
                audio_buffer = []
                volume = np.sqrt(np.mean(audio_data**2))
                if volume > 0.01:
                    segments, info = model.transcribe(audio_data, beam_size=5)
                    sentence = "".join([segment.text for segment in segments]).strip()
                    if sentence:
                        print('[Text for confirmation]:', sentence)
                        math_output = solve_math(sentence)
                        if math_output is not None:
                            print('[System]: The result is,', math_output)
                            speak = ('The result is,', str(math_output))
                            engine.say(speak)
                            engine.runAndWait()
                   
                else:
                   print('[System]: Too quiet, skipping.......' ) 

                system_processing = False

            time.sleep(0.1)
          