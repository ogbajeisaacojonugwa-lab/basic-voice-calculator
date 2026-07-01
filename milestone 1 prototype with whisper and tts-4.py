import time
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import pyttsx3
from word2number import w2n
import random


# activating the brain
model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
audio_buffer = []


#VAD parameters
VOLUME_THRESHOLD = 0.015
SILENCE_DURATION = 1.2

# live engine track
silence_counter = 0
is_speaking = False
collected_audio_frames = []
system_processing = False


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
    if a % b == 0:
        return round(result)
    else:
        remainder = a % b
        return f"{round(result, 2)} with a remainder of {remainder}"
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
def exponent(a,b):
    global number_of_calculations
    number_of_calculations += 1
    result = a**b
    if a % b == 0:
        return round(result)
    else:
        return round(result,2)


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
    "into": division,
    "divide": division,
    'divided': division,
    '/': division,
    'power': exponent,
    "root": exponent,
    "square root": exponent,
    "square": exponent
}

import threading
def speech_feedback(text):
    #executing speech engine on a background worker thread microphone input stream never stutters
    def worker():
        try:
            local_engine = pyttsx3.init()
            local_engine.say(text)
            local_engine.runAndWait()

            local_engine.stop()
        except Exception as e:
            print(f"[Speech Thread Alert]: {e}")
       
    threading.Thread(target=worker, daemon=True).start()

def number_extract(speech_text):
    m = speech_text
    clean_m = m.strip('.,!?')
    split = clean_m.split()
    current_number = []
    final_number = []
    for word in split:
        if word == 'and':
            current_number.append(word)
            continue
        try:
            w2n.word_to_num(word)
            current_number.append(word)
       
         
        except ValueError:
            if len(final_number) < 2:
                phrase = " ".join(current_number)
                if not phrase:
                    continue
                else:
                    try:
                        converted_number = w2n.word_to_num(phrase)
                        final_number.append(converted_number)
                    except ValueError:
                        pass 

                    current_number = []
                    continue
            else:
                print('[System]:integers more than (2). only accepts two integers')
                break
       
    if current_number:
        if len(final_number) < 2:
    
            phrase = " ".join(current_number)
            try:
                converted_number = w2n.word_to_num(phrase)    
                final_number.append(converted_number)
            except ValueError:
                pass

            current_number = []
        else:
            print('[System]:integers more than (2). only accepts two integers')
    
    else:
        print('[System]: No integer detected in the phrase')
    return final_number

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_buffer.append(indata.copy())

def solve_math(text):
    text = text.lower()
    words = text.split()

    numbers = number_extract(text)
    if "square" in words and "root" in words:
        if len(numbers) > 0:
            base_number = numbers[0]
            numbers = [base_number, 0.5]
    elif "square" in words:
        if len(numbers) > 0:
            base_number = numbers[0]
            numbers = [base_number, 2]

    if len(numbers) == 2:
        a, b = numbers[0], numbers[1]

        #inversion checker
        if "from" in words or "into" in words:
            a = numbers[1]
            b = numbers[0]


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
    # to clean backlog fluid
    audio_buffer.clear()
    # speedbump number 1
    system_processing = False

    while True:
       sentence = ""
       if system_processing:
           time.sleep(0.1)
           continue
       if len(audio_buffer) > 0:
            # for pulling only a single 1024 frame slice off the queue
            next_chunk = audio_buffer.pop(0).flatten()
            if is_speaking:
                collected_audio_frames.append(next_chunk)

            chunk_volume = np.sqrt(np.mean(next_chunk**2))
            #calculate the energy level


            if chunk_volume > VOLUME_THRESHOLD:
                if not is_speaking:
                    print('[VAD]: Voice detected capturing stream....')
                    is_speaking = True
                    collected_audio_frames.append(next_chunk)
                silence_counter = 0
            else:
                if is_speaking:
                    silence_counter += 1

            # check silence duration is reached
            chunks_per_second = SAMPLE_RATE / CHUNK_SIZE
            if is_speaking and (silence_counter / chunks_per_second) >= SILENCE_DURATION:
                system_processing = True
                
                #merge chunks intpo one continuous audio vector
                audio_data = np.concatenate(collected_audio_frames, axis=0)

                collected_audio_frames = []
                is_speaking = False
                silence_counter = 0

                print("[VAD]: silence detected. processing phrase")

                segments, info = model.transcribe(audio_data, beam_size=1, language="en")
                sentence = "".join([segment.text for segment in segments]).strip()


                if sentence:
                    print('[Text for confirmation]:', sentence)

                #handling safe exits
                    sentence_words = [word.strip(".,!?") for word in sentence.lower().split()]

                    #the trigger words (seperate single from phrase)
                    single_word_triggers = ["stop","end", "exit", "terminate", "goodbye", "bye", "kill","off","shut"]                    
                    phrase_triggers = ["power off", "shut down"]
                    
                    #trigger logic
                    should_exit = (
                        any(trigger in sentence_words for trigger in single_word_triggers) or
                        any(phrase in sentence.lower() for phrase in phrase_triggers)
                    )

                    if should_exit:
                        print("[System]: Shutting down pipeline.")
                        remarks = ["goodbye", "see you later", "goodbye, catch you later", "goodbye, have a nice day"]
                        speech_feedback(random.choice(remarks))
                        audio_buffer.clear()
                        print('number of calculations made:',number_of_calculations)
                        time.sleep(1)
                        break
                    elif "thank you" in sentence.lower() or "thanks" in sentence_words:
                        print("[System]: You Are Welcome")
                        response = ["I am glad i could help", "Don't mention it", "You are welcome"]
                        speech_feedback(random.choice(response))

                        audio_buffer.clear()
                        system_processing = False
                        continue

                    math_output = solve_math(sentence)
                    if math_output is not None:
                        output_str = f"the result is {math_output}"
                        print('[System]:', output_str)
                        speech_feedback(output_str)
                else:
                    print('[System Debug]: False trigger discarded')

                audio_buffer.clear()
                system_processing = False

            
            time.sleep(0.01)
          