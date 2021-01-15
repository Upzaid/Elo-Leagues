import sqlite3
from tkinter import *
from tkinter.ttk import *
from datetime import date
from matplotlib import pyplot as plt


# OPEN NEW LEAGUE WINDOW


def open_add_new_league():
    new_league_window = Toplevel()
    new_league_window.title("Add a New League")
    new_league_window.geometry("280x180")
    new_league_window.resizable(width=False, height=False)

    league_name = Label(new_league_window, text='League Name')
    league_name.place(relx=1 / 5, rely=1 / 5, anchor=CENTER)

    league_name_entry = Entry(new_league_window)
    league_name_entry.place(relx=3 / 5, rely=1 / 5, anchor=CENTER)

    k_value_lbl = Label(new_league_window, text="Select K Value")
    k_value_lbl.place(relx=1 / 5, rely=2 / 5, anchor=CENTER)

    k_value_entry = Combobox(new_league_window, width=5, values=(8, 16, 24, 32, 48))
    k_value_entry.place(relx=3 / 5, rely=2 / 5, anchor=CENTER)

    # ADD NEW LEAGUE TO THE LEAGUES LIST DATABASE

    def submit_new_league():
        conn = sqlite3.connect('League List.db')
        c = conn.cursor()

        c.execute("INSERT INTO leagues VALUES(:league_name, :k_value)",
                  {
                      'league_name': league_name_entry.get(),
                      'k_value': k_value_entry.get(),
                  })

        league_name_entry.delete(0, END)
        k_value_entry.delete(0, END)

        conn.commit()
        conn.close()

    submit_new_league = Button(new_league_window, text='Submit', command=submit_new_league)
    submit_new_league.place(relx=1 / 2, rely=4 / 5, anchor=CENTER)

# OPEN SELECTED LEAGUE WINDOW


def open_league():
    league = leagues_combobox.get()
    league_selection_window.destroy()

# FIND K VALUE FOR RATING FORMULA

    conn = sqlite3.connect('League List.db')
    c = conn.cursor()

    parameter = "'" + league + "'"

    c.execute("SELECT k_value FROM leagues WHERE league_name= %s;" % parameter)

    k = c.fetchall()[0][0]

    conn.commit()
    conn.close()

    root.geometry("480x380")
    root.title("Zaid's Elo Program")
    root.resizable(width=False, height=False)

    top_players = Label(root, text="Top Players")
    top_players.grid(column=0, row=0, columnspan=3, rowspan=1, pady=10)

# CREATE TOP PLAYERS TREE

    top_players_tree = Treeview(root, columns="2")
    top_players_tree.grid(column=0, row=1, columnspan=3, rowspan=2, padx=10, pady=10)

    top_players_tree.heading("#0", text="Rank    Player")
    top_players_tree.column("0", width=10)
    top_players_tree.heading("2", text="Rating")
    top_players_tree.column("2", width=100)

# CONNECT TO SELECTED LEAGUE DATABASE

    conn = sqlite3.connect(league + '.db')
    c = conn.cursor()

# POPULATE TOP PLAYERS TREE

    c.execute("""CREATE TABLE IF NOT EXISTS players (
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city TEXT,
            state TEXT,
            country TEXT,
            rating REAL,
            matches INTEGER
            )
            """)

    c.execute("SELECT first_name, last_name, rating FROM players ORDER BY rating DESC;")
    players = c.fetchall()

    conn.commit()
    conn.close()

    i = 0
    for player in players:
        i += 1
        top_players_tree.insert("", i, text=str(i) + " " + player[0] + " " + player[1], values=(round(player[2], 1)))

# CREATE NEW PLAYER WINDOW

    def open_new_player_window():
        new_player_window = Toplevel()
        new_player_window.title("Add a New Player")
        new_player_window.geometry("240x240")
        new_player_window.resizable(width=False, height=False)

        first_name_lbl = Label(new_player_window, text="First Name")
        first_name_lbl.grid(column=0, row=0, padx=5, pady=5)
        first_name = Entry(new_player_window, width=15)
        first_name.grid(column=1, row=0, padx=10, pady=5)

        last_name_lbl = Label(new_player_window, text="Last Name")
        last_name_lbl.grid(column=0, row=1, padx=5, pady=5)
        last_name = Entry(new_player_window, width=15)
        last_name.grid(column=1, row=1, padx=10, pady=5)

        city_lbl = Label(new_player_window, text="City")
        city_lbl.grid(column=0, row=2, padx=5, pady=5)
        city = Entry(new_player_window, width=15)
        city.grid(column=1, row=2, padx=5, pady=5)

        state_lbl = Label(new_player_window, text="State")
        state_lbl.grid(column=0, row=3, padx=5, pady=5)
        state = Entry(new_player_window, width=15)
        state.grid(column=1, row=3, padx=5, pady=5)

        country_lbl = Label(new_player_window, text="Country")
        country_lbl.grid(column=0, row=4, padx=5, pady=5)
        country = Entry(new_player_window, width=15)
        country.grid(column=1, row=4, padx=5, pady=5)

        def submit_new_player():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

# INSERT PLAYER INFORMATION INTO "PLAYERS" TABLE

            c.execute("INSERT INTO players VALUES(:first_name, :last_name, :city, :state, :country, 1200, 0)",
                      {
                          'first_name': first_name.get(),
                          'last_name': last_name.get(),
                          'city': city.get(),
                          'state': state.get(),
                          'country': country.get(),
                      })

            print(c.lastrowid)
            last_oid = c.lastrowid

            c.execute("""CREATE TABLE IF NOT EXISTS %s (
                            opponent text,
                            result text,
                            rating_delta real,
                            rating,
                            date text)
                            ;""" % ('table' + str(last_oid)))

            first_name.delete(0, END)
            last_name.delete(0, END)
            city.delete(0, END)
            state.delete(0, END)
            country.delete(0, END)

            conn.commit()
            conn.close()

        submit_button = Button(new_player_window, text="Submit", command=submit_new_player)
        submit_button.grid(column=1, row=6, pady=20)

    def open_history():
        conn = sqlite3.connect(league + '.db')
        c = conn.cursor()

        history_window= Toplevel()
        history_window.title("History")
        history_window.geometry("530x555")
        history_window.resizable(width=False, height=False)

        player_list_label = Label(history_window, text="Player List")
        player_list_label.grid(column=0, row=0, columnspan=2, pady=(10, 0))

        player_list_tree = Treeview(history_window, columns=("2", "3", "4"))
        player_list_tree.grid(column=0, row=1, columnspan=2, padx=(15, 0), pady=10)

        player_list_tree["columns"] = ("2", "3", "4")
        player_list_tree.heading("#0", text="ID")
        player_list_tree.column("#0", width=40)
        player_list_tree.heading("2", text="First Name")
        # player_list_tree.column("#2", width=80)
        player_list_tree.heading("3", text="Last Name")
        # player_list_tree.column("3", width=100)
        player_list_tree.heading("4", text="Matches")
        player_list_tree.column("4", width=60)

# INSERT PLAYERS LIST TO PLAYER TREE

        c.execute("SELECT oid, first_name, last_name FROM players")
        player_list = c.fetchall()

        x = 0
        for player in player_list:
        # COUNT MATCHES AND INSERT IN EACH ROW
            c.execute("SELECT COUNT (*) FROM table%s;" % (player[0]))
            matches = c.fetchall()
            x += 1
            player_list_tree.insert("", x, text=str(player[0]),
                                    values=(str(player[1]), str(player[2]), str(matches[0][0])))

        player_history_label = Label(history_window, text="Player History")
        player_history_label.grid(column=0, row=2, columnspan=2, pady=10)

        player_history_tree = Treeview(history_window, columns=("2", "3", "4", "5"))
        player_history_tree.grid(column=0, row=3, padx=(10, 0))
        player_history_tree["columns"] = ("2", "3", "4", "5")
        player_history_tree.heading("#0", text="Opponent")
        player_history_tree.column("0", width=5)
        player_history_tree.heading("2", text="Result")
        player_history_tree.column("2", width=50)
        player_history_tree.heading("3", text="Rating Δ")
        player_history_tree.column("3", width=60)
        player_history_tree.heading("4", text="Rating")
        player_history_tree.column("4", width=60)
        player_history_tree.heading("5", text="Date")
        player_history_tree.column("5", width=70)

# DOUBLE CLICK ON PLAYERS LIST BIND FUNCTION

        def click_player_list_tree(event):

            player_history_tree.delete(*player_history_tree.get_children())

            # print(player_list_tree.identify_column(event.x))
            # print(player_list_tree.identify_column(event.y))

            curItem = player_list_tree.item(player_list_tree.focus())
            # print(curItem)
            # print(curItem['text'])
            graph_title = curItem['values'][0] + " " + curItem['values'][1]

            oid = curItem['text']

            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("SELECT * FROM table%s;" % oid)
            player_history = c.fetchall()

            # print(player_history)
            x = 0
            dev_x = [0]
            dev_y = [1200]

            for row in player_history:
                x += 1
                player_history_tree.insert("", x, text=row[0], values=(row[1], round(row[2]), round(row[3], 1), row[4]))
                dev_x.append(x)
                # print(dev_x)

                dev_y.append(round(row[3], 1))
                # print(dev_y)

# CREATE ASSOCIATED GRAPH

            plt.close()
            plt.plot(dev_x, dev_y, '-d')
            plt.title(graph_title)
            plt.xlabel('Match Number')
            plt.ylabel('Rating')
            plt.grid(True)
            plt.show()

            conn.commit()
            conn.close()

        player_list_tree.bind("<Double-Button-1>", click_player_list_tree)

        conn.commit()
        conn.close()

    def open_match():
        match_window = Toplevel()
        match_window.title("Match")
        match_window.geometry("420x180")
        match_window.resizable(width=False, height=False)

        player_1_id = Entry(match_window, width=5)
        player_1_id.place(relx=3 / 10, rely=1 / 8, anchor=CENTER)
        player_1_id.insert(END, "P1 ID")

        player_2_id = Entry(match_window, width=5)
        player_2_id.place(relx=7 / 10, rely=1 / 8, anchor=CENTER)
        player_2_id.insert(END, "P2 ID")

        vs_lbl = Label(match_window)

        def submit_player_ids():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_1_id.get())))
            p1_data = c.fetchall()
            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_2_id.get())))
            p2_data = c.fetchall()

            vs_lbl['text'] = str(p1_data[0][0] + " " + p1_data[0][1] + "  V.S.  " + p2_data[0][0] + " " + p2_data[0][1])
            vs_lbl.place(relx=0.5, rely=1 / 3, anchor=CENTER)

            conn.commit()
            conn.close()

        submit_players_button = Button(match_window, text="Submit IDs", command=submit_player_ids)
        submit_players_button.place(relx=0.5, rely=1 / 2, anchor=CENTER)

        def p_1_win():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_1_id.get())))
            p1_data = c.fetchall()
            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_2_id.get())))
            p2_data = c.fetchall()

            p1_rating = p1_data[0][5]
            # print(p1_rating)

            p2_rating = p2_data[0][5]
            # print(p2_rating)

            p1_prob = (pow(10, p1_rating / 400)) / (pow(10, p1_rating / 400) + pow(10, p2_rating / 400))
            # print(p1_prob)

            p2_prob = (pow(10, p2_rating / 400)) / (pow(10, p2_rating / 400) + pow(10, p1_rating / 400))
            # print(p2_prob)

            p1_rating_change = k * (1 - p1_prob)
            p2_rating_change = (-1) * p1_rating_change

            p1_rating_new = p1_rating + p1_rating_change
            p2_rating_new = p2_rating + p2_rating_change

            # print(p1_rating_new)
            # print(p2_rating_new)

# UPDATE PLAYERS' RATING IN "PLAYERS" TABLE

            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p1_rating_new, player_1_id.get()))
            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p2_rating_new, player_2_id.get()))

# INSERT MATCH IN PLAYER 1'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_1_id.get()),
                {
                    'opponent': p2_data[0][0] + " " + p2_data[0][1],
                    'result': "WIN",
                    'rating_delta': p1_rating_change,
                    'rating': p1_rating_new,
                    'date': date.today()
                })

# INSERT MATCH IN PLAYER 2'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_2_id.get()),
                {
                    'opponent': p1_data[0][0] + " " + p1_data[0][1],
                    'result': "LOSS",
                    'rating_delta': p2_rating_change,
                    'rating': p2_rating_new,
                    'date': date.today()
                })

            player_1_id.delete(0, END)
            player_2_id.delete(0, END)

            root.update()

            conn.commit()
            conn.close()

        def draw():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_1_id.get())))
            p1_data = c.fetchall()
            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_2_id.get())))
            p2_data = c.fetchall()

            p1_rating = p1_data[0][5]
            # print(p1_rating)

            p2_rating = p2_data[0][5]
            # print(p2_rating)

            p1_prob = (pow(10, p1_rating / 400)) / (pow(10, p1_rating / 400) + pow(10, p2_rating / 400))
            # print(p1_prob)

            p2_prob = (pow(10, p2_rating / 400)) / (pow(10, p2_rating / 400) + pow(10, p1_rating / 400))
            # print(p2_prob)

            if p1_rating > p2_rating:
                p1_rating_change = k/2 * (p1_prob - 1)
                p2_rating_change = (-1) * p1_rating_change

            else:
                p1_rating_change = k/2 * (1 - p1_prob)
                p2_rating_change = (-1) * p1_rating_change

            print(p1_rating_change)
            print(p2_rating_change)

            p1_rating_new = p1_rating + p1_rating_change
            p2_rating_new = p2_rating + p2_rating_change

            # print(p1_rating_new)
            # print(p2_rating_new)

# UPDATE BOTH PLAYERS' RATING IN PLAYERS TABLE

            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p1_rating_new, player_1_id.get()))
            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p2_rating_new, player_2_id.get()))

# INSERT MATCH IN PLAYER 1'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_1_id.get()),
                {
                    'opponent': p2_data[0][0] + " " + p2_data[0][1],
                    'result': "DRAW",
                    'rating_delta': p1_rating_change,
                    'rating': p1_rating_new,
                    'date': date.today()
                })

# INSERT MATCH IN PLAYER 2'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_2_id.get()),
                {
                    'opponent': p1_data[0][0] + " " + p1_data[0][1],
                    'result': "DRAW",
                    'rating_delta': p2_rating_change,
                    'rating': p2_rating_new,
                    'date': date.today()
                })

            player_1_id.delete(0, END)
            player_2_id.delete(0, END)

            root.update()

            conn.commit()
            conn.close()

        def p_2_win():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_1_id.get())))
            p1_data = c.fetchall()
            c.execute("SELECT * FROM players WHERE oid= %s ;" % (str(player_2_id.get())))
            p2_data = c.fetchall()

            p1_rating = p1_data[0][5]
            # print(p1_rating)

            p2_rating = p2_data[0][5]
            # print(p2_rating)

            p1_prob = (pow(10, p1_rating / 400)) / (pow(10, p1_rating / 400) + pow(10, p2_rating / 400))
            # print(p1_prob)

            p2_prob = (pow(10, p2_rating / 400)) / (pow(10, p2_rating / 400) + pow(10, p1_rating / 400))
            # print(p2_prob)

            p1_rating_change = k * (p2_prob - 1)
            p2_rating_change = -1 * p1_rating_change

            p1_rating_new = p1_rating + p1_rating_change
            p2_rating_new = p2_rating + p2_rating_change

            # print(p1_rating_new)
            # print(p2_rating_new)

# UPDATE BOTH PLAYERS' RATING IN PLAYERS TABLE

            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p1_rating_new, player_1_id.get()))
            c.execute("UPDATE players SET rating = %s WHERE oid = %s;" % (p2_rating_new, player_2_id.get()))

# INSERT MATCH IN PLAYER 1'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_1_id.get()),
                {
                    'opponent': p2_data[0][0] + " " + p2_data[0][1],
                    'result': "LOSS",
                    'rating_delta': p1_rating_change,
                    'rating': p1_rating_new,
                    'date': date.today()
                })

# INSERT MATCH IN PLAYER 2'S HISTORY

            c.execute(
                "INSERT INTO table%s VALUES(:opponent, :result, :rating_delta, :rating, :date) ;" % (player_2_id.get()),
                {
                    'opponent': p1_data[0][0] + " " + p1_data[0][1],
                    'result': "WIN",
                    'rating_delta': p2_rating_change,
                    'rating': p2_rating_new,
                    'date': date.today()
                })

            player_1_id.delete(0, END)
            player_2_id.delete(0, END)

            root.update()

            conn.commit()
            conn.close()

        result_button_1 = Button(match_window, text=" 1 - 0 ", command=p_1_win)
        result_button_1.place(relx=1 / 6, rely=3 / 4, anchor=CENTER)

        result_button_2 = Button(match_window, text=" DRAW ", command=draw)
        result_button_2.place(relx=3 / 6, rely=3 / 4, anchor=CENTER)

        result_button_3 = Button(match_window, text=" 0 - 1 ", command=p_2_win)
        result_button_3.place(relx=5 / 6, rely=3 / 4, anchor=CENTER)

    add_player_button = Button(root, text="Add a new player", command=open_new_player_window)
    add_player_button.grid(column=3, row=1, padx=(10, 0))

    history_button = Button(root, text="History", command=open_history)
    history_button.grid(column=2, row=3, pady=(10, 0))

    match_button = Button(root, text="New Match", command=open_match)
    match_button.grid(column=1, row=3, pady=(10, 0))

    def open_edit_players_window():
        edit_players_window = Toplevel()
        edit_players_window.title("Edit Players")
        edit_players_window.resizable(width=False, height=False)

        player_id_lbl = Label(edit_players_window, text="Enter Player ID")
        player_id_lbl.grid(column=0, row=0, padx=10, pady=5)

        player_id_entry = Entry(edit_players_window, width=5)
        player_id_entry.grid(column=1, row=0, rowspan=1, padx=10, pady=5)

# FILL ENTRIES WITH INFORMATION CORRESPONDING TO THE SELECTED PLAYER'S OID

        def submit_id():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            id = player_id_entry.get()

            c.execute("SELECT * FROM players WHERE oid = %s;" % id)
            record = c.fetchall()

            print(record)

            for field in record:
                first_name.insert(0, field[0])
                last_name.insert(0, field[1])
                city.insert(0, field[2])
                state.insert(0, field[3])
                country.insert(0, field[4])

            conn.commit()
            conn.close()

# UPDATE PLAYER INFORMATION

        def update():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("""UPDATE players SET
                    first_name = :first_name,
                    last_name = :last_name,
                    city = :city,
                    state = :state,
                    country = :country

                    WHERE oid= :oid""",
                      {
                          'first_name': first_name.get(),
                          'last_name': last_name.get(),
                          'city': city.get(),
                          'state': state.get(),
                          'country': country.get(),
                          'oid': player_id_entry.get()
                      })

            conn.commit()
            conn.close()

        def delete():
            conn = sqlite3.connect(league + '.db')
            c = conn.cursor()

            c.execute("DELETE from players WHERE oid= %s;" % (player_id_entry.get()))

# DELETE SELECTED PLAYER'S MATCH HISTORY TABLE

            player_id_entry.delete(0, END)
            first_name.delete(0, END)
            last_name.delete(0, END)
            city.delete(0, END)
            state.delete(0, END)
            country.delete(0, END)

            conn.commit()
            conn.close()

        submit_button = Button(edit_players_window, text="Submit", command=submit_id)
        submit_button.grid(column=2, row=1, pady=5)

        edit_player_button = Button(edit_players_window, text="Edit Player", command=update)
        edit_player_button.grid(column=2, row=2, pady=5)

        delete_player_button = Button(edit_players_window, text="Delete Player", command=delete)
        delete_player_button.grid(column=2, row=3, padx=5, pady=5)

        first_name_lbl = Label(edit_players_window, text="First Name")
        first_name_lbl.grid(column=0, row=1, padx=5, pady=5)
        first_name = Entry(edit_players_window, width=15)
        first_name.grid(column=1, row=1, padx=10, pady=5)

        last_name_lbl = Label(edit_players_window, text="Last Name")
        last_name_lbl.grid(column=0, row=2, padx=5, pady=5)
        last_name = Entry(edit_players_window, width=15)
        last_name.grid(column=1, row=2, padx=10, pady=5)

        city_lbl = Label(edit_players_window, text="City")
        city_lbl.grid(column=0, row=3, padx=5, pady=5)
        city = Entry(edit_players_window, width=15)
        city.grid(column=1, row=3, padx=5, pady=5)

        state_lbl = Label(edit_players_window, text="State")
        state_lbl.grid(column=0, row=4, padx=5, pady=5)
        state = Entry(edit_players_window, width=15)
        state.grid(column=1, row=4, padx=5, pady=5)

        country_lbl = Label(edit_players_window, text="Country")
        country_lbl.grid(column=0, row=5, padx=5, pady=5)
        country = Entry(edit_players_window, width=15)
        country.grid(column=1, row=5, padx=5, pady=5)

    edit_players_button = Button(root, text="Edit existing players", command=open_edit_players_window)
    edit_players_button.grid(column=3, row=2, padx=(10, 0))

# DELETE LEAGUE FROM LEAGUE LIST DATABASE


def delete_league():
    conn = sqlite3.connect('League List.db')
    c = conn.cursor()

    parameter = "'" + leagues_combobox.get() + "'"

    c.execute("DELETE FROM leagues WHERE league_name =%s;" % parameter)

    conn.commit()
    conn.close()


root = Tk()

# CONNECT TO LEAGUE LIST DATABASE

conn = sqlite3.connect('League List.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS leagues (
            'league_name' TEXT PRIMARY KEY,
            'k_value' INTEGER NOT NULL
            )
            """)

# LEAGUE SELECTION WINDOW

league_selection_window = Toplevel()
league_selection_window.title("League Selection")
league_selection_window.geometry("360x180")
league_selection_window.resizable(width=False, height=False)

# POPULATE LEAGUE SELECTION COMBOBOX

league_list = []


def populate_league_selection_box():
    conn = sqlite3.connect('League List.db')
    c = conn.cursor()

    c.execute("""SELECT league_name
                FROM leagues""")
    i = 0
    for league in c.fetchall():
        league_list.append(league[i])

    conn.commit()
    conn.close()


populate_league_selection_box()

# WIDGETS IN LEAGUE SELECTION WINDOW

league_selection_lbl = Label(league_selection_window, text='Select Your League')
league_selection_lbl.place(relx=1 / 2, rely=1 / 10, anchor=CENTER)

league_name_lbl = Label(league_selection_window, text='League Name')
league_name_lbl.place(relx=1 / 8, rely=2 / 5, anchor=CENTER)

leagues_combobox = Combobox(league_selection_window, state='readonly', values=league_list)
leagues_combobox.place(relx=1 / 2, rely=2 / 5, anchor=CENTER)

open_league_btn = Button(league_selection_window, text='Open League', command=open_league)
open_league_btn.place(relx=7 / 8, rely=2 / 5, anchor=CENTER)

new_league_btn = Button(league_selection_window, text='New League', command=open_add_new_league)
new_league_btn.place(relx=3 / 10, rely=4 / 5, anchor=CENTER)

delete_league_btn = Button(league_selection_window, text='Delete League', command=delete_league)
delete_league_btn.place(relx=7 / 10, rely=4 / 5, anchor=CENTER)

conn.commit()
conn.close()

root.mainloop()
