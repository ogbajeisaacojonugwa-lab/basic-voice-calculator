import speech_recognition as sr
import pyaudiowpatch as ya
import pyttsx3

engine = pyttsx3.init()

sr.Microphone.get_pyaudio = lambda *args, **kwargs: ya
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
    "minus": minus,
    "subtract": minus,
    "remove": minus,
    "multiply": multiply,
    "times": multiply,
    "divide": division
}

"""everything after here is just hypothesis, to understand the flow, so gemini bear with me
and see if you can get te concept i don't really know the syntax
"""
recognizer = sr.Recognizer()
while True:
    number = []
    sentence_list = []
    action = None
    with sr.Microphone(device_index=2) as source:
        print('[System]: Calibrating for background noise..stay quiet')
        #recognizer.adjust_for_ambient_noise(source, duration=1)

        #manual energy treshold hardcoded(300 is standard for clear speech)
        recognizer.energy_threshold = 300

        print('[System]: Mic is live, speak your math operation now')
        #listens until you stop talking
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=6)
        try:
        #convert to text with google api also making it lowercase
            sentence = recognizer.recognize_google(audio_data).lower()
            print('[Text Confirmation]: You said', sentence)
        except sr.UnknownValueError:
            print('[Error]: My bad i couldn\'t make out what you said')
            continue
        except sr.WaitTimeoutError:
            #EXIT CONDITION 1: 10 seconds of absolute silence passed
            output = "Shutting down due to inactivity. Goodbye!"
            print('[System]:', output)
            engine.say(output)
            engine.runAndWait()
            break  # Breaks the while loop to end the program cleanly
        except sr.RequestError:
            print('[Error]: Couldn\'t reach the server, check your internet connectiion and try again')

    #EXIT CONDITION 2:
    if "end" in sentence or "stop" in sentence or "exit" in sentence:
        output = "Terminating system session. Goodbye!"
        print('[System]:', output)
        engine.say(output)
        engine.runAndWait()
        break   
    
    split = sentence.split()
    for k in split:
        sentence_list.append(k)
        if k in dict_map:
            action = k
        elif k.isdigit():
            integer = int(k)
            number.append(integer)

        #dict search and assignment
    function_to_call = dict_map[action]    
    a = number[0]
    b = number[1]

    result = function_to_call(a,b)
    print('[Result]:', result)
    engine.say('The result is ' + str(result))
    engine.runAndWait()