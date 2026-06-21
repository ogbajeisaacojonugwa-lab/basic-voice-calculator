import json 
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3

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

"""everything after here is just hypothesis, to understand the flow, so gemini bear with me
and see if you can get te concept i don't really know the syntax
"""
#booting up the voice input
engine = pyttsx3.init()

#booting up the brain input
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)
print('[System]: Offline Engine Ready. Mic is live.......')

#  opening the physical wire to the microphone, note we use 1 channel to reduce load on cpu performance 
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
    while True:
        print('.', end ='', flush = True)# checkpoint 1
    # to capture the raw data block from the sound device
        data, overflow = stream.read(8000)
        sd.wait()
    # feed the raw audio bytes into the vosk engine
        if recognizer.AcceptWaveform(bytes(data)):
            print("\n[vosk]: Sentence completed!")### checkpoint 2
        # pulls the raw data package from the vosk engine
            result_raw = recognizer.Result()
        # use json to unpack to python dict
            result_json = json.loads(result_raw)
        # ectract the clean text and doesn't crash if dict is empty
            sentence = result_json.get('text', '')
            print("[Raw text heard]:", sentence)
            if not sentence:
                continue
        
            print('[Text confirmation]: You said:', sentence)
            if "end" in sentence or "stop" in sentence or "exit" in sentence:
                output = "Terminating system session. Goodbye!"
                print('[System]:', output)
                engine.say(output)
                engine.runAndWait()
                break

            number = []
            sentence_list = []
            action = None
            split = sentence.split()
            for k in split:
                sentence_list.append(k)
                if k in dict_map:
                    action = k
                elif k.isdigit():
                    integer = int(k)
                    number.append(integer)

        #dict search and assignment
            if action and len(number) >=2: 
                function_to_call = dict_map[action]    
                a = number[0]
                b = number[1]

                result = function_to_call(a,b)
                print('[Result]:', result)
                engine.say('The result is' + str(result))
                engine.runAndWait()