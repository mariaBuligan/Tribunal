-- Inserții pentru tabela Sectie
INSERT INTO Sectie (Nume, Tribunal) VALUES 
('Penal', 'Bucuresti'),
('Civil', 'Deva'),
('Litigii de munca', 'Deva'),
('Contencios', 'Timisoara');

-- Inserții pentru tabela Complet
INSERT INTO Complet (Sectie_id, Nume_Presedinte, Data_infiintare, Sala) VALUES 
(1, 'Ion Popescu', '2020-01-01', 101),
(1, 'Maria Ionescu', '2021-03-15', 102),
(2, 'George Marinescu', '2019-05-10', 201),
(4, 'Ana Georgescu', '2022-06-20', 202),
(3, 'Vasile Dumitru', '2023-08-25', 301);

-- Inserții pentru tabela Angajat
INSERT INTO Angajat (Tip, Nume, Prenume, Vechime, Salariu, Complet_id) VALUES 
('Judecător', 'Ion', 'Popescu', 5, 8000.00, 1),
('Judecător', 'Maria', 'Ionescu', 10, 10000.00, 2),
('Judecător', 'George', 'Marinescu', 3, 7000.00, 3),
('Judecător', 'Ana', 'Georgescu', 4, 7500.00, 4),
('Judecător', 'Vasile', 'Dumitru', 8, 10000.00, 5),
('Judecător', 'Alexandru', 'Petrescu', 5, 8000.00, 1),
('IT', 'Cristina', 'Vlad', 3, 7500.00, null),
('Grefier', 'Daniel', 'Popa', 2, 3000.00, null),
('Grefier', 'Elena', 'Marin', 4, 3200.5, null),
('Judecător', 'Ioana', 'Radu', 1, 7000.00, 3);



-- Inserții pentru tabela Persoana
INSERT INTO Persoana (Nume, Prenume, Adresa, Telefon, Tip) VALUES 
('Mihai', 'Ionescu', 'Str. Primăverii, nr. 5', '0723456789', 'R'),
('Andreea', 'Popescu', 'Str. Libertății, nr. 10', '0787654321', 'P'),
('Florin', 'Dumitru', 'Str. Unirii, nr. 20', '0712345678', 'R'),
('Laura', 'Pavăl', 'Str. Moșneagului, nr. 15', '0732167890', 'P'),
('Gabriela', 'Matei', 'Str. Nucilor, nr. 30', '0776996941', 'R');

-- Inserții pentru tabela Locatie
INSERT INTO Locatie (Nr_camera, Nr_raft, Nr_nivel) VALUES 
(65, 1, 1),
(66, 2, 1),
(65, 1, 2),
(65, 3, 2),
(67, 1, 3);

-- Inserții pentru tabela Dosar
INSERT INTO Dosar (Termen, Stadiu, Complet_id, Locatie_id) VALUES 
('2024-01-10', 'fond', 1, 1),
('2024-02-15', 'apel', 1, 2),
('2024-03-20', 'fond', 2, 3),
('2024-04-25', 'recurs', 3, 4),
('2024-05-30', 'recurs', 4, 5);

-- Inserții pentru tabela Pers_Dosar
INSERT INTO Pers_Dosar (Persoana_id, Dosar_id) VALUES 
(1, 1),
(2, 2),
(1, 3),
(3, 4),
(4, 5);

-- Inserții pentru tabela Mandat
INSERT INTO Mandat (Dosar_id, Tip) VALUES 
(1, 'Arest'),
(2, 'Perchezitie'),
(3, 'Arest preventiv'),
(4, 'Dare plata'),
(5, 'Dare Frontiera');

INSERT INTO Users(Username,Parola) VALUES
('MariaBuligan','1234'),
('Gabriel16','1234');

SELECT name,state_desc FROM sys.databases WHERE name = 'Tribunal';

SELECT * From Users;



