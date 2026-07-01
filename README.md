building a voice input calculator
AIM: The objective of this project is to develop a completely hands-free, off-hand calculation engine.
Current Project Status: Phase 2.0


Current abilities:
1. audio capture
2. speech processing-----Audio conversion into localized string text.
3. Functional Mappping------Routing parsed text to programmatic mathematical execution functions.

   
Current Challenges(at phase 1.5):
While "faster-whisper" solved the accuracy bottleneck, it introduced critical architectural constraints that are currently being debugged:

1. The Block-Buffering Latency Gap
The Problem: Unlike Vosk, Whisper cannot natively transcribe raw audio frame-by-frame in real-time. The system currently uses an interval-capture method (e.g., 3-second hard windows). 
The Bottleneck: The system captures 3 seconds of sound, locks the stream to run processing math, and then restarts the buffer. Any speech that spills across that 3-second boundary is either severed or lost entirely.

2. The Multi-Form Number Obstacle
The Problem: The engine frequently converts spoken strings interchangeably into raw numbers ("5") or text terms ("five"), which causes failure points in basic string parsing models.
The Fix: Implementing a "word2number" normalization wrapper to intercept strings and map text phrases to consistent integer data types prior to logic execution.(yet to be implemented)

3. CPU Core Overhead
The Problem: Running localized transformer models places a substantial processing load on the system hardware, causing thread delays between the audio collector loop and the inference module.

---
Solutions To This Challenges(phase 2.0):
1. The Block-Buffering Latency Gap
Since whisper could not handle real time and unlike the previous phase where i would only capture 3 seconds(or any timeframe you might set). I now restructure the code so the mic captures audio from the moment you start speaking till the moment you stop, then it transcribes the audio captured and executes.

2. The Multi-Form Number Obstacle
so i implemented the word2number library to be able to fix this as whisper would bring out numbers in numerical form or text(the model does it as to what fits the context). so with the w2n when i capture the command audio no matter the transcription in words or numerics the code understands and execution is sure.
   
3. CPU Core Overhead
the solution to this didn't take much. well i am currently using CPU that is why i am using a faster whisper model(base.en), tho its a lower model it immediately kicked my fans the moment i ran the code so it was really heavy on my CPU, all i did was just reduce the beam size from '5' to '1'(when the mic captures audio and sends it to the model for transcription, it begins to run the transcription in different scenarios for a higher accuracy, now the beam size is that number of scenarios, so i reduced it from '5' scenarios to '1' scenario. 


Stack:
1. for STT engine we use Faster-whisper(base.en)
2. audio processing we use numpy, sounddevice
3. text normalization we use word2number(now implemented)

order:
1. milestone prototype 1 with tts -(uses google cloud)
2. milestone1 protoype - (uses vosk)
3. milestone1 prototype with whisper - (faster whissper)
4. milestone 1 prototype with whisper and tts -(faster whisper)
5. milestone 1 prototype with whisper and tts 4-(faster whisper)

PHASE 1.5
so far so the best result one got was with the google cloud, but my aim is to get it offline and working very efficiently cos of internet access in my location so that one is not limited. so i decided to try vosk(their lowest model of about 40mb) first which was alright in terms of real-time transcription but very poor in accuracy. now decided to try faster whisper their base.en model tho its amongst their least models it's accuracy is way superior to that of vosk but comes with a downside, it cannot implement real time transcription. i first have to capture some seconds of audio data(adjustable to any timeframe i want) then send it to the model for transcription so for instance i say 3 seconds it first take 3 seconds of audio and send to the model it processes that and then captures another 3 seconds again. so you see that anything outside that 3 seconds is lost or parsed into the next line of transcription. so i still got lot of work to do, this basic voice calculator is actually my first milestone in the long-term journey of what is to come.  

PHASE 2.0
now i have worked out how whisper takes in audio, the new structure makes it realtime, it starts capturing the moment you start speaking and stops for interpretation and execution the moment you stop speaking. so it runs well, it can do basic the following basic calculations:
1. addition.
2. subtraction.
3. division(it gives you in 2 decimal places and also includes the remainder).
4. multiplication.
5. exponent.
#you can comment whatever arithmetic operation you would like me to add
