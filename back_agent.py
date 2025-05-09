import os
import json
from langchain import hub
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from typing import Any

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
        state["temperature"] = temp
        save_state(state)
        return f"Température réglée à {temp} degrés.\n"
    except ValueError:
        return "Je n'ai pas compris la température demandée."

def volume(vol: int):
    try:
        volume = min(100, max(0, int(vol)))
        state = load_state()
        state["volume"] = volume
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
        state["limiteur"] = vitesse
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
L'état de la voiture te sera rappelé à chaque demande de l'utilisateur. Par exemple, si l'utilisateur te demande d'aumgenter un peu la température et qu'elle est actuellement à 23 degrés, tu mettra la température à 25 degrés."""

base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)





if __name__ == "__main__":
    print("Assistant voiture IA - Entrez une commande (ou 'exit')")
    
    while True:
        command = input("\nVous: ")
        if command == "exit":
            break
        agent_executor.invoke({"input": f"Utilisateur: {command} \nEtat actuel de la voiture: {str(load_state())}"})








#  Confirmation orale de l'action à effectuer


