import cv2
import requests
import datetime
import os
from tkinter import filedialog, Tk, Label, Button, messagebox
import threading
from tkinter import ttk


class DetecteurPersonne:
    def __init__(self, webhook_url):
        self.HOGCV = cv2.HOGDescriptor()
        self.HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.webhook_url = webhook_url
        self.fenetre = None
        self.preview_ouvert = False
        self.bouton_selectionner_fichier = None

    def envoyer_alerte(self, chemin_image, heure_detection):
        données = {
            "contenu": f"PERSONNE DÉTECTÉE À {heure_detection}",
        }
        with open(chemin_image, "rb") as fichier:
            fichiers = {
                "fichier": (chemin_image, fichier),
            }
            réponse = requests.post(self.webhook_url, data=données, files=fichiers)
        os.remove(chemin_image)

    def traiter_vidéo(self, chemin_fichier):
        cap = cv2.VideoCapture(chemin_fichier)

        def rappel_fermeture(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.preview_ouvert = False

        cv2.namedWindow("preview")
        cv2.setMouseCallback("preview", rappel_fermeture)

        while True:
            succès, frame = cap.read()
            if succès:
                frame = cv2.resize(frame, (640, 480))
                boites, poids = self.HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

                for (x, y, w, h), poids in zip(boites, poids):
                    if poids > 0.6:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame, "PERSONNE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        horodatage = datetime.datetime.now()
                        chemin_img = f"{horodatage.strftime('%Y-%m-%d-%H-%M-%S')}.png"
                        img_recadrée = frame[y:y+h, x:x+w]
                        cv2.imwrite(chemin_img, img_recadrée)
                        self.envoyer_alerte(chemin_img, horodatage)

                cv2.imshow("preview", frame)
                self.preview_ouvert = True

            touche = cv2.waitKey(1)
            if touche == 27 or not self.preview_ouvert:
                break

        cap.release()
        cv2.destroyAllWindows()

        self.fenetre.event_generate("<<PreviewFermée>>")

    def sélectionner_fichier(self):
        try:
            chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4;*.avi")])
            if chemin_fichier:
                self.bouton_selectionner_fichier.configure(state="disabled")
                threading.Thread(target=self.démarrer_traitement, args=(chemin_fichier,), daemon=True).start()
            else:
                messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def démarrer_traitement(self, chemin_fichier):
        try:
            self.traiter_vidéo(chemin_fichier)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


class InterfaceUtilisateur:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Script de Détection de Personnes")
        self.fenetre.configure(bg="#252525")

        style = ttk.Style()
        style.theme_use("default")

        etiquette_bienvenue = Label(self.fenetre, text="Détection HOG", font=("Arial", 16), bg="#252525", fg="white")
        etiquette_bienvenue.pack(pady=20)

        self.detecteur = DetecteurPersonne(webhook_url)
        self.detecteur.fenetre = self.fenetre
        self.detecteur.bouton_selectionner_fichier = ttk.Button(self.fenetre, text="Sélectionner un fichier vidéo", command=self.detecteur.sélectionner_fichier)
        self.detecteur.bouton_selectionner_fichier.pack()

        style.configure("TButton", foreground="white", background="#2975D1", font=("Arial", 14), padding=10)
        style.map("TButton", background=[("active", "#1C4C8C"), ("disabled", "#606060")])

        self.fenetre.bind("<<PreviewFermée>>", self.sur_fermeture_preview)

    def sur_fermeture_preview(self, event):
        self.detecteur.bouton_selectionner_fichier.configure(state="normal")


if __name__ == "__main__":
    webhook_url = "https://discord.com/api/webhooks/1101906867065720883/5VzXSBM0hrbfuILGtwXO8paXHcu9hD_gGNDPaLnPCYkQlSADNKY3VbF16ruS-SH2ursa"
    fenetre = Tk()
    interface = InterfaceUtilisateur(fenetre)
    fenetre.mainloop()
