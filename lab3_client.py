# Client
def creerMessage():

    message=""
    for i in range(20):
        print("Entrer un entier")
        e=input()
        if (i!=19):
            message+=str(e)+","
        else:
            message+=str(e)
    
    return message

