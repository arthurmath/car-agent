# import json

# def charger_etat():
#     with open("etat.json", "r", encoding="utf-8") as f:
#         return json.load(f)

# def sauvegarder_etat(car_state):
#     with open("etat.json", "w", encoding="utf-8") as f:
#         json.dump(car_state, f, indent=4, ensure_ascii=False)

# # Exemple d'utilisation :
# etat = charger_etat()
# print(etat)
# etat["volume"] = 80
# print(etat)
# sauvegarder_etat(etat)





import tkinter as tk
import time


def assistant():
    print("assistant")
    time.sleep(5)
    print("assistant fin")


class TableauDeBord:
    def __init__(self, root):
        self.root = root
        self.root.title("Tableau de bord voiture")
        self.root.geometry("1200x600")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg="grey15")
        self.canvas.pack()

        # Mettre à jour l'affichage
        self.update_dashboard()

    def update_dashboard(self):
        print("update")
 
        assistant()
            
        print("update fin") 
        # Rafraîchir automatiquement toutes les 0.5 secondes
        self.root.after(500, self.update_dashboard) # attend 2s ici puis reload




if __name__ == "__main__":
    root = tk.Tk()
    app = TableauDeBord(root)
    root.mainloop()
