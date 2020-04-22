
import tkinter as tk
import sqlite3
from PIL import ImageTk, Image


root= tk.Tk()
root.title("GUI for Address Book")
root.iconbitmap('G:\Python\Projects\Hopstarter-Sleek-Xp-Software-Windows-Messenger.ico')
root.geometry("400x600")

global show_label

conn= sqlite3.connect("Address book.db")                                                                    # connecting to the database

# Create cursor
c= conn.cursor()


# Function
def submit():
    conn = sqlite3.connect("Address book.db")                                                               # connecting to the database

    # Create cursor
    c = conn.cursor()

    c.execute("INSERT INTO addresses VALUES ( :f_name, :l_name, :address, :city, :state, :zipcode)",        # inserting data into the database

              # Creating a dictionary
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'address': address.get(),
                  'city': city.get(),
                  'state': state.get(),
                  'zipcode': zipcode.get()
              })
    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()

    # Delete the entries
    f_name.delete(0, "end")
    l_name.delete(0, "end")
    address.delete(0, "end")
    city.delete(0, "end")
    state.delete(0, "end")
    zipcode.delete(0, "end")
    return

def show():
    global show_label
    conn = sqlite3.connect("Address book.db")                                                                   # connecting to the database

    # Create cursor
    c = conn.cursor()

    c.execute("SELECT *, oid FROM addresses")                                                                   # selecting data from the database
    records= c.fetchall()
    print(records)                                                                                              # prints the complete data as tuples in the terminal

    print_rec=''
    for record in records:
        print_rec += str(record[0]) + " " + str(record[1]) + "\t" + str(record[6]) + "\n"                       # accessing only the first and last name from the database

    show_label= tk.Label(root, text= print_rec)                                                                 # shows the records in the gui
    show_label.grid(row= 11, column= 0, columnspan= 2)

    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()
    return

def delete():                                                                                                   # to delete a particular record form the database
    global show_label
    conn = sqlite3.connect("Address book.db")  # connecting to the database

    # Create cursor
    c = conn.cursor()

    c.execute("DELETE FROM addresses where oid =" + id_number.get())                                            # deletes the record corresponding to the entered oid number
    id_number.delete(0, "end")

    show_label.grid_forget()

    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()
    return

# Function to edit an existing entry in the database
def edit():
    global editor
    # Creating a new window
    editor = tk.Tk()
    editor.title("Make your changes")
    editor.iconbitmap('G:\Python\Projects\Hopstarter-Sleek-Xp-Software-Windows-Messenger.ico')
    editor.geometry("400x600")

    conn = sqlite3.connect("Address book.db")                                                                   # connecting to the database

    # Create cursor
    c = conn.cursor()

    record= id_number.get()
    c.execute("SELECT *, oid FROM addresses WHERE oid=" + record)  # selecting data from the database
    records = c.fetchall()

    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor


    # Entries-Text Boxes for the editor window
    f_name_editor = tk.Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, pady=(5, 2))
    l_name_editor = tk.Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1, pady=2)
    address_editor = tk.Entry(editor, width=30)
    address_editor.grid(row=2, column=1, pady=2)
    city_editor = tk.Entry(editor, width=30)
    city_editor.grid(row=3, column=1, pady=2)
    state_editor = tk.Entry(editor, width=30)
    state_editor.grid(row=4, column=1, pady=2)
    zipcode_editor = tk.Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1, pady=2)

    # Labels for the database
    f_name_label = tk.Label(editor, text="Enter your first name")
    f_name_label.grid(row=0, column=0)
    l_name_label = tk.Label(editor, text="Enter your last name")
    l_name_label.grid(row=1, column=0)
    address_label = tk.Label(editor, text="Enter your address")
    address_label.grid(row=2, column=0)
    city_label = tk.Label(editor, text="Enter your city")
    city_label.grid(row=3, column=0)
    state_label = tk.Label(editor, text="Enter your state")
    state_label.grid(row=4, column=0)
    zipcode_label = tk.Label(editor, text="Enter your zipcode")
    zipcode_label.grid(row=5, column=0)

    # Loop through the list in the database and inserting the values from the database onto the text boxes in the new window
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    # Save Changes button
    save_changes_btn= tk.Button(editor, text= "Save Changes", command= update)
    save_changes_btn.grid(row= 6, column= 0, columnspan= 2, padx= 10, pady= 10, ipadx= 125)


    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()
    return

# Function to update the changes in the database
def update():
    global editor
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    conn = sqlite3.connect("Address book.db")  # connecting to the database

    # Create cursor
    c = conn.cursor()

    record = id_number.get()
    c.execute("""UPDATE addresses SET
                first_name= :first,
                last_name= :last,
                address= :address,
                city= :city,
                state= :state,
                zipcode= :zipcode
                
                WHERE oid= :oid""",
                {
                'first': f_name_editor.get(),
                'last' : l_name_editor.get(),
                'address': address_editor.get(),
                'city': city_editor.get(),
                'state': state_editor.get(),
                'zipcode': zipcode_editor.get(),
                'oid': record
               })

    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()

    # Close the window
    editor.destroy()
    return

# Entries Text Boxes for the database
f_name= tk.Entry(root, width= 30)
f_name.grid(row= 0, column= 1, pady= (5,2))
l_name= tk.Entry(root, width= 30)
l_name.grid(row= 1, column= 1, pady= 2)
address= tk.Entry(root, width= 30)
address.grid(row= 2, column= 1, pady= 2)
city= tk.Entry(root, width= 30)
city.grid(row= 3, column= 1, pady= 2)
state= tk.Entry(root, width= 30)
state.grid(row= 4, column= 1, pady= 2)
zipcode= tk.Entry(root, width= 30)
zipcode.grid(row= 5, column= 1, pady= 2)
id_number= tk.Entry(root, width= 30)
id_number.grid(row= 8, column= 1, pady=2)

# Labels for the database
f_name_label= tk.Label(root, text= "Enter your first name")
f_name_label.grid(row= 0, column= 0)
l_name_label= tk.Label(root, text= "Enter your last name")
l_name_label.grid(row= 1, column= 0)
address_label= tk.Label(root, text= "Enter your address")
address_label.grid(row= 2, column= 0)
city_label= tk.Label(root, text= "Enter your city")
city_label.grid(row= 3, column= 0)
state_label= tk.Label(root, text= "Enter your state")
state_label.grid(row= 4, column= 0)
zipcode_label= tk.Label(root, text= "Enter your zipcode")
zipcode_label.grid(row= 5, column= 0)
id_number_label= tk.Label(root, text= "ID # to delete ")
id_number_label.grid(row= 8, column=0)

# Submit Button
submit_btn= tk.Button(root, text= "Submit", command= submit)
submit_btn.grid(row= 6, column= 0, columnspan= 2, padx= 10, pady= 10, ipadx= 150 )

# Show Button
show_btn= tk.Button(root, text= "Show Records", command= show)
show_btn.grid(row= 7, column= 0, columnspan= 2, padx= 10, pady= 10, ipadx= 133)

#Delete Button
delete_btn= tk.Button(root, text= "Delete Record", command= delete)
delete_btn.grid(row= 9, column= 0, padx= 10, pady= 10, columnspan= 2, ipadx= 134)

# Edit Button
edit_btn= tk.Button(root, text= "Edit Record", command= edit)
edit_btn.grid(row= 10, column= 0, padx= 10, pady= 10, columnspan= 2, ipadx= 134)


# Commit changes
conn.commit()

# Close the connection
conn.close()


# Start the program
root.mainloop()