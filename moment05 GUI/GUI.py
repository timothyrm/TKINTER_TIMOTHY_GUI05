#Jag ska låta användaren regristrera sig med ett konto
#Jag ska låta användearen kunna logga in med det konto som skapades (om det inte är samma användarnamn etc i login som i regrestrering så ska det bli error)
#Jag ska låta användaren lägga in pengar och ta ut pengar, när den gör detta så måste filen uppdateras
#Jag ska låta användaren se dens saldo och person uppgifter som den kommer kunna ändra



#Imports
from tkinter import *
import os 
from PIL import ImageTk, Image

#Hemskärmen
master = Tk()
master.title('Bankapplikation')

#Functions
def finish_reg():
    namn = temp_namn.get()
    ålder = temp_ålder.get()
    kön = temp_kön.get()
    lödsenord = temp_lödsenord.get()
    all_accounts = os.listdir()
    
    if namn == "" or ålder == "" or kön == "" or lödsenord == "":
        notif.config(fg="red",text="Du måste fylla i dina uppgifter *")
        return

    for namn_check in all_accounts:   #tittar så att namnet inte upprepas och att kontot då redan finns 
        if namn == namn_check:
            notif.config(fg="red",text="Kontot finns redan!")
        else:
            new_file = open(namn,"w")
            new_file.write(namn+'\n')
            new_file.write(lödsenord+'\n')
            new_file.write(ålder+'\n')
            new_file.write(kön+'\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text="Du har nu skapat ett konto")

def register():
    #Variabler
    global temp_namn
    global temp_ålder
    global temp_kön
    global temp_lödsenord
    global notif 
    temp_namn = StringVar()
    temp_ålder = StringVar()
    temp_kön = StringVar()
    temp_lödsenord = StringVar()
    
    #Här är register skärmen
    register_screen = Toplevel(master)
    register_screen.title('Regristrera')

    #labels
    Label(register_screen, text="Snälla skriv in dina person uppgfiter nedan", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Namn:", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(register_screen, text="Ålder:", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(register_screen, text="Kön:", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(register_screen, text="Lödsenord:", font=('Calibri',12)).grid(row=4,sticky=W)
    notif = Label(register_screen, font=('Calibri',12))
    notif.grid(row=6,sticky=N,pady=10)



    Entry(register_screen,textvariable=temp_namn).grid(row=1,column=0)
    Entry(register_screen,textvariable=temp_ålder).grid(row=2,column=0)
    Entry(register_screen,textvariable=temp_kön).grid(row=3,column=0)
    Entry(register_screen,textvariable=temp_lödsenord,show="*").grid(row=4,column=0)

    #Buttons
    Button(register_screen, text="Regristera", command = finish_reg, font=('Calibri',12)).grid(row=5,sticky=N,pady=10)

def login_session():
    global login_namn
    all_accounts = os.listdir()
    login_namn = temp_login_namn.get()
    login_lödsenord = temp_login_lödsenord.get()

    for namn in all_accounts: #kollar så att nåt namn redan finns i directeryn
        if namn == login_namn:
            file = open(namn,"r")
            file_data = file.read()
            file_data = file_data.split('\n')
            lödsenord = file_data[1]
            #Dashboard
            if login_lödsenord == lödsenord:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                #Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard, text="Välkommen "+namn, font=('Calibri',12)).grid(row=1,sticky=N,padx=5)
                #Buttons
                Button(account_dashboard, text="Personliga detaljer",font=('Calibri',12),width=30,command=personliga_detaljer).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard, text="Insättning",font=('Calibri',12),width=30,command=insättning).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard, text="Uttagning",font=('Calibri',12),width=30,command=uttagning).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)

               
                return
            else:
                login_notif.config(fg="red", text="Lödsenordet är fel!")
                return
    login_notif.config(fg="red", text="Inget konto med det namnet finns!")

def insättning():
    #variabler
    global amount
    global deposit_notif 
    global current_balance_label
    amount = StringVar()
    file = open(login_namn, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    #Insättningsskärmen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    #Labels
    Label(deposit_screen, text="Deposit", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(deposit_screen, text="Nurvarande saldot : £ "+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen, text="Belopp : ", font=('Calibri',12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen,font=('Calibri',12))
    deposit_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2,column=1)
    #Button
    Button(deposit_screen,text="Klar",font=('Calibri',12),command=färdig_instättning).grid(row=3,stick=W,pady=5)

def färdig_instättning():
    if amount.get() == "":
        deposit_notif.config(text='Måste skriva in något',fg="red")
    if float(amount.get()) <=0:
        deposit_notif.config(text='Du kan inte sätta in negativa tal', fg="red")
        return

    file = open(login_namn, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance,str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text="Nurvarande saldot : £ "+str(updated_balance),fg="green")
    deposit_notif.config(text='Saldot har uppdaterats', fg='green')



def uttagning():
    #variabler
    global withdraw_amount
    global withdraw_notif 
    global current_balance_label
    withdraw_amount = StringVar()
    file = open(login_namn, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    #Insättningsskärmen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    #Labels
    Label(withdraw_screen, text="Withdraw", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(withdraw_screen, text="Nurvarande saldot : £ "+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen, text="Belopp : ", font=('Calibri',12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen,font=('Calibri',12))
    withdraw_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1)
    #Button
    Button(withdraw_screen,text="Klar",font=('Calibri',12),command=färdig_uttagning).grid(row=3,stick=W,pady=5)

def färdig_uttagning():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text='Måste skriva in något',fg="red")
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(text='Du kan inte sätta in negativa tal', fg="red")
        return

    file = open(login_namn, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]


    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notif.config(text='Kan inte ta ut mer än vad du har!', fg='red')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance,str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text="Nurvarande saldot : £ "+str(updated_balance),fg="green")
    withdraw_notif.config(text='Saldot har uppdaterats', fg='green')   

def personliga_detaljer():
    file = open(login_namn,'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_namn = user_details[0]
    details_ålder = user_details[2]
    details_kön = user_details[3]
    details_saldo = user_details[4]
    #Personliga detaljer skärmen
    personliga_detaljer_screen = Toplevel(master)
    personliga_detaljer_screen.title('Personliga detaljer')
    #Labels
    Label(personliga_detaljer_screen, text="Personliga detaljer", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(personliga_detaljer_screen, text="Namn : "+details_namn, font=('Calibri',12)).grid(row=1,sticky=W)
    Label(personliga_detaljer_screen, text="Ålder : "+details_ålder, font=('Calibri',12)).grid(row=2,sticky=W)
    Label(personliga_detaljer_screen, text="Kön : "+details_kön, font=('Calibri',12)).grid(row=3,sticky=W)
    Label(personliga_detaljer_screen, text="Saldo : "+details_saldo, font=('Calibri',12)).grid(row=4,sticky=W)



def login():
    #Variabler
    global temp_login_namn
    global temp_login_lödsenord
    global login_notif
    global login_screen
    temp_login_namn = StringVar()
    temp_login_lödsenord = StringVar()

    #Logga in skärmen
    login_screen = Toplevel()
    login_screen.title('Logga in')

    #labels
    Label(login_screen, text="Logga vänligen in på ditt konto", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Användarnamn", font=('Calibri',12)).grid(row=1,sticky=N)
    Label(login_screen, text="Lödsenord", font=('Calibri',12)).grid(row=2,sticky=N)
    login_notif = Label(login_screen, font=('Calibri',12))
    login_notif.grid(row=4,sticky=N)

    #Entrys för att kunna skriva in anvnändarnamn osv
    Entry(login_screen, textvariable=temp_login_namn).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_lödsenord,show="*").grid(row=2,column=1,padx=5)

    #Button
    Button(login_screen, text="Logga in", command=login_session, width=15,font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)


#Buttons
Button(master, text="Regristrera  ", font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Logga in", font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()