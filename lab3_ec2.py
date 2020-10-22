# EC2
 
import statistics
# Parser pour récupérer le message sous forme d'une liste d'entiers
def parser(message):
    liste=message.split(",")
    listeEntiers=[]
    for i in range(len(liste)):
        listeEntiers.append(int(liste[i]))
    listeEntiers.sort()
    #print(listeEntiers)
    return(listeEntiers)
    
    
# Calcul du minimum
def minimum(listeEntiers):
    return listeEntiers[0]

# Calcul du maximum
def maximum(listeEntiers):
    return listeEntiers[-1]

# Calcul de la moyenne
def moyenne(listeEntiers):
    return statistics.mean(listeEntiers)
    
# Calcul de la mediane
def mediane(listeEntiers):
    return statistics.median(listeEntiers)