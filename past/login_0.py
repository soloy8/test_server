import streamlit as st
import pandas as pd


import sqlite3
conn,cur=None,None
conn = sqlite3.connect('capstoneDB.db')
cur=conn.cursor()

def create_usertable():
        cur.execute('CREATE TABLE IF NOT EXISTS userTable(username TEXT,password TEXT)')

def add_userdata(username,password):
        cur.execute('INSERT INTO userTable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        cur.execute('SELECT*FROM userTable WHERE username =? AND password=?',(username,password))
        data=cur.fetchall()
        return data

def view_all_users():
    cur.execute('SELECT*FROM usertable')
    data=cur.fetchall()
    return data

def main():
    #공통실행
    st.title("simple login")

    #선택실행
    menu=["Home","Login","Signup"]  
    choice=st.sidebar.selectbox("Menu",menu)

    ## home(작동확인)
    if choice == "Home":
        st.subheader("Home")


    ## Login
    # c.f. subheader9 미존재로 error
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        
       	password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.button("Login"):
               create_usertable()
               result=login_user(username,password)
               if result:
                     st.success("Logged In as {}".format(username))
                     task=st.selectbox("Task",["Add Post","Analytics","Profiles"])
                     if task == "Add Post":
                         st.subheader("Add your Post")
                     elif task == "Analytics":
                         st.subheader("Analytics")
                     elif task == "Profiles":
                         st.subheader("User Profiles")
                         user_result = view_all_users()
                         clean_db=pd.DataFrame(user_result,columns=["Username","Password"])
                         st.dataframe(clean_db)
               else:
                   st.warning("Incorrect Username/Password")


    ##Sign_up
    # =
    elif choice == "Signup":
        st.subheader("Create New Account")
        new_user=st.text_input("Username")
        new_password=st.text_input("Password",type='password')
        if st.button("Signup"):
             create_usertable()
             add_userdata(new_user,new_password)
             st.success("You have successfully created a valid Account")
             st.info("Go to Login Menu to login")


## run
main()