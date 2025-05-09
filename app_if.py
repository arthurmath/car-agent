import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import PhotoImage
import json
import sys



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
    print("ASSISTANT:", text)
    # engine.say(text)
    # engine.runAndWait() # Attendre la fin de la synthèse vocale



def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("En écoute...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="fr-FR").lower()
        print("UTILISATEUR:", command)
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

    elif "limiteur" in command or "vitesse" in command:
        for word in command.split():
            if word.isdigit():
                speed = int(word)
                car_state["limiteur_vitesse"] = speed
                save_state(car_state)
                speak(f"Limiteur de vitesse réglé à {speed} km/h.")

    elif "phares" in command.split() or "feux" in command.split():
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

    elif "playlist" in command.split() or "musique" in command.split():
        if "arrête" in command.split() or "stop" in command.split():
            car_state["musique"] = "aucune"
            save_state(car_state)
            speak("Playlist arrêtée.")
        elif "lance" in command.split() or "mets" in command.split():
            car_state["musique"] = "playlist lancée"
            save_state(car_state)
            speak("Playlist lancée.")

    elif "volume" in command.split():
        for word in command.split():
            if word.isdigit():
                volume = int(word)
                car_state["volume"] = min(100, max(0, volume))
                save_state(car_state)
                speak(f"Volume réglé à {volume}%.")

    elif "appelle" in command.split():
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



def assitant():
    command = listen()
    if command == "quitter":
        sys.exit()
        
    if command == "assistant":
        speak("Bonjour, que puije faire pour vous ?")
        command = listen()
        process_command(command)
        









    
############### Interface graphique ###############

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
        self.canvas.delete("all")
        car_state = load_state()
        
        self.canvas.create_image(0, 0, image=self.dashboard, anchor="nw")

        if car_state['appel'] != "aucun":
            self.canvas.create_image(558, 415, image=self.icon_vitesse, anchor="nw")
            self.canvas.create_text(400, 50, text=f"Appel en cours : {car_state['appel'].capitalize()}", font=("Helvetica", 16), fill="white")
            
        else:
            self.canvas.create_image(558, 415, image=self.icon_vitesse, anchor="nw")
            self.canvas.create_text(620, 430, text=f"{car_state['limiteur_vitesse']} km/h", font=("Helvetica", 12), fill="white")

            self.canvas.create_image(560, 445, image=self.icon_volume, anchor="nw")
            self.canvas.create_text(610, 458, text=f"{car_state['volume']}%", font=("Helvetica", 12), fill="white")
            
            self.canvas.create_image(560, 475, image=self.icon_temp, anchor="nw")
            if car_state['climatisation'] == "On":
                self.canvas.create_text(607, 486, text=f"{car_state['temperature']}°", font=("Helvetica", 12), fill="white")
            else:
                self.canvas.create_text(607, 486, text="Off", font=("Helvetica", 12), fill="white")

            if car_state['phares'] == "feux de position":
                self.canvas.create_oval(275, 377, 305, 407, fill="green", outline="white")
                self.canvas.create_image(280, 381, image=self.icon_feux_position, anchor="nw")
            if car_state['phares'] == "feux de croisement":
                self.canvas.create_oval(275, 377, 305, 407, fill="green", outline="white")
                self.canvas.create_image(280, 381, image=self.icon_feux_croisement, anchor="nw")
            if car_state['phares'] == "feux de route":
                self.canvas.create_oval(275, 377, 305, 407, fill="skyblue", outline="white")
                self.canvas.create_image(280, 381, image=self.icon_feux_route, anchor="nw")
                
        assitant()
            
        # Rafraîchir automatiquement toutes les 2 secondes
        self.root.after(2000, self.update_dashboard)





if __name__ == "__main__":
    root = tk.Tk()
    app = TableauDeBord(root)
    root.mainloop()






