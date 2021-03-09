from datetime import datetime

def writeError(Pyfile, error):
    
    now = datetime.now();
    occurenceTime = now.strftime("%d/%m/%Y - %H:%M:%S")
    
    try:
        with open("errorlog.txt", 'a') as file:
            file.writelines(occurenceTime + " - in " + Pyfile + " - " + str(error) + "\n")
    except FileNotFoundError:
        with open("errorlog.txt", 'w') as file:
            file.writelines(occurenceTime + " - in " + Pyfile + " - " + str(error) + "\n")
            