brew install portaudio
CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio
pip install SpeechRecognition pyttsx3 streamlit


streamlit run frontend.py
