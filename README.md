building a voice input calculator
AIM: The objective of this project is to develop a completely hands-free, off-hand calculation engine.
Current Project Status: Phase 1.5


Current abilities:
1. audio capture
2. speech processing-----Audio conversion into localized string text.
3. Functional Mappping------Routing parsed text to programmatic mathematical execution functions.

   
Current Challenges:
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


Stack:
1. for STT engine we use Faster-whisper(base.en)
2. audio processing we use numpy, sounddevice
3. text normalization we use word2number(yet to be implemented)

order:
1. milestone prototype 1 with tts -(uses google cloud)
2. milestone1 protoype - (uses vosk)
3. milestone1 prototype with whisper - (faster whissper)
4. milestone 1 prototype with whisper and tts -(faster whisper)

so far so the best result one got was with the google cloud, but my aim is to get it offline and working very efficiently cos of internet access in my location so that one is not limited. so i decided to try vosk(their lowest model of about 40mb) first which was alright in terms of real-time transcription but very poor in accuracy. now decided to try faster whisper their base.en model tho its amongst their least models it's accuracy is way superior to that of vosk but comes with a downside, it cannot implement real time transcription. i first have to capture some seconds of audio data(adjustable to any timeframe i want) then send it to the model for transcription so for instance i say 3 seconds it first take 3 seconds of audio and send to the model it processes that and then captures another 3 seconds again. so ou see that anything outside that 3 seconds is lost or parsed into the next line of transcription. so i still got lot of work to do, this basic voice calculator is actually my first milestone in the long-term journey of what is to come.  

