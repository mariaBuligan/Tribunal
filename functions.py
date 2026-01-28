import PySimpleGUI as sg

def create_start_window():
    layout_start = [
        [sg.Button("Create Account")],
        [sg.Button("Login")]
    ]
    return sg.Window("Bun venit la Tribunal", layout_start, size=(400, 200))

def create_login_window():
    layout_login = [
        [sg.Text("Username:"), sg.Input(key="username_login", size=(20, 1))],
        [sg.Text("Password:"), sg.Input(key="parola_login", size=(20, 1),password_char="*")],
        [sg.Button("Sign IN"), sg.Button("Back")]
    ]
    return sg.Window("Sign IN", layout_login, size=(400, 200))

def create_menu_window():
    layout_menu = [
        [sg.Combo(["VIZUALIZEAZA", "UPDATEAZA", "STERGE", "INTRODUCE","CAUTA"], key="combo")],
        [sg.Button("Submit")]
    ]
    return sg.Window("Menu", layout_menu, size=(800, 300), resizable=True, finalize=True)

def check_user(u,p, event, cursor):
    if event == "Login":
        cursor.execute(f"SELECT Parola FROM Users WHERE Username = ?",u)
        rows = cursor.fetchone()
        if not rows:
            sg.popup("The User does not exist", title="ERROR")
        elif rows[0] == p:
            return 1
        else: sg.popup("Incorect password", title="ERROR")

    elif event == "Create Account":
        try:
            cursor.execute("INSERT INTO Users (Username, Parola) VALUES (?, ?);", (u, p))
            return 1
        except:
            sg.popup("This username already has an account!", title="ERROR")

    return 0

def command(value):
        if value == "VIZUALIZEAZA":
            return "SELECT"
        elif value == "UPDATEAZA":
            return "UPDATE"
        elif value == "STERGE":
            return "DELETE"
        elif value == "INTRODUCE":
            return "INSERT"


def find_all_ids(tabel,cursor):
    cursor.execute(f"Select {tabel}_id FROM {tabel};")
    rows = cursor.fetchall()
    ids = [row[0] for row in rows]  #turn it into a vector
    return ids

def find_all_sectii(cursor):
    cursor.execute("Select DISTINCT S.Nume From Sectie S;")
    rows = cursor.fetchall()
    sectii = [row[0] for row in rows]
    return sectii

def get_all_columns(tabel, cursor):
    cursor.execute(f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{tabel}');")
    column_names = [desc[0] for desc in cursor.fetchall()]
    return column_names

def get_column_values(tabel,id, cursor):
    cursor.execute(f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{tabel}')  AND is_identity = 0;")
    column_names = [desc[0] for desc in cursor.fetchall()]
    cursor.execute(f"SELECT {', '.join(column_names)} FROM {tabel} WHERE {tabel}_id = {id};")
    column_values = cursor.fetchone()
   
    return dict(zip(column_names, column_values))    

#   SELECT 
def handle_select(window, cursor):
    # Layout suplimentar pentru SELECT
    layout_select = [
        [sg.Text("Selectați tabelul pentru vizualizare:")],
        [sg.Combo(["Sectie", "Complet", "Dosar", "Angajat", "Persoana", "Mandat", "Locatie"],key="tabel")],
        [sg.Button("Selecteaza")]
    ]
    window.extend_layout(window, layout_select)

    while True:
        event_select, values_select = window.read()
        if event_select in (sg.WINDOW_CLOSED, None):
            break  
        if event_select == "Selecteaza":
            tabel = values_select.get("tabel")
            if tabel:  
                Select_query(tabel, cursor)

def Select_query(tabel,cursor):
        cursor.execute(f"Select * FROM {tabel};")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]
        result = "";
        for row in rows:
            for col_name, value in zip(column_names, row):
                result+= f"{col_name}: {value}\n"
            result+= "-" * 20 + "\n";
        sg.popup_scrolled(result, title="Query Results")
        return;

#   UPDATE 
def handle_update(window, cursor):
    layout_select = [
        [sg.Text("Selectați tabelul care vreti sa il editati:")],
        [sg.Combo(["Sectie", "Complet", "Dosar", "Angajat", "Persoana", "Mandat", "Locatie"],key="tabel")],
        [sg.Button("Selecteaza")]
    ]
    window.extend_layout(window, layout_select)

    while True:
        event1, value1 = window.read()
        if event1 in (sg.WINDOW_CLOSED, None): break
        if event1 == "Selecteaza":
            tabel = value1["tabel"]
            if tabel:
                ids = find_all_ids(tabel,cursor)
                window.extend_layout(window, [[sg.Spin(ids,size = (10,1),key="id_spin")],[sg.Button("Selecteaza ID")]])
            
        if event1 == "Selecteaza ID":
            id = value1["id_spin"]
            Update_query(window,tabel,id,cursor)

def Update_query(window,tabel,id,cursor):
    column_data = get_column_values(tabel, id, cursor)

    layout = [
        [sg.Text(f"{col_name}: "), sg.Input(default_text=col_value, key=col_name)]
        for col_name, col_value in column_data.items()  ]
    layout.append([sg.Button("Save"), sg.Button("Cancel")])
    window.extend_layout(window,layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            return None  # User canceled
        if event == "Save":
            set_clause = ", ".join([f"{col} = '{values[col]}'" for col in column_data.keys()])
            sql_update = f"UPDATE {tabel} SET {set_clause} WHERE {tabel}_id = {id};"
            cursor.execute(sql_update)
            sg.popup("Database updated successfully")
            return

#   DELETE 
def handle_delete(window,cursor):
    layout_select = [
        [sg.Text("Selectați tabelul din care vreti sa stergeti:")],
        [sg.Combo(["Sectie", "Complet", "Dosar", "Angajat", "Persoana", "Mandat", "Locatie"],key="tabel")],
        [sg.Button("Selecteaza")]
    ]
    window.extend_layout(window, layout_select)

    while True:
        event1, value1 = window.read()
        if event1 in (sg.WINDOW_CLOSED, None): break
        if event1 == "Selecteaza":
            tabel = value1["tabel"]
            if tabel:
                ids = find_all_ids(tabel,cursor)
                window.extend_layout(window, [[sg.Spin(ids,size = (10,1),key="id_spin")],[sg.Button("Delete")]])
            
        if event1 == "Delete":
            id = value1["id_spin"]
            cursor.execute(f"DELETE FROM {tabel} WHERE {tabel}_id={id};")
            return 


#   INSEERT 
def dublicate(tabel,valori, coloane, cursor):
    conditions = " AND ".join([f"{coloane[i]} = '{valori[i]}'" for i in range(len(valori))])
    sql_queue = f"SELECT * FROM {tabel} WHERE {conditions};"
    cursor.execute(sql_queue)
    rows = cursor.fetchone()

    if not rows:
        return 1
    else: return 0

def handle_insert(window,cursor):
    layout_select = [
        [sg.Text("Selectați tabelul in care vreti sa inserati:")],
        [sg.Combo(["Sectie", "Complet", "Dosar", "Angajat", "Persoana", "Mandat", "Locatie"],key="tabel")],
        [sg.Button("Selecteaza")]
    ]
    window.extend_layout(window, layout_select)

    while True:
        event1, value1 = window.read()
        if event1 in (sg.WINDOW_CLOSED, None): break
        if event1 == "Selecteaza":
            tabel = value1["tabel"]
            if tabel:
                 Insert_query(window,tabel, cursor);

def Insert_query(window,tabel, cursor):
    columns = get_all_columns(tabel,cursor); columns = columns[1:];

    layout = [
        [sg.Text(f"{col_name}: "), sg.Input(key=col_name)]
        for col_name in columns ]
    layout.append([sg.Button("Save"), sg.Button("Cancel")])
    window.extend_layout(window,layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            return None  # User canceled
        if event == "Save":
            col_names = ", ".join(columns)
            set_clause = ", ".join([f"'{values[col]}'" for col in columns])
            if(dublicate(tabel, [values[col] for col in columns], columns, cursor)):
                sql_update = f"INSERT INTO {tabel} ({col_names}) VALUES ({set_clause});"
                cursor.execute(sql_update)
                sg.popup("Insersion successfully")
                return
            else: sg.popup("These entries already exist")