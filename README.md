# Car Vocal Agent
Agent vocal pour voiture. Vous pouvez appeler l'agent en disant à l'oral "Assistant", puis il sera à votre écoute pour effectuer l'action que vous souhaitez. Un agent IA analysera votre demande et choisira l'action à effectuer. Le LLM GPT-4.1-mini est utilisé pour orchestrer les actions. Le framework utilisé pour executer les actions est Langchain.  

![Ma voiture](images/image_readme.png)


## Exemples : 
- Aumgmente le volume : 50% -> 60%
- J'ai trop chaud : active la climatisation et met la température sur 18°
- On arrive sur l'autoroute : limiteur de vitesse à 130km/h
- Je vois rien : active les plein phares
- Met du rap
- Appelle Jean
- Raccroche




## Installations : 

Variables d'environnement : 
Créer un fichier .env avec : 
```
OPENAI_API_KEY="sk-..."
USER_AGENT="myagent"
```
Obtenir une Clé API OpenAI : https://platform.openai.com/api-keys

Environnement virtuel : 
```
python3.11 -m venv .venv
source .venv/bin/activate
```

Mac : 
```
brew install portaudio
CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio
pip install -r requirements.txt
```

## Lancer l'application : 

Frontend Tkinter (image de présentation): 
```
python app_agent.py
```

Frontend Streamlit simple : 
```
streamlit run frontend.py
python back_agent.py
```
