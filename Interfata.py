import pyodbc
import PySimpleGUI as sg
import functions as f
import cautari as f2

server = 'localhost' ; database = 'Tribunal' ; username = 'SA' ; password = 'My@StrongPass123' ;

db_connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=" + server + ";Database=" + database + ";UID=" + username + ";PWD=" + password + ";""TrustServerCertificate=yes;"
conn = pyodbc.connect(db_connection_string, autocommit=True);
cursor = conn.cursor()

window_start = f.create_start_window()

while True:
    event, values = window_start.read()
    if event == sg.WINDOW_CLOSED: break
    if event:
        window_login = f.create_login_window()
        while True:
            event_login, values_login = window_login.read()
            if event_login in (sg.WINDOW_CLOSED,"Back"):
                window_login.close()
                window_start.close()
                window_start = f.create_start_window()
                break

            if event_login == "Sign IN":
                user = values_login["username_login"]
                parola = values_login["parola_login"]
                if f.check_user(user,parola,event,cursor) == 1:
                    sg.popup("Sign IN successful!", title="SUCCESS")
                    window_login.close()
                    window_start.close()
                    window_menu = f.create_menu_window()

                    while True:
                        event, values_menu = window_menu.read()
                        if event == sg.WINDOW_CLOSED: break
                        
                        if event == "Submit":
                            opt = values_menu["combo"]
                            opt = f.command(opt)
                            
                            if opt == "SELECT": f.handle_select(window_menu, cursor)
                            elif opt == "UPDATE": f.handle_update(window_menu, cursor)
                            elif opt == "DELETE": f.handle_delete(window_menu,cursor)
                            elif opt == "INSERT": f.handle_insert(window_menu,cursor)
                            else: f2.handle_cautare(window_menu,cursor)

                            window_menu = f.create_menu_window()
                            window_menu.TKroot.deiconify()
