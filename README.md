# HOG DETECTOR

![image](https://github.com/th3k3y/hogpersondetector/assets/49789253/fbb90937-a57f-48a3-a749-6f8ca78a4892)

# Script de Détection de Personnes

Ce script de détection de personnes est un script Python qui utilise la technologie de détection de personnes basée sur le Descripteur d'Objets HOG (Histogram of Oriented Gradients). 

La détection de personnes basée sur HOG est une méthode populaire pour détecter les objets d'apparences humaines dans n'importe quel type de média tels que les images et les vidéos. Elle repose sur la caractérisation des formes des humains à partir des gradients d'intensité des pixels. Le descripteur HOG extrait des informations sur les orientations locales des gradients dans une image, ce qui permet de représenter les formes des humains de manière distinctive. Cette technologie est relativement simple ce qui fait qu'elle n'est pas extrêmement précise, cela dit, elle fonctionne dans la plupart des cas.

L'algorithme utilise ensuite un classificateur SVM (Support Vector Machine) pré-entraîné avec des exemples positifs et négatifs pour détecter les personnes dans l'image. Une fois qu'une personne est détectée, le script envoie une alerte via un webhook Discord, fournissant une image de la personne détectée ainsi que l'heure de la détection.

## Instructions d'utilisation

1. Assurez-vous d'avoir installé les dépendances requises répertoriées dans le fichier `requirements.txt`.
2. Obtenez un lien de webhook Discord pour recevoir les alertes de détection de personnes.
3. Exécutez le script `person_detection.py` en spécifiant le webhook URL en tant qu'argument.
4. Lorsque le script est en cours d'exécution, vous pouvez sélectionner un fichier vidéo pour le traitement en utilisant l'interface utilisateur graphique (GUI).
5. Le script détectera automatiquement les personnes dans la vidéo, encadrera les personnes détectées et enverra des alertes via le webhook Discord.
6. Une fois le traitement terminé, fermez la fenêtre de l'aperçu en utilisant la touche ESC et le script sera prêt à détecter des personnes dans un autre fichier vidéo ou à être fermé.


