CREATE TABLE Marche(
   id COUNTER,
   libelle VARCHAR(50) ,
   posX INT,
   posY INT,
   longueur DECIMAL(15,2)  ,
   largeur DECIMAL(15,2)  ,
   prix_m2 DECIMAL(15,2)  ,
   PRIMARY KEY(id)
);

CREATE TABLE Box(
   id COUNTER,
   libelle VARCHAR(50) ,
   posX INT,
   posY INT,
   longueur DECIMAL(15,2)  ,
   largeur DECIMAL(15,2)  ,
   id_marche INT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(id_marche) REFERENCES Marche(id)
);

CREATE TABLE Facture(
   id COUNTER,
   montant_paye DECIMAL(15,2)  ,
   reste_a_payer DECIMAL(15,2)  ,
   date_facturation DATE,
   id_box INT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(id_box) REFERENCES Box(id)
);

CREATE TABLE Paiement(
   id COUNTER,
   montant DECIMAL(15,2)  ,
   date_paiement DATE,
   id_facture INT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(id_facture) REFERENCES Facture(id)
);
