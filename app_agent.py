import os
import json
from langchain import hub
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from typing import Any
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import PhotoImage
import json
import sys

from dotenv import load_dotenv
load_dotenv()






# === CHARGER/SAUVER L'ÉTAT ===

def load_state():
    with open("voiture.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open("voiture.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)





# === TOOLS ===

def climatisation(button: str):
    if button == "On":
        state = load_state()
        state["climatisation"] = "On"
        save_state(state)
        return "Climatisation activée.\n"
    elif button == "Off":
        state = load_state()
        state["climatisation"] = "Off"
        save_state(state)
        return "Climatisation désactivée.\n"
    else:
        return "Commande invalide. Utilisez 'On' ou 'Off' uniquement."
    
def temperature(temp: int):
    try:
        state = load_state()
        state["temperature"] = int(temp)
        save_state(state)
        return f"Température réglée à {temp} degrés.\n"
    except ValueError:
        return "Je n'ai pas compris la température demandée."

def volume(vol: int):
    try:
        volume = min(100, max(0, int(vol)))
        state = load_state()
        state["volume"] = int(volume)
        save_state(state)
        return f"Volume réglé à {volume}%.\n"
    except ValueError:
        return "Je n'ai pas compris le volume demandé."
    
def musique(playlist: str):
    try:
        state = load_state()
        state["musique"] = playlist
        save_state(state)
        return f"Playlist {playlist} lancée.\n"
    except ValueError:
        return "Je n'ai pas compris la playlist demandée."
    
def limiteur_vitesse(vitesse: int):
    try:
        state = load_state()
        state["limiteur"] = int(vitesse)
        save_state(state)
        return f"Limiteur de vitesse réglé à {vitesse} km/h.\n"
    except ValueError:
        return "Je n'ai pas compris la vitesse demandée."

def changer_phare(type_phare: str):
    options = ["position", "croisement", "route"]
    state = load_state()
    if type_phare in options:
        correspondance = {
            "position": "feux de position",
            "croisement": "feux de croisement",
            "route": "feux de route"
        }
        state["phares"] = correspondance[type_phare]
        save_state(state)
        return f"Phares réglés sur {correspondance[type_phare]}.\n"
    else:
        return "Type de phare inconnu."

def appeler_contact(nom: str):
    state = load_state()
    if nom.lower() in state["contacts"]:
        state["appel"] = nom.lower()
        save_state(state)
        return f"Appel lancé vers {nom.capitalize()}.\n"
    else:
        return "Contact introuvable."

def raccrocher(nothing: Any):
    state = load_state()
    state["appel"] = "aucun"
    save_state(state)
    return "Appel terminé.\n"





tools = [
    Tool(name="Climatisation", func=climatisation, description="Active ou désactive la climatisation. Prend en entrée : 'On' ou 'Off'."),
    Tool(name="Temperature", func=temperature, description="Règle la température en degrés. Prend en entrée un entier, par exemple '23'."),
    Tool(name="Volume", func=volume, description="Règle le volume de la musique. Prend en entrée un entier entre 0 et 100, par exemple '55'."),
    Tool(name="Musique", func=musique, description="Lance une playlist. Prend en entrée le nom d'une playlist, comme 'rock'. Si le nom de la playlist n'est pas sauvegardé dans l'état de la voiture, tu dira 'Playlist inconnue' et tu ne lancera pas la musique. Si le nom de la playlist n'est pas précisé, tu lancera une playlist au hasard dans celles sauvegardées. Si l'utilsateur dit 'coupe la musique', tu appelera cette fonction avec 'aucune' comme paramètre."),
    Tool(name="Limiteur", func=limiteur_vitesse, description="Permet de modifier la vitesse (en km/h) du limiteur de vitesse. Prend en entrée un entier, par exemple '130'."),
    Tool(name="Phares", func=changer_phare, description="Permet d'activer les feux de position, de croisement ou de route. Prend en entrée 'position', 'croisement' ou 'route'."),
    Tool(name="Appeler", func=appeler_contact, description="Appelle un contact du carnet d'adresse. Prend entrée un nom de contact, par exemple 'Jean'. Si le nom du contact n'est pas sauvegardé dans l'état de la voiture, tu dira 'Contact inconnu' et tu ne lancera pas l'appel."),
    Tool(name="Raccrocher", func=raccrocher, description="Met fin à l'appel en cours. Prend en entrée toujours 'True'."),
]







# === AGENT ===

llm = ChatOpenAI(
    model="gpt-4.1-mini-2025-04-14", # "gpt-3.5-turbo-0125", "gpt-4o"
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

instructions = """Tu es un agent IA devant assister un conducteur de voiture dans ses actions. Il te dira à l'oral ce qu'il veut faire et tu devra effectuer les actions demandées.
Tu as accès à plusieurs fonction pour effectuer les actions sur la voiture. Tu dois choisir la fonction appropriée et lui passer les paramètres nécessaires. N'utilise pas de fonction si ce n'est pas nécessaire.
Tu dois vérifier que les paramètres sont valides avant d'appeler la fonction. Si ce n'est pas le cas, tu dois dire à l'utilisateur que tu ne peux pas effectuer l'action.
L'état de la voiture te sera rappelé à chaque demande de l'utilisateur. Par exemple, si l'utilisateur te demande d'aumgenter un peu la température et qu'elle est actuellement à 23 degrés, tu mettra la température à 25 degrés.
À la fin de ta réponse, ne demande pas si l'utilisateur veut faire quelque chose d'autre."""

base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)








# Initialise le moteur de synthèse vocale et de transciption audio
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text):
    print("ASSISTANT:", text)
    engine.say(text)
    engine.runAndWait() # Attendre la fin de la synthèse vocale



def listen():
    with sr.Microphone() as source:
        print("En écoute...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="fr-FR").lower()
        print("UTILISATEUR:", command)
        return command
    except sr.UnknownValueError:
        return "Je n'ai pas compris."
    except sr.RequestError:
        speak("Erreur de service de reconnaissance vocale.")
        return None



def assistant():
    global compteur
    command = listen()
    if command == "quitter":
        sys.exit()
        
    if command == "assistant":
        speak("Que puije faire pour vous ?")
        command = listen()
        
        while command == "Je n'ai pas compris.":
            speak("Je n'ai pas compris. Pouvez-vous répéter ?")
            command = listen()
        
        resultat = agent_executor.invoke({"input": f"Utilisateur: {command} \nEtat actuel de la voiture: {str(load_state())}"})
        speak(resultat["output"])
        compteur = 0












    
############### Interface graphique ###############

compteur = 0

class TableauDeBord:
    def __init__(self, root):
        self.root = root
        self.root.title("Tableau de bord voiture")
        self.root.geometry("1200x600")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg="grey15")
        self.canvas.pack()

        # Charger les icônes (prévoir des images .png dans le dossier)
        a = 20
        self.icon_feux_position = PhotoImage(file="images/feux_position.png").subsample(a+5, a+5)
        self.icon_feux_croisement = PhotoImage(file="images/feux_croisement.png").subsample(a+5, a+5)
        self.icon_feux_route = PhotoImage(file="images/feux_route.png").subsample(a+5, a+5)
        self.icon_volume = PhotoImage(file="images/volume.png").subsample(a+2, a+2)
        self.icon_vitesse = PhotoImage(file="images/vitesse.png").subsample(a, a)
        self.icon_temp = PhotoImage(file="images/temperature.png").subsample(a+4, a+4)
        self.icon_phone = PhotoImage(file="images/phone.png").subsample(a+2, a+2)
        self.dashboard = PhotoImage(file="images/dashboard.png").zoom(2, 2)
        
        # Mettre à jour l'affichage
        self.update_dashboard()
        

    def update_dashboard(self):
        global compteur
        
        self.canvas.delete("all")
        car_state = load_state()
        
        self.canvas.create_image(0, 0, image=self.dashboard, anchor="nw")
        
        # Phares
        if car_state['phares'] == "feux de position":
            self.canvas.create_oval(275, 377, 305, 407, fill="green", outline="white")
            self.canvas.create_image(280, 381, image=self.icon_feux_position, anchor="nw")
        if car_state['phares'] == "feux de croisement":
            self.canvas.create_oval(275, 377, 305, 407, fill="green", outline="white")
            self.canvas.create_image(280, 381, image=self.icon_feux_croisement, anchor="nw")
        if car_state['phares'] == "feux de route":
            self.canvas.create_oval(275, 377, 305, 407, fill="skyblue", outline="white")
            self.canvas.create_image(280, 381, image=self.icon_feux_route, anchor="nw")

        # Écran central
        if car_state['appel'] != "aucun":
            self.canvas.create_image(558, 445, image=self.icon_phone, anchor="nw")
            self.canvas.create_text(635, 457, text=f"Appel : {car_state['appel'].capitalize()}", font=("Helvetica", 16), fill="white")
        else:
            self.canvas.create_image(558, 415, image=self.icon_vitesse, anchor="nw")
            self.canvas.create_text(620, 430, text=f"{car_state['limiteur']} km/h", font=("Helvetica", 12), fill="white")

            self.canvas.create_image(560, 445, image=self.icon_volume, anchor="nw")
            self.canvas.create_text(610, 458, text=f"{car_state['volume']}%", font=("Helvetica", 12), fill="white")
            
            self.canvas.create_image(560, 475, image=self.icon_temp, anchor="nw")
            if car_state['climatisation'] == "On":
                self.canvas.create_text(607, 486, text=f"{car_state['temperature']}°", font=("Helvetica", 12), fill="white")
            else:
                self.canvas.create_text(607, 486, text="Off", font=("Helvetica", 12), fill="white")
                
        # Compteur pour éviter la non mise à jour de l'UI
        if compteur > 1:
            assistant()
        compteur += 1
            
        # Rafraîchir automatiquement toutes les 0.5 secondes
        self.root.after(500, self.update_dashboard) # attend 2s ici puis reload




if __name__ == "__main__":
    root = tk.Tk()
    app = TableauDeBord(root)
    root.mainloop()






# Confirmation orale de l'action à effectuer
# Mettre une musique de rock