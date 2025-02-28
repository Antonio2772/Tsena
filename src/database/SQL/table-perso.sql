-- Ajout d'une table Locataire pour enregistrer les informations des locataires
CREATE TABLE Locataire(
   id COUNTER PRIMARY KEY,
   nom VARCHAR(100),
   prenom VARCHAR(100),
   telephone VARCHAR(20),
   email VARCHAR(100),
   adresse VARCHAR(255)
);

-- Ajout d'une table Contrat qui lie un box à un locataire
CREATE TABLE Contrat(
   id COUNTER PRIMARY KEY,
   date_debut DATE,
   date_fin DATE,
   montant_loyer CURRENCY,
   caution CURRENCY,
   periodicite VARCHAR(50),
   statut VARCHAR(20),
   id_box INT NOT NULL,
   id_locataire INT NOT NULL
);

-- Ajouter les contraintes de clé étrangère séparément après la création de la table
ALTER TABLE Contrat ADD CONSTRAINT fk_box 
   FOREIGN KEY (id_box) REFERENCES Box(id);

ALTER TABLE Contrat ADD CONSTRAINT fk_locataire 
   FOREIGN KEY (id_locataire) REFERENCES Locataire(id);

-- Modification de la table Facture pour lier au contrat au lieu du box
ALTER TABLE Facture ADD COLUMN id_contrat INT;
ALTER TABLE Facture ADD CONSTRAINT fk_contrat 
   FOREIGN KEY(id_contrat) REFERENCES Contrat(id);