CREATE DATABASE Tribunal;

CREATE TABLE Sectie(
    Sectie_id int identity(1,1) NOT NULL,
    Nume nvarchar(50) NOT NULL,
    Tribunal nvarchar(50),

    CONSTRAINT PK_Sectie PRIMARY KEY (Sectie_id)
)

CREATE TABLE Complet(
    Complet_id int identity(1,1) NOT NULL,
    Sectie_id int NOT NULL,
    Nume_Presedinte nvarchar(50) NOT NULL,
    Data_infiintare DATE,
    Sala int,

    CONSTRAINT PK_Complet PRIMARY KEY (Complet_id),
    CONSTRAINT FK_Complet FOREIGN KEY (Sectie_id) REFERENCES Sectie(Sectie_id)
)

CREATE TABLE Angajat(
    Angajat_id int identity(1,1) NOT NULL,
    Tip nvarchar(20) NOT NULL,
    Nume nvarchar(20) NOT NULL,
    Prenume nvarchar(20) NOT NULL,
    Vechime int,
    Salariu DECIMAL(8,2),
    Complet_id int,

    CONSTRAINT PK_Angajat PRIMARY KEY (Angajat_id),
    CONSTRAINT FK_Angajat FOREIGN KEY (Complet_id) REFERENCES Complet(Complet_id)
)

CREATE TABLE Persoana(
    Persoana_id int identity(1,1) NOT NULL,
    Nume nvarchar(20) NOT NULL,
    Prenume nvarchar(20) NOT NULL,
    Adresa nvarchar(100),
    Telefon char(10),
    Tip char(1) NOT NULL,

    CONSTRAINT PK_Persoana PRIMARY KEY (Persoana_id),
    CONSTRAINT CHK_Tip CHECK(Tip = 'R' OR Tip = 'P')  --Reclamant sau Parat--
)

CREATE TABLE Locatie(
    Locatie_id int identity(1,1) NOT NULL,
    Nr_camera int NOT NULL,
    Nr_raft int NOT NULL,
    Nr_nivel int NOT NULL,

    CONSTRAINT PK_Locatie PRIMARY KEY (Locatie_id)
)

CREATE TABLE Dosar(
    Dosar_id int identity(1,1) NOT NULL,
    Termen DATE,
    Stadiu nvarchar(10) NOT NULL,
    Complet_id int NOT NULL,
    Locatie_id int NOT NULL,

    CONSTRAINT PK_Dosar PRIMARY KEY (Dosar_id),
    CONSTRAINT FK_DosarC FOREIGN KEY (Complet_id) REFERENCES Complet(Complet_id),
    CONSTRAINT FK_DosarL FOREIGN KEY (Locatie_id) REFERENCES Locatie(Locatie_id)
)

CREATE TABLE Pers_Dosar(
    Persoana_id int NOT NULL,
    Dosar_id int NOT NULL

    CONSTRAINT FK_DosarP FOREIGN KEY (Persoana_id) REFERENCES Persoana(Persoana_id),
    CONSTRAINT FK_DosarD FOREIGN KEY (Dosar_id) REFERENCES Dosar(Dosar_id)
)

CREATE TABLE Mandat(
    Mandat_id int identity(1,1) NOT NULL,
    Dosar_id int NOT NULL,
    Tip nvarchar(20) NOT NULL,

    CONSTRAINT PK_Mandat PRIMARY KEY (Mandat_id),
    CONSTRAINT FK_Dosar FOREIGN KEY (Dosar_id) REFERENCES Dosar(Dosar_id)
)

CREATE TABLE Users(
    Username nvarchar(50) NOT NULL,
    Parola nvarchar(20) NOT NULL ,

    CONSTRAINT UQ_Users UNIQUE (Username)
)