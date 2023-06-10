import psycopg2
from psycopg2 import Error
from tkinter import *

def compound_postgress(func):
    def wrapper(*args, **kwargs):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          password="postgres",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")

            cursor = connection.cursor()


            return func(cursor=cursor, connection=connection, *args, **kwargs)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()


    return wrapper

@compound_postgress
def select_post(query, cursor=None, many=True, connection=None):
    if many:
        result = []
        cursor.execute(query)
        response = cursor.fetchall()
        for row in response:

            result.append(row[0])

        return result

    else:
        cursor.execute(query)
        response = cursor.fetchall()

        return response



@compound_postgress
def update_post(query, id, cursor=None, connection=None, many=True):
    '''
    пример
    update_post('Update users_user set email = %s where id = %s', (id, email))
    '''

    cursor.execute(query)
    connection.commit()

    postgreSQL_select_Query = f"SELECT * FROM users_user WHERE id = {id}"
    res = select_post(query=postgreSQL_select_Query, many=False)

    return "Успешно изменено", res


@compound_postgress
def all_my_tabs(cursor=None, connection=None):
    postgreSQL_select_Query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    result = []
    cursor.execute(postgreSQL_select_Query)
    response = cursor.fetchall()
    for row in response:
        result.append(row[0])
    return result

@compound_postgress
def all_my_col(tab, cursor=None, connection=None):
    postgreSQL_select_Query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tab}'"
    result = []
    cursor.execute(postgreSQL_select_Query)

    response = cursor.fetchall()
    # print(response)
    for row in response:
        result.append(row[0])

    return result


@compound_postgress
def sel_id(tab, cols, id, cursor=None, connection=None):
    cols_list = cols.split(', ')

    postgreSQL_select_Query = f"SELECT {cols} FROM {tab} WHERE id = '{id}'"
    result = {}
    cursor.execute(postgreSQL_select_Query)
    response = cursor.fetchall()[0]
    result = response
    # for index, col in enumerate(cols_list):
    #
    #     result[col] = response[index]
    #
    # print(result)


    return result

@compound_postgress
def full_tab(tab, cursor=None, connection=None):

    result = []

    postgreSQL_select_Query = f"SELECT * FROM {tab}"

    cursor.execute(postgreSQL_select_Query)

    tab = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]


    # for row in response:
    #     row_res = {}
    #
    #     for index, col in enumerate(cols_list):
    #         row_res[col] = row[index]
    #
    #     result.append(row_res)
    #     print(row_res)

    return {
        "tab": tab,
        "cols": cols
    }


@compound_postgress
def sel_all(tab, cols, cursor=None, connection=None):
    cols_list = cols.split(', ')
    result = []


    postgreSQL_select_Query = f"SELECT {cols} FROM {tab}"

    cursor.execute(postgreSQL_select_Query)
    response = cursor.fetchall()

    for row in response:
        row_res = {}

        for index, col in enumerate(cols_list):
            row_res[col] = row[index]

        result.append(row_res)


    return result

@compound_postgress
def count_row(tab, cursor=None, connection=None):
    postgreSQL_select_Query = f"SELECT count(*) AS exact_count FROM {tab}"
    cursor.execute(postgreSQL_select_Query)
    response = cursor.fetchone()[0]

    return response

@compound_postgress
def list_id(tab, cursor=None, connection=None):
    result = []
    postgreSQL_select_Query = f"SELECT id FROM {tab}"
    cursor.execute(postgreSQL_select_Query)
    response = cursor.fetchall()
    for row in response:
        result.append(row[0])


    return result






def interpost():
    COMAND = ['mytab', "tabcol", 'selid', 'update']

    while True:
        command = input('\nСписок команд: mytab, tabcol, selid, update\n\nПример tabcol -'
                        ' tabcol users_user\n\nselid users_user [first_name, last_name]'
                        ' 2 или *:\n\n update users_user first_name 1\n\n ')


        if command in COMAND or 'selid' in command or "tabcol" in command or 'update' in command:
            if command == 'mytab':
                res = all_my_tabs()
                print(res)
                continue
            if "tabcol" in command:
                tab = command.split()[1]
                res = all_my_col(tab)
                print(res)
                continue
            if "selid" in command.lower():

                tab = command.split()[1]


                start = command.index('[') + 1
                finish = command.index(']')
                cols = command[start:finish]
                id = command[finish + 2:]
                if id == "*":
                    res = sel_all(tab, cols)

                    continue
                else:
                    res = sel_id(tab, cols, id)

                    continue

            if command == 'stop':
                break

            if 'update' in command:
                tab = command.split()[1]
                col = command.split()[2]
                id = command.split()[3]
                old_data = sel_id(tab, col, id)
                data = input(f'Змаенить "{old_data}", на: ')
                update(tab, col, id, data)
                continue


        else:
            continue


def update(tab, col, id, data):

    query = f'Update {tab} set {col} = {data} where id = {id}'
    update_post(query, id)


def data_fill_numbers_by_id(tab, col):

    ids = list_id(tab)
    print(ids)
    for id in ids:
        update(tab, col, id, id)

    return sel_all(tab, col)


# print(data_fill_numbers_by_id('ads_categories', 'slug'))


# interpost()



class Example(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Список таблиц бд")
        self.pack(fill=BOTH, expand=1)

        acts = all_my_tabs()

        lb = Listbox(self, height=30, width=50, font=20, selectmode=SINGLE)

        for i in acts:
            lb.insert(END, i)

        select = lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.pack(pady=15)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.label.pack()

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)
        # select = lb.get(lb.curselection())
        # print(select)
        okButton = Button(self, text="Ок", command=lambda: self.tabl_interface(lb.get(lb.curselection())))
        okButton.pack(side=RIGHT, padx=20, pady=20)




    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)


    def tabl_interface(self, tab_name):


        # cols = all_my_col(tab_name)
        full_table = full_tab(tab_name)
        tab = full_table["tab"]
        cols = full_table["cols"]
        root = Tk()
        root.title(tab_name)
        height = len(tab)
        width = len(cols)



        for i, col in enumerate(cols):
            b = Entry(root, text='')
            b.grid(row=0, column=i)
            b.insert(END, col)


        for i in range(height): #Rows
            for j in range(width): #Columns

                data = tab[i][j]
                if not data:
                    text = ''
                if type(data) != str:
                    text = str(data)
                else:
                    text = data

                b = Entry(root, text='')
                b.grid(row=i + 1 , column=j)
                b.insert(END, text)

# def window_gen():

def main():
    root = Tk()
    ex = Example()
    root.geometry("800x750")
    root.mainloop()


if __name__ == '__main__':
    # print(full_tab('users_user'))
    main()

# mainloop()

