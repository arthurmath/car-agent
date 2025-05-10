# Car Vocal Agent
Agent vocal pour voiture. Vous pouvez appeler l'agent en disant à l'oral "Assistant", puis il sera à votre écoute pour effectuer l'action que vous souhaitez. Un agent IA analysera votre demande et choisira l'action à effectuer. Le LLM GPT-4.1-mini est utilisé pour orchestrer les actions.  
Exemples : 
    - J'ai trop chaud : active la climatisation et met la température sur 18°
    - On arrive sur l'autoroute : limiteur de vitesse à 130km/h


## Installations : 
Mac : 

    brew install portaudio
    CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio
    pip install -r requirements.txt


## Lancer l'application : 

Nouveau frontend : 
    launch app_agent.py

Ancien frontend : 
    streamlit run frontend.py
