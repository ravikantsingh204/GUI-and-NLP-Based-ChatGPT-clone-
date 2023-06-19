#**********************************************************importing required modules *****************************************************************************************************************
import tkinter
import customtkinter 
from PIL import Image, ImageTk
import mysql.connector as sqltor
from tkinter import messagebox
import openai
import speech_recognition as sr
import pyttsx3
#**********************************************************function to read out the text **************************************************************************************************************
def read():
    command=output_textbox.get("0.0","end")
    command=command.strip()
    if len(command)<=0:
        messagebox.showerror("Error","No Response found on Result ask any question")
    else:
        #**************************************************Initialize the engine***********************************************************************************************************************
        engine = pyttsx3.init()
        engine.setProperty('rate',140)
        #engine.setProperty('volume',0.9)
        engine.say(command)
        engine.runAndWait()
#**********************************************************function for clearing textboxes*************************************************************************************************************
def clear():
    question_textbox.delete("0.0", "end")
    output_textbox.delete("0.0", "end")
#**********************************************************Initialize the speech recognizer ***********************************************************************************************************
r = sr.Recognizer()
#**********************************************************function for listening question ************************************************************************************************************
def listen():
    try:
		#**************************************************use the microphone as source for input.*****************************************************************************************************
        with sr.Microphone() as source2:
			#**********************************************wait for a second to let the recognizer*****************************************************************************************************
			#**********************************************adjust the energy threshold based on the surrounding noise level****************************************************************************
            #question_textbox.insert("0.0","listening........... \n")
            r.adjust_for_ambient_noise(source2, duration=0.2)
			#**********************************************listens for the user's input****************************************************************************************************************
            audio2 = r.listen(source2)
			#**********************************************Using google to recognize audio*************************************************************************************************************
            my_text = r.recognize_google(audio2)
            my_text = my_text.lower()
            #print(my_text)
            #my_text="Did you say :->  " + my_text
            question_textbox.insert("1.0",my_text)
            #SpeakText(MyText)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))	    
    except sr.UnknownValueError:
        print("unknown error occurred")
#**********************************************************function for chatGPT************************************************************************************************************************
def chatGPT():
    #******************************************************retriving data inside textbox***************************************************************************************************************
    question_variable=question_textbox.get("0.0","end")
    question_variable=question_variable.strip()
    if len(question_variable)<=0:
        messagebox.showerror("Error","Please ask some question")
    else:
        #**************************************************Set up the OpenAI API client****************************************************************************************************************
        openai.api_key = "api key"
        #**************************************************Set up the model and prompt*****************************************************************************************************************
        model_engine = "text-davinci-003"
        #**************************************************Generate a response*************************************************************************************************************************
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=question_variable,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        #**************************************************extracting useful part of response**********************************************************************************************************
        response = completion.choices[0].text
        #**************************************************returning response**************************************************************************************************************************
        #return response
        output_textbox.insert("0.0",response)
#**********************************************************function for generating result**************************************************************************************************************
def display_result():
    answer=chatGPT(question_variable)
    output_textbox.insert("0.0",answer)
#**********************************************************setting connection with database************************************************************************************************************
mycon=sqltor.connect(host='localhost',user='root',password='*********',database='chatgpt_project')
#**********************************************************creating welcome window*********************************************************************************************************************
def welcome_page():
    #******************************************************destroy login window************************************************************************************************************************
    login_window.destroy()
    #******************************************************creating welcome window or frame************************************************************************************************************
    welcome_window=customtkinter.CTk()
    welcome_window.geometry("1920x1080")
    welcome_window.title("Welcome Page")
    #******************************************************inserting background image******************************************************************************************************************
    image2=ImageTk.PhotoImage(Image.open("background wallpaper4.jpg"))
    #******************************************************converting image into lable*****************************************************************************************************************
    background_frame1=customtkinter.CTkLabel(master=welcome_window,image=image2)
    background_frame1.pack()
    #******************************************************creating a new frame for login credentials *************************************************************************************************
    welcome_frame=customtkinter.CTkFrame(master=background_frame1,width=700,height=850,corner_radius=100)
    welcome_frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    #******************************************************heading of login frame credential***********************************************************************************************************
    heading_label1=customtkinter.CTkLabel(master=welcome_frame,text="Welcome Mr.{},".format(saved_name),font=("Century Gothic",36))
    heading_label1.place(x=50,y=45)
    #******************************************************creating a label for question***************************************************************************************************************
    heading_label2=customtkinter.CTkLabel(master=welcome_frame,text="Ask Your Question",font=("Century Gothic",26))
    heading_label2.place(x=50,y=100)
    #******************************************************creating entry box for question*************************************************************************************************************
    global question_textbox
    global question_variable
    #question_variable=customtkinter.StringVar()
    question_textbox=customtkinter.CTkTextbox(master=welcome_frame,width=500,height=100,font=("Century Gothic",20))
    question_textbox.place(x=50,y=150)
    question_textbox.focus()
    #question_variable=question_textbox.get("0.0","end")
    #print(question_variable)
    #******************************************************inserting background image for mic button***************************************************************************************************
    mic_logo=ImageTk.PhotoImage(Image.open("mic.png").resize((50,50),Image.ANTIALIAS))
    mic_button=customtkinter.CTkButton(master=welcome_frame,width=100,height=100,image=mic_logo,corner_radius=10,text="Speak",compound="top",command=listen,font=("Century Gothic",20))
    mic_button.place(x=575,y=150)
    #******************************************************search button*******************************************************************************************************************************
    search_logo=ImageTk.PhotoImage(Image.open("search2.png").resize((50,50),Image.ANTIALIAS))
    search_button=customtkinter.CTkButton(master=welcome_frame,width=150,height=50,corner_radius=6,image=search_logo,text="Search",command=chatGPT,font=("Century Gothic",20),compound="left")
    search_button.place(x=300,y=275)
    #******************************************************label for result****************************************************************************************************************************
    result_label3=customtkinter.CTkLabel(master=welcome_frame,text="Result:",font=("Century Gothic",26))
    result_label3.place(x=50,y=325)
    #******************************************************text box for output*************************************************************************************************************************
    global output_textbox
    output_textbox=customtkinter.CTkTextbox(master=welcome_frame,width=600,height=400,font=("Century Gothic",20))
    output_textbox.place(x=50,y=375)
    #******************************************************clear button********************************************************************************************************************************
    clear_logo=ImageTk.PhotoImage(Image.open("clear.png").resize((50,50),Image.ANTIALIAS))
    clear_button=customtkinter.CTkButton(master=welcome_frame,width=100,height=50,corner_radius=6,text="Clear",image=clear_logo,font=("Century Gothic",16),command=clear,compound="left")
    clear_button.place(x=550,y=780)
    #******************************************************read button*********************************************************************************************************************************
    speaker_logo=ImageTk.PhotoImage(Image.open("speaker.png").resize((50,50),Image.ANTIALIAS))
    speaker_button=customtkinter.CTkButton(master=welcome_frame,width=100,height=50,image=speaker_logo,corner_radius=10,text="Read",compound="left",command=read,font=("Century Gothic",20))
    speaker_button.place(x=50,y=780)
    
    welcome_window.mainloop()
#**********************************************************function for create new account button firing query*****************************************************************************************
def create_new_account():
    #******************************************************fetching all values*************************************************************************************************************************
    name=new_name_variable.get()
    name=name.strip()
    email=new_email_variable.get()
    email=email.strip()
    password=new_password_variable.get()
    password=password.strip()
    confirm_password=new_confirm_password_variable.get()
    confirm_password=confirm_password.strip()
    #******************************************************function to validate name*******************************************************************************************************************
    def name_validator():
        if len(name)<3:
            #**********************************************display error message***********************************************************************************************************************
            messagebox.showinfo("warning","Name can't be empty")
        else:
            return True
    #******************************************************function to validate Email******************************************************************************************************************
    def email_validate():
        if email[-10:-1]!="@gmail.co" or len(email)<11 or email[-1]!="m":
            messagebox.showinfo("warning","Enter a valid google Email")
        else:
            return True
    #******************************************************function to validate password***************************************************************************************************************
    def password_validate():
        if len(password)<8:
            messagebox.showinfo("warning","Password length should be greater than 8")
        else:
            upper_case=lower_case=number=special_charecter=0
            for i in password:
                #****************************************** count number of upper case in password*****************************************************************************************************
                if i.isupper():
                    upper_case=upper_case+1
                #****************************************** count number of lower case in password*****************************************************************************************************
                elif i.islower():
                    lower_case=lower_case+1
                #****************************************** count number of numbers in password********************************************************************************************************
                elif i.isnumeric():
                    number=number+1
                #****************************************** count number of special character in password**********************************************************************************************
                elif i in ["@","#","*","$","%","&","!"]:
                    special_charecter=special_charecter+1
                #******************************************check for satisfaction of password**********************************************************************************************************
            if upper_case<=0:
                messagebox.showinfo("warning","Password must contain a Upper case alphabet")
            elif lower_case<=0:
                messagebox.showinfo("warning","Password must contain a lower case alphabet")
            elif number<=0:
                messagebox.showinfo("warning","Password must contain a Number")
            elif special_charecter<=0:
                messagebox.showinfo("warning","Password must contain a Special Character [@,#,*,$,%,&,!]")
            else:
                return True
    #****************************************************** function to validate password and confirm password*****************************************************************************************
    def password_confirm_match():
        if password==confirm_password:
            return True
        else:
            messagebox.showwarning("warning","Password does not Match")
    if name_validator():
        if email_validate():
            if password_validate():
                if password_confirm_match():
                    #**************************************checking connection with database***********************************************************************************************************
                    if mycon.is_connected()==False:
                        messagebox.showerror("Error","There some Technical issue in connecting database")
                    else:
                        #**********************************firing query to insert data into database***************************************************************************************************
                        cursor=mycon.cursor()
                        query="insert into users(Name,Email,Password)values('{}','{}','{}')".format(name,email,password)
                        cursor.execute(query)
                        mycon.commit()
                        messagebox.showinfo("Congratulations","You are registered successfully go to login page")
                        create_new_acc_window.destroy()
                        login_page()
#**********************************************************creating new account page*******************************************************************************************************************
def create_new_acc_page():
    login_window.destroy()
    #******************************************************creating frame or window for create new account*********************************************************************************************
    global create_new_acc_window
    create_new_acc_window=customtkinter.CTk()
    create_new_acc_window.geometry("1920x1080")
    create_new_acc_window.title("Create New Account")
    #******************************************************inserting background image******************************************************************************************************************
    image1=ImageTk.PhotoImage(Image.open("background wallpaper4.jpg"))
    #******************************************************converting image into lable*****************************************************************************************************************
    background_frame1=customtkinter.CTkLabel(master=create_new_acc_window,image=image1)
    background_frame1.pack()    
    #******************************************************creating a new frame for create new account credentials ************************************************************************************
    create_new_acc_frame=customtkinter.CTkFrame(master=background_frame1,width=500,height=700,corner_radius=100)
    create_new_acc_frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    #******************************************************heading of login frame credential***********************************************************************************************************
    heading_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Create New Account",font=("Century Gothic",36))
    heading_label.place(x=50,y=45)
    #******************************************************creating lable for name*********************************************************************************************************************
    name_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Name:",font=("Century Gothic",20))
    name_label.place(x=50,y=150)
    #******************************************************creating entry box name*********************************************************************************************************************
    global new_name_variable
    new_name_variable=customtkinter.StringVar()
    name_entry=customtkinter.CTkEntry(master=create_new_acc_frame,width=400,placeholder_text="Name",placeholder_text_color="white",textvariable=new_name_variable,font=("Century Gothic",20))
    name_entry.place(x=50,y=200)
    name_entry.focus()
    #******************************************************creating lable for email********************************************************************************************************************
    email_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Email/Username:",font=("Century Gothic",20))
    email_label.place(x=50,y=250)
    #******************************************************creating entry box for email or username****************************************************************************************************
    global new_email_variable
    new_email_variable=customtkinter.StringVar()
    email_entry=customtkinter.CTkEntry(master=create_new_acc_frame,width=400,placeholder_text="Email/Username:",placeholder_text_color="white",textvariable=new_email_variable,font=("Century Gothic",20))
    email_entry.place(x=50,y=300)
    #******************************************************creating lable for password*****************************************************************************************************************
    password_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Password:",font=("Century Gothic",20))
    password_label.place(x=50,y=350)
    #******************************************************creating entry box for password*************************************************************************************************************
    global new_password_variable
    new_password_variable=customtkinter.StringVar()
    password_entry=customtkinter.CTkEntry(master=create_new_acc_frame,width=400,placeholder_text="Password",placeholder_text_color="white",textvariable=new_password_variable,show="*",font=("Century Gothic",20))
    password_entry.place(x=50,y=400)
    #******************************************************creating lable for confirm password*********************************************************************************************************
    password_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Confirm Password:",font=("Century Gothic",20))
    password_label.place(x=50,y=450)
    #******************************************************creating entry box for password*************************************************************************************************************
    global new_confirm_password_variable
    new_confirm_password_variable=customtkinter.StringVar()
    password_entry=customtkinter.CTkEntry(master=create_new_acc_frame,width=400,placeholder_text="Confirm Password:",placeholder_text_color="white",textvariable=new_confirm_password_variable,show="*",font=("Century Gothic",20))
    password_entry.place(x=50,y=500)
    #******************************************************creating lable for gender*******************************************************************************************************************
    #gender_label=customtkinter.CTkLabel(master=create_new_acc_frame,text="Gender:",font=("Century Gothic",20))
    #gender_label.place(x=50,y=550)
    #********************************creating combobox for gender****************************
    #new_gender_variable=customtkinter.StringVar()
    #gender_combobox=customtkinter.CTkOptionMenu(master=create_new_acc_frame,width=400,values=["Select option","Male","Female","Other"],variable=new_gender_variable)
    #gender_combobox.place(x=50,y=600)
    #******************************************************creating create new account button**********************************************************************************************************
    create_new_acc_button=customtkinter.CTkButton(master=create_new_acc_frame,width=400,text="Create New Account",corner_radius=6,font=("Century Gothic",16),height=50,command=create_new_account)
    create_new_acc_button.place(x=50,y=575)
    create_new_acc_window.mainloop()
#**********************************************************Setting environment ************************************************************************************************************************
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
#**********************************************************function for login**************************************************************************************************************************
def login():
    #******************************************************fetching value******************************************************************************************************************************
    login_page_email=email_variable.get()
    login_page_email=login_page_email.strip()
    login_page_password=password_variable.get()
    login_page_password=login_page_password.strip()
    #******************************************************checking for database connection ***********************************************************************************************************
    if mycon.is_connected()==False:
        messagebox.showerror("Error","There some Technical issue in connecting database")
    else:
        #**************************************************executing SQL Query*************************************************************************************************************************
        cursor=mycon.cursor()
        cursor.execute("select Password,Name from users where email='{}'".format(login_page_email))        
        data=cursor.fetchall()
        #**************************************************return empty list if no data found else return the data as list of tuples*******************************************************************
        if len(data)==0:
            #**********************************************error message if user not found or data not found*******************************************************************************************
            messagebox.showinfo("User not found","looks like you have entered wrong Email-ID or you are new to our application ")
        else:
            #**********************************************checking for password correctness***********************************************************************************************************
            saved_password=data[0][0]
            global saved_name
            saved_name=data[0][1]
            if saved_password==login_page_password:
                welcome_page()
            else:
                #******************************************error message if password mismatched********************************************************************************************************
                messagebox.showerror("Error","Incorrect Password")
def login_page():
    #******************************************************creating first window or frame**************************************************************************************************************
    global login_window
    login_window=customtkinter.CTk()
    login_window.geometry("1920x1080")
    login_window.title("Login Page")
    #******************************************************inserting background image******************************************************************************************************************
    image1=ImageTk.PhotoImage(Image.open("background wallpaper4.jpg"))
    #******************************************************converting image into lable*****************************************************************************************************************
    background_frame1=customtkinter.CTkLabel(master=login_window,image=image1)
    background_frame1.pack()
    #******************************************************creating a new frame for login credentials**************************************************************************************************
    login_credential_frame=customtkinter.CTkFrame(master=background_frame1,width=500,height=500,corner_radius=100)
    login_credential_frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    #******************************************************heading of login frame credential***********************************************************************************************************
    heading_label=customtkinter.CTkLabel(master=login_credential_frame,text="Log into your Account",font=("Century Gothic",36))
    heading_label.place(x=50,y=45)
    #******************************************************creating lable for email********************************************************************************************************************
    email_label=customtkinter.CTkLabel(master=login_credential_frame,text="Email/Username:",font=("Century Gothic",20))
    email_label.place(x=50,y=150)
    #******************************************************creating entry box for email or username****************************************************************************************************
    global email_variable
    email_variable=customtkinter.StringVar()
    email_entry=customtkinter.CTkEntry(master=login_credential_frame,width=400,placeholder_text="Email/Username",placeholder_text_color="white",textvariable=email_variable,font=("Century Gothic",20))
    email_entry.place(x=50,y=200)
    email_entry.focus()
    #******************************************************creating lable for password*****************************************************************************************************************
    password_label=customtkinter.CTkLabel(master=login_credential_frame,text="Password:",font=("Century Gothic",20))
    password_label.place(x=50,y=250)
    #******************************************************creating entry box for password*************************************************************************************************************
    global password_variable
    password_variable=customtkinter.StringVar()
    password_entry=customtkinter.CTkEntry(master=login_credential_frame,width=400,placeholder_text="Password",placeholder_text_color="Black",textvariable=password_variable,show="*",font=("Century Gothic",20))
    password_entry.place(x=50,y=300)
    #******************************************************creating login button***********************************************************************************************************************
    login_button=customtkinter.CTkButton(master=login_credential_frame,width=400,text="Login",corner_radius=6,font=("Century Gothic",18),command=login)
    login_button.place(x=50,y=350)
    #******************************************************creating create new account button**********************************************************************************************************
    create_new_acc_button=customtkinter.CTkButton(master=login_credential_frame,width=400,text="Create New Account",corner_radius=6,font=("Century Gothic",18),command=create_new_acc_page)
    create_new_acc_button.place(x=50,y=400)
    login_window.mainloop()
login_page()
