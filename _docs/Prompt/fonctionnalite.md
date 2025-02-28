Je vais analyser les tables de votre base de données et vous proposer des requêtes SQL pour atteindre vos objectifs.

D'après votre schéma de base de données, vous avez quatre tables principales :
- `Marche` : contient les informations sur les marchés (emplacement, dimensions, prix au m²)
- `Box` : représente les boxes disponibles dans un marché
- `Facture` : enregistre les factures émises pour la location des boxes
- `Paiement` : garde trace des paiements effectués pour chaque facture

Voici les requêtes que vous pouvez utiliser pour obtenir les informations souhaitées :

## 1. Voir le reste à payer pour un box donné :

```sql
SELECT b.id AS id_box, b.libelle AS nom_box, f.id AS id_facture, 
       f.date_facturation, f.reste_a_payer
FROM Box b
JOIN Facture f ON b.id = f.id_box
WHERE b.id = [ID_DU_BOX]
ORDER BY f.date_facturation DESC;
```

## 2. Montant payé pour un mois et une année donnés pour un box :

```sql
SELECT b.id AS id_box, b.libelle AS nom_box,
       SUM(p.montant) AS montant_total_paye
FROM Box b
JOIN Facture f ON b.id = f.id_box
JOIN Paiement p ON f.id = p.id_facture
WHERE b.id = [ID_DU_BOX]
AND MONTH(p.date_paiement) = [MOIS]
AND YEAR(p.date_paiement) = [ANNEE]
GROUP BY b.id, b.libelle;
```

## 3. Montant à payer par mois pour un box :

Pour cette requête, je suppose que le montant à payer par mois correspond au prix du marché au m² multiplié par la surface du box :

```sql
SELECT b.id AS id_box, b.libelle AS nom_box,
       m.prix_m2 * (b.longueur * b.largeur) AS montant_mensuel
FROM Box b
JOIN Marche m ON b.id_marche = m.id
WHERE b.id = [ID_DU_BOX];
```

Ces requêtes vous permettent d'obtenir les informations demandées. Cependant, je note quelques points qui pourraient être améliorés dans votre modèle de données :

1. Il manque une table ou un champ pour définir clairement la périodicité des paiements (mensuel, trimestriel, etc.)
2. Il serait utile d'avoir un champ "montant_total" dans la table Facture
3. Vous pourriez envisager d'ajouter une table "Contrat" qui lierait un box à un locataire

Avez-vous besoin d'autres requêtes ou souhaitez-vous des modifications sur celles que je vous ai proposées ?