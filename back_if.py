import json
import speech_recognition as sr
import pyttsx3


def load_state():
    with open("voiture.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(car_state):
    with open("voiture.json", "w", encoding="utf-8") as f:
        json.dump(car_state, f, indent=4, ensure_ascii=False)

car_state = load_state()






# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait() # Attendre la fin de la synthèse vocale





def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("En écoute...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="fr-FR").lower()
        print("Utilisateur:", command)
        return command
    except sr.UnknownValueError:
        speak("Je n'ai pas compris. Pouvez-vous répéter ?")
        return None
    except sr.RequestError:
        speak("Erreur de service de reconnaissance vocale.")
        return None



def process_command(command):
    if not command:
        return

    if "clim" in command or "climatisation" in command:
        if "active" in command.split() or "met" in command.split():
            car_state["climatisation"] = "On"
            save_state(car_state)
            speak(f"Climatisation activée à {car_state['temperature']} degrés.")
        elif "désactive" in command.split() or "coupe" in command.split():
            car_state["climatisation"] = "Off"
            save_state(car_state)
            speak("Climatisation désactivée.")

    elif "température" in command:
        for word in command.split():
            if word.replace("°", "").isdigit():
                temp = int(word)
                car_state["temperature"] = temp
                save_state(car_state)
                speak(f"Température réglée à {temp} degrés.")

    elif "limiteur" in command:
        for word in command.split():
            if word.isdigit():
                speed = int(word)
                car_state["limiteur_vitesse"] = speed
                save_state(car_state)
                speak(f"Limiteur de vitesse réglé à {speed} km/h.")

    elif "phares" in command or "feux" in command:
        if "position" in command:
            car_state["phares"] = "feux de position"
            save_state(car_state)
        elif "croisement" in command:
            car_state["phares"] = "feux de croisement"
            save_state(car_state)
        elif "route" in command or "plein phares" in command:
            car_state["phares"] = "feux de route"
            save_state(car_state)
        speak(f"{car_state['phares'].capitalize()} activés.")

    elif "playlist" in command:
        car_state["musique"] = "playlist lancée"
        save_state(car_state)
        speak("Playlist lancée.")

    elif "volume" in command:
        for word in command.split():
            if word.isdigit():
                volume = int(word)
                car_state["volume"] = min(100, max(0, volume))
                save_state(car_state)
                speak(f"Volume réglé à {volume}.")

    elif "appelle" in command:
        for contact in car_state["contacts"]:
            if contact in command:
                car_state["appel"] = contact
                save_state(car_state)
                speak(f"J'appelle {contact.capitalize()}.")
                return
        speak("Contact non trouvé.")
        
    elif "raccroche" in command:
        car_state["appel"] = "aucun"
        save_state(car_state)
        speak("Appel terminé.")

    else:
        speak("Commande non reconnue.")



def main():
    speak("Bonjour, que puije faire pour vous ?")
    while True:
        command = listen()
        if command == "quitter":
            break
        process_command(command)

if __name__ == "__main__":
    main()




