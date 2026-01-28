SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('Complet'); AND is_identity = 0;

INSERT INTO Pers_Dosar(Persoana_id,Dosar_id) VALUES (5,1)

Select * FROM Dosar;
SELECT * FROM Pers_Dosar;
SELECT * FROM Locatie;
SELECT * FROM Persoana;
SELECT * FROM Complet;
SELECT * FROM Sectie;
SELECT * FROM Angajat;
SELECT * FROM Mandat;
Select DISTINCT S.Nume From Sectie S;


SELECT Nume,Prenume ,Adresa,Telefon FROM Persoana P
JOIN Pers_Dosar PD ON P.Persoana_id=PD.Persoana_id
JOIN Dosar D ON PD.Dosar_id=D.Dosar_id
WHERE P.Tip = 'R' AND D.Dosar_id = 1;

SELECT DISTINCT A.Nume,A.Prenume FROM Angajat A
JOIN Complet C ON A.Complet_id = C.Complet_id
WHERE C.Complet_id = 1;

SELECT Mandat_id,Tip, Termen FROM Mandat M 
JOIN Complet C on C.Complet_id = D.Complet_id
WHERE D.Dosar_id = 1003;

SELECT Nr_camera,Nr_raft,Nr_nivel FROM Locatie L 
JOIN Dosar D ON L.Locatie_id = D.Locatie_id
JOIN Complet C on C.Complet_id = D.Complet_id
WHERE D.Complet_id = '1';

SELECT Adresa, Telefon, D.Dosar_id, Termen, Stadiu, Tip From Persoana P
JOIN Pers_Dosar PD ON P.Persoana_id = PD.Persoana_id
JOIN Dosar D ON PD.Dosar_id = D.Dosar_id
WHERE P.Nume = 'el' and P.Prenume = 'Ionescu'

SELECT A.Nume, A.Prenume, S.Nume From Angajat A
JOIN Complet C ON A.Complet_id = C.Complet_id
JOIN Sectie S ON C.Sectie_id = S.Sectie_id
WHERE S.Tribunal = 'Bucuresti';

SELECT A.Nume, A.Prenume From Angajat A
WHERE A.Tribunal = 'Bucuresti' AND Complet_id IS NULL;

SELECT D.Dosar_id, D.Stadiu, D.Termen 
FROM Dosar D 
WHERE D.Complet_id IN (
    SELECT C.Complet_id 
    FROM Complet C 
    WHERE C.Sectie_id IN (
        SELECT S.Sectie_id 
        FROM Sectie S 
        WHERE S.Sectie_id = C.Sectie_id AND C.Nume_Presedinte = 'Ion Popescu'
    )
);

SELECT COUNT(*)
FROM Dosar D
WHERE D.Complet_id IN 
      (SELECT C.Complet_id 
       FROM Complet C 
       WHERE C.Sectie_id IN 
             (SELECT S.Sectie_id 
              FROM Sectie S 
              WHERE S.Tribunal = 'Bucuresti'));

SELECT D.Dosar_id, D.Stadiu, D.Termen 
FROM Dosar D 
WHERE D.Termen < '2024-01-25' 
  AND D.Complet_id IN (
      SELECT C.Complet_id 
      FROM Complet C 
      WHERE C.Sectie_id IN (
          SELECT S.Sectie_id 
          FROM Sectie S 
          WHERE C.Nume_presedinte = 'Ion Popescu'
      )
  );

SELECT A.Nume, A.Prenume, A.Salariu, A.Tribunal, A.Vechime 
FROM Angajat A 
WHERE A.Salariu > (
    SELECT AVG(A2.Salariu) 
    FROM Angajat A2 
    WHERE A2.Complet_id IN (
        SELECT C.Complet_id 
        FROM Complet C 
        WHERE C.Sectie_id IN (
            SELECT S.Sectie_id 
            FROM Sectie S 
            WHERE S.Nume = 'civil'
        )
    )
);


SELECT AVG(A.Salariu) FROM Angajat A 
JOIN Complet C ON A.Complet_id = C.Complet_id 
JOIN Sectie S ON C.Sectie_id = S.Sectie_id WHERE S.Nume = 'penal';

