import csv
import easygui
import sqlite3
import logging


# Ouverture et lecture du fichier Historique de la banque
myFile = easygui.fileopenbox("Selection du fichier à importer", default="C:/Users/henri/OneDrive/Documents/06 Banques/")
print(myFile)
CSVFile = open(myFile, 'r')
reader = csv.DictReader(CSVFile, delimiter=';')

# Ouverture de la base de donnée
conn = sqlite3.connect('C:/Users/henri/OneDrive/Documents/06 Banques/Transactions.db')

cur = conn.cursor()

# Insérer une ligne de données
# On Parse et on met dans la base données
DateOperation = "Date de l'opération"

# cur.execute("Delete from TransactionsList ")
# conn.commit()
for row in reader:
    Beneficiaire = row["contrepartie"].strip(" ")
    if (Beneficiaire == ""):
        Beneficiaire = row["nom du terminal"].strip(" ")
    if (Beneficiaire == ""):
        Beneficiaire = row["description du type d'opération"].strip(" ")

    # Modifie le contenu des champs pour les accents
    myBeneficiaire = Beneficiaire.replace("'", " ")
    Beneficiaire.replace("é", "e")
    Beneficiaire.replace("è", "e")
    Beneficiaire.replace("à", "a")
    Beneficiaire.replace("^é", "e")
    Beneficiaire.replace("Retrait", "RETRAIT")

    Donnees = row["date de l'opération"] + "','" + myBeneficiaire + "'," + row["montant"].replace(',', ".") + ",1"
    print(Donnees)

    try:
        # Insere la Transaction
        cur.execute(
            "INSERT INTO TransactionsList (`DateOperation`,`Contrepartie`,`Montant`,`Status`) VALUES ('" + Donnees + ")")

        conn.commit()
        Donnees = Beneficiaire + "',0,0"
        try:
            cur.execute("INSERT INTO Contrepartie (`Nom`,`Category`,`ID`) VALUES ('" + Donnees + ")")
            conn.commit()
        except:
            print("Erreur Insertion Contrepartie ", Beneficiaire)
    except:
        logging.exception('Erreur Insertion')
        print(myBeneficiaire)
