building a voice input calculator
AIM: to develop an off-hand system for calculations
Current Project Status: Phase 1.5
Current abilities:
1. audio capture
2. speech processing
3. Functional Mappping

Current challenges:
1.  the accent accuracy
2.  The multi-form number obstacle
3.  weight on cpu

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

