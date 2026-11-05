-- vérification des données 
SELECT * FROM pizzas LIMIT 10;

SELECT * FROM pizza_types LIMIT 10;

SELECT * FROM orders LIMIT 10;

SELECT * FROM order_details LIMIT 10;


-- vérification du nombres de lignes
SELECT COUNT(*) AS nombre_pizzas FROM pizzas;

SELECT COUNT(*) AS nombre_types FROM pizza_types;

SELECT COUNT(*) AS nombre_commandes FROM orders;

SELECT COUNT(*) AS nombre_details FROM order_details;


-- Vérifier le noms des colonnes et leurs types
PRAGMA table_info(pizzas);
PRAGMA table_info(pizza_types);
PRAGMA table_info(orders);
PRAGMA table_info(order_details);


-- jointure test entre pizzas et pizza_types
SELECT
    p.pizza_id,
    pt.name,
    pt.category,
    p.size,
    p.price
FROM pizzas AS p
JOIN pizza_types AS pt
    ON p.pizza_type_id = pt.pizza_type_id
LIMIT 10;



-- vue axe ventes (jointure entre les quatres tables)
DROP VIEW IF EXISTS vue_ventes;
CREATE VIEW vue_ventes AS
SELECT
    od.order_details_id,
    o.order_id,
    o.date,
    o.time,
    pt.name AS pizza_name,
    pt.category,
    p.size,
    p.price,
    od.quantity,
    p.price * od.quantity AS chiffre_affaires
FROM order_details AS od
JOIN orders AS o
    ON od.order_id = o.order_id
JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id
JOIN pizza_types AS pt
    ON p.pizza_type_id = pt.pizza_type_id;

SELECT * FROM vue_ventes LIMIT 10;





-- AXE 1 : PERFORMANCE GLOBALE DE LA PIZZERIA

-- CA TOTAL (817 860,05 $)
SELECT ROUND(SUM(chiffre_affaires), 2) AS ca_total 
FROM vue_ventes;

-- NOMBRE DE COMMANDES PASSÉES (21 350)
SELECT COUNT(DISTINCT order_id) AS nombre_commandes
FROM vue_ventes;

-- NOMBRE DE PIZZAS VENDUES AU TOTAL (49 574)
SELECT SUM(quantity) AS quantite_totale_vendue
FROM vue_ventes;

-- PANIER MOYEN (38,31 $)
SELECT ROUND(AVG(ca_commande), 2) AS panier_moyen
FROM (SELECT
		order_id,
        SUM(chiffre_affaires) AS ca_commande
    	FROM vue_ventes
    	GROUP BY order_id);





-- AXE 2 : PERFORMANCE DES PRODUITS

-- TOP 10 DES PIZZAS VENDUES (EN QUANTITÉ)
SELECT
    pizza_name,
    SUM(quantity) AS quantite_vendue
FROM vue_ventes
GROUP BY pizza_name
ORDER BY quantite_vendue DESC
LIMIT 10;

-- TOP 10 DES PIZZAS QUI GÉNERENT LE PLUS DE CA
SELECT
    pizza_name,
    ROUND(SUM(chiffre_affaires), 2) AS ca_total
FROM vue_ventes
GROUP BY pizza_name
ORDER BY ca_total DESC
LIMIT 10;

-- TOP 10 DES PIZZAS PAR CA : COMPARAISON AVEC LE VOLUME VENDU
SELECT
    pizza_name,
    SUM(quantity) AS quantite,
    ROUND(SUM(chiffre_affaires), 2) AS ca
FROM vue_ventes
GROUP BY pizza_name
ORDER BY ca DESC
LIMIT 10;

-- CATÉGORIE DE PIZZAS QUI GÉNERENT LE PLUS DE CA
SELECT
    category,
    ROUND(SUM(chiffre_affaires), 2) AS ca_total
FROM vue_ventes
GROUP BY category
ORDER BY ca_total DESC;

-- TAILLE DE PIZZA LA PLUS COMMANDÉE
SELECT
    size,
    SUM(quantity) AS quantite_vendue
FROM vue_ventes
GROUP BY size
ORDER BY quantite_vendue DESC;

-- CA PAR TAILLE DE PIZZA
SELECT
    size,
    SUM(quantity) AS quantite_vendue,
    ROUND(SUM(chiffre_affaires), 2) AS ca_total,
    ROUND(AVG(price), 2) AS prix_moyen
FROM vue_ventes
GROUP BY size
ORDER BY ca_total DESC;






-- AXE 3 : ANALYSE TEMPORELLE DES VENTES

-- ÉVOLUTION DU CA MENSUEL
SELECT
    strftime('%Y-%m', date) AS mois,
    ROUND(SUM(chiffre_affaires), 2) AS ca_mensuel
FROM vue_ventes
GROUP BY mois
ORDER BY mois;

-- JOURS QUI GÉNERENT LE PLUS DE COMMANDES
SELECT
    CASE strftime('%w', date)
        WHEN '0' THEN 'Dimanche'
        WHEN '1' THEN 'Lundi'
        WHEN '2' THEN 'Mardi'
        WHEN '3' THEN 'Mercredi'
        WHEN '4' THEN 'Jeudi'
        WHEN '5' THEN 'Vendredi'
        WHEN '6' THEN 'Samedi'
    END AS jour_semaine,
    COUNT(DISTINCT order_id) AS nombre_commandes
FROM vue_ventes
GROUP BY strftime('%w', date)
ORDER BY nombre_commandes DESC;

-- PANIER MOYEN PAR JOUR DE SEMAINE 
SELECT
    CASE strftime('%w', date)
        WHEN '0' THEN 'Dimanche'
        WHEN '1' THEN 'Lundi'
        WHEN '2' THEN 'Mardi'
        WHEN '3' THEN 'Mercredi'
        WHEN '4' THEN 'Jeudi'
        WHEN '5' THEN 'Vendredi'
        WHEN '6' THEN 'Samedi'
    END AS jour_semaine,
    ROUND(AVG(ca_commande), 2) AS panier_moyen
FROM (
    SELECT
        order_id,
        date,
        SUM(chiffre_affaires) AS ca_commande
    FROM vue_ventes
    GROUP BY order_id, date
)
GROUP BY strftime('%w', date)
ORDER BY strftime('%w', date);

-- HEURES OU LES COMMANDES SONT LES PLUS NOMBREUSES
SELECT
    strftime('%H', time) AS heure,
    COUNT(DISTINCT order_id) AS nombre_commandes
FROM vue_ventes
GROUP BY heure
ORDER BY nombre_commandes DESC;

-- ZONES CREUSES PAR JOUR ET HEURES
SELECT
    CASE strftime('%w', date)
        WHEN '0' THEN 'Dim'
        WHEN '1' THEN 'Lun'
        WHEN '2' THEN 'Mar'
        WHEN '3' THEN 'Mer'
        WHEN '4' THEN 'Jeu'
        WHEN '5' THEN 'Ven'
        WHEN '6' THEN 'Sam'
    END AS jour,
    strftime('%H', time) AS heure,
    COUNT(DISTINCT order_id) AS nb_cmd
FROM vue_ventes
GROUP BY
    strftime('%w', date),
    strftime('%H', time)
ORDER BY
    CAST(strftime('%w', date) AS INTEGER),
    CAST(strftime('%H', time) AS INTEGER);

-- PIZZAS LES MOINS VENDUES
SELECT
    pizza_name,
    SUM(quantity) AS quantite_vendue
FROM vue_ventes
GROUP BY pizza_name
ORDER BY quantite_vendue ASC
LIMIT 10;

-- PANIER MOYEN PAR CRÉNEAU HORAIRE 
SELECT 
		strftime('%H', time) AS heure,
		COUNT(DISTINCT order_id) AS nb_cmd, 
		SUM(quantity*price)/COUNT(DISTINCT order_id) AS panier_moyen
FROM vue_ventes GROUP BY heure ORDER BY heure;

-- VOLUME VS PANIER 
SELECT
    strftime('%Y-%m', date) AS mois,
    COUNT(DISTINCT order_id) AS nb_commandes,
    ROUND(SUM(chiffre_affaires), 2) AS ca_mensuel,
    ROUND(SUM(chiffre_affaires) / COUNT(DISTINCT order_id), 2) AS panier_moyen
FROM vue_ventes
GROUP BY mois
ORDER BY mois;




