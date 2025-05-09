import json
import time
import streamlit as st

# Charger les données depuis le fichier JSON

with open("voiture.json", "r", encoding="utf-8") as f:
    etat = json.load(f)

# Interface Streamlit
st.set_page_config(page_title="Tableau de bord de la voiture", layout="centered")
st.title("🚗 Tableau de bord de la voiture")

# Affichage des états
st.subheader("🎛️ Statut actuel")
st.markdown(f"**♨️ Climatisation :** {etat['climatisation']}")
st.markdown(f"**🎚️ Température :** {etat['temperature']} °C")
st.markdown(f"**🚄 Limiteur de vitesse :** {etat['limiteur_vitesse']} km/h")
st.markdown(f"**💡 Phares :** {etat['phares']}")
st.markdown(f"**🎵 Playlist :** {etat['musique']}")
st.markdown(f"**🔊 Volume :** {etat['volume']} / 100")
st.markdown(f"**📞 Appel en cours :** {etat['appel']}")

# Affichage des contacts
st.subheader("👥 Contacts disponibles")
for contact in etat.get("contacts", []):
    st.markdown(f"- {contact.capitalize()}")
    
# Affichage des playlists
st.subheader("🎶 Playlists disponibles")
for song in etat.get("playlists", []):
    st.markdown(f"- {song.capitalize()}")



# Déclencher le rafraîchissement après un court délai
time.sleep(2)
st.rerun()


# # Mise à jour de l'état
# if etat != ancien_etat:
#     st.rerun()
    
# ancien_etat = etat









# st.subheader("🔧 Modifier l'état de la voiture")
# # Climatisation
# climatisation = st.selectbox("Climatisation", ["On", "Off"], index=0 if etat["climatisation"] == "On" else 1)
# etat["climatisation"] = climatisation

# # Température
# temperature = st.slider("Température (°C)", min_value=16, max_value=30, value=etat["temperature"])
# etat["temperature"] = temperature

# # Limiteur de vitesse
# limiteur_vitesse = st.slider("Limiteur de vitesse (km/h)", min_value=0, max_value=200, value=etat["limiteur_vitesse"])
# etat["limiteur_vitesse"] = limiteur_vitesse

# # Phares
# phares = st.selectbox("Phares", ["Feux de position", "Feux de croisement", "Feux de route"], index=["Feux de position", "Feux de croisement", "Feux de route"].index(etat["phares"]))
# etat["phares"] = phares

# # Volume
# volume = st.slider("Volume", min_value=0, max_value=100, value=etat["volume"])
# etat["volume"] = volume