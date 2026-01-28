import PySimpleGUI as sg
import functions as f

def handle_cautare(window,cursor):
    ids_complete = f.find_all_ids("Complet",cursor)
    ids_dosare = f.find_all_ids("Dosar",cursor)
    sectii = f.find_all_sectii(cursor)

    layout = [
    [sg.Text('Toate partile din Dosarul:'), sg.Spin(ids_dosare,size = (10,1),key="1"), sg.Button('Search', key= 'Join1')],
    [sg.Text('Toti judecatorii din Completul:'), sg.Spin(ids_complete,size = (10,1),key="2"),sg.Button('Search', key= 'Join2')],
    [sg.Text('Toate Mandatele din Dosarul:'), sg.Spin(ids_dosare,size = (10,1),key="3"), sg.Button('Search', key= 'Join3')],
    [sg.Text('Locatiile asociate Completului:'),sg.Spin(ids_complete,size = (10,1),key="4"),sg.Button('Search', key= 'Join4')],
    [sg.Text('Cauta Persoana (nume | prenume):'), sg.Input(key='5', size=(9, 1)),sg.Input(key='13', size=(9, 1)),sg.Button('Search', key= 'Join5')],
    [sg.Text('Angajatii din fiecare Sectie din Orasul:'), sg.Input(key='6', size=(9, 1)), sg.Button('Search', key= 'Join6')],

    [sg.Text('Toate Dosarele Judecatorului (nume | prenume):'), sg.Input(key='7', size=(9, 1)),sg.Input(key='14', size=(9, 1)), sg.Button('Search', key= 'Complex1')],
    [sg.Text('Numarul de Dosare de la Tribunalul'), sg.Input(key='8', size=(9, 1)), sg.Button('Search', key= 'Complex2')],
    [sg.Text('Dosarele care au termenul înainte de data și apartin judecatorului(nume | prenume | yyyy-mm-dd ):'), sg.Input(key='9', size=(9, 1)),sg.Input(key='11', size=(9, 1)),sg.Input(key='12', size=(9, 1)),sg.Button('Search', key= 'Complex3')],
    [sg.Text('Angajatii care au salariu mai mare decat media din Sectia:'),sg.Spin(sectii,size = (10,1),key="10"), sg.Button('Search', key= 'Complex4')],
    ]

    window.extend_layout(window, layout)

    while True:
        event,value  = window.read()
        if event in (sg.WINDOW_CLOSED, None): break
        if event == 'Join1': 
            id = value["1"]
            join1(id,cursor)
        elif event == 'Join2':
            id = value["2"]
            join2(id,cursor)
        elif event == 'Join3': 
            id = value["3"]
            join3(id,cursor)
        elif event == 'Join4': 
            id = value["4"]
            join4(id,cursor)
        elif event == 'Join5':
            nume = value["5"]; prenume = value["13"]
            join5(nume,prenume,cursor)
        elif event == 'Join6':
            oras = value["6"];
            join6(oras,cursor)
        elif event == 'Complex1':
            nume = value["7"]; prenume = value["14"]
            complex1(nume,prenume,cursor)
        elif event == 'Complex2':
            nume = value["8"]
            complex2(nume,cursor) 
        elif event == 'Complex3': 
            nume = value["9"]; prenume = value["11"]; data = value["12"]
            complex3(nume,prenume,data,cursor)
        else: 
            nume = value["10"]
            complex4(nume,cursor)
    
    return


def join1(id, cursor):
    reclamanti = f"SELECT Nume,Prenume ,Adresa,Telefon FROM Persoana P JOIN Pers_Dosar PD ON P.Persoana_id=PD.Persoana_id JOIN Dosar D ON PD.Dosar_id=D.Dosar_id WHERE P.Tip = 'R' AND D.Dosar_id = {id};"
    parati = f"SELECT Nume,Prenume ,Adresa,Telefon FROM Persoana P JOIN Pers_Dosar PD ON P.Persoana_id=PD.Persoana_id JOIN Dosar D ON PD.Dosar_id=D.Dosar_id WHERE P.Tip = 'P' AND D.Dosar_id = {id};"

    cursor.execute(reclamanti); rows1 = cursor.fetchall()
    cursor.execute(parati); rows2 = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    result = "RECLAMANTI:\n";
    for row in rows1:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    result += "PÂRÂȚI:\n";
    for row in rows2:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def join2(id, cursor):
    nume = f"SELECT DISTINCT Nume,Prenume FROM Angajat A JOIN Complet C ON A.Complet_id = C.Complet_id WHERE C.Complet_id = {id};"
    presedinte = f"SELECT Nume_Presedinte FROM Complet WHERE Complet_id = {id};"

    cursor.execute(nume); rows = cursor.fetchall()
    cursor.execute(presedinte); pres = cursor.fetchone();
    nume_pres,prenume_pres = pres[0].split()
    
    result = "NUME    PRENUME\n\n"
    for row in rows:
        if(row[0] == nume_pres and row[1] == prenume_pres):
            result+= f"{row[0]} {row[1]} (presedinte)"
        else: result+= f"{row[0]} {row[1]}"
        result+="\n" + "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def join3(id, cursor):
    mandate = f"SELECT Mandat_id,Tip, Termen FROM Mandat M JOIN Dosar D ON M.Dosar_id = D.Dosar_id WHERE D.Dosar_id = {id};"
    cursor.execute(mandate); rows = cursor.fetchall()
    if not rows:
        sg.popup_scrolled("Dosarul selectat nu are mandate!", title="Query Results")
        return;

    column_names = [description[0] for description in cursor.description[:-1]]
    result = f"Termen de Judecata:{rows[0][2]}\n\n"
    for row in rows:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def join4(id, cursor):
    locatii = f"SELECT Nr_camera,Nr_raft,Nr_nivel FROM Locatie L JOIN Dosar D ON L.Locatie_id = D.Locatie_id WHERE Complet_id = {id};"
    cursor.execute(locatii); rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    result = ""
    for row in rows:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def join5(nume,prenume, cursor):
    info = """SELECT Adresa, Telefon, D.Dosar_id, Termen, Stadiu, Tip FROM Persoana P JOIN Pers_Dosar PD ON P.Persoana_id = PD.Persoana_id JOIN Dosar D ON PD.Dosar_id = D.Dosar_id WHERE P.Nume = ? AND P.Prenume = ?;"""
    cursor.execute(info,prenume,nume); rows = cursor.fetchall()

    result=f"{nume.upper()} {prenume.upper()}\n\n"
    if rows:
        result+= f"Adresa: {rows[0][0]}\n"
        result+= f"Telefon:{rows[0][1]}\n"
        result+= "-" * 20 + "\n";

        column_names = [description[0] for description in cursor.description[2:]]
        for row in rows:
            for col_name, value in zip(column_names, row[2:]):
                result+= f"{col_name}: {value}\n"
            result+= "-" * 20 + "\n";
    else: result+= "Name not Found!!\n"
    sg.popup_scrolled(result, title="Query Results")
    return

def join6(oras, cursor):
    sql1 = f"SELECT A.Nume, A.Prenume, S.Nume From Angajat A JOIN Complet C ON A.Complet_id = C.Complet_id JOIN Sectie S ON C.Sectie_id = S.Sectie_id WHERE S.Tribunal = '{oras}';"
    sql2 = f"SELECT A.Nume, A.Prenume, A.Tip From Angajat A WHERE A.Tribunal = '{oras}' AND Complet_id IS NULL;"
    cursor.execute(sql1); rows1 = cursor.fetchall()
    cursor.execute(sql2); rows2 = cursor.fetchall()

    if  not rows1 and not rows2: result = "Orasul introdus nu exista in baza noastra de date!\n"
    if rows1 or rows2:
        result = "NUME   PRENUME \n"
        if rows1:
            for row in rows1:
                result += f"{row[0]} {row[1]} -> {row[2]} \n "
        if rows2:    
            for row in rows2:
                result += f"{row[0]} {row[1]} -> {row[2]}\n"

    sg.popup_scrolled(result, title="Query Results")
    return

def complex1(nume,prenume,cursor):
    dosare = f"SELECT D.Dosar_id, D.Stadiu, D.Termen FROM Dosar D WHERE D.Complet_id IN (SELECT C.Complet_id FROM Complet C WHERE C.Nume_Presedinte = '{prenume} {nume}');"
    cursor.execute(dosare)
    rows = cursor.fetchall()

    if not rows:
        sg.popup_scrolled("Nu a fost gasit judeecatorul cautat!\n", title="Query Results")
        return
    
    column_names = [description[0] for description in cursor.description]
    result = ""
    for row in rows:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def complex2(nume,cursor):
    dosare = f"SELECT COUNT(*) FROM Dosar D WHERE D.Complet_id IN (SELECT C.Complet_id FROM Complet C WHERE C.Sectie_id IN (SELECT S.Sectie_id FROM Sectie S WHERE S.Tribunal = '{nume}'));"
    cursor.execute(dosare)
    rows = cursor.fetchone()

    result = f"Numarul de dosare din {nume}: {rows[0]}\n"
    sg.popup_scrolled(result, title="Query Results")
    return

def complex3(nume,prenume,data,cursor):
    dosare = f"SELECT D.Dosar_id, D.Stadiu, D.Termen FROM Dosar D WHERE D.Termen < '{data}' AND D.Complet_id = (SELECT C.Complet_id FROM Complet C WHERE C.Nume_presedinte = '{prenume} {nume}');"
    cursor.execute(dosare)
    rows = cursor.fetchall()
    if not rows:
        sg.popup_scrolled("Nu a fost gasit nici un dosar!\n", title="Query Results")
        return
    
    column_names = [description[0] for description in cursor.description]
    result = ""
    for row in rows:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return

def complex4(nume,cursor):
    ang = f"SELECT A.Nume, A.Prenume, A.Salariu, A.Tribunal, A.Vechime FROM Angajat A WHERE A.Salariu > (SELECT AVG(A2.Salariu) FROM Angajat A2 JOIN Complet C ON A2.Complet_id = C.Complet_id JOIN Sectie S ON C.Sectie_id = S.Sectie_id WHERE S.Nume = '{nume}');"
    medie = f"SELECT AVG(A.Salariu) FROM Angajat A JOIN Complet C ON A.Complet_id = C.Complet_id JOIN Sectie S ON C.Sectie_id = S.Sectie_id WHERE S.Nume = '{nume}';"
    cursor.execute(medie); rows2 = cursor.fetchone()
    cursor.execute(ang); rows1 = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    result = f"Media sectiei: {rows2[0]:.2f} \n\n"
    for row in rows1:
        for col_name, value in zip(column_names, row):
            result+= f"{col_name}: {value}\n"
        result+= "-" * 20 + "\n";
    
    sg.popup_scrolled(result, title="Query Results")
    return