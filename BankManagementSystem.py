import mysql.connector
from mysql.connector import IntegrityError

class InsufficientBalance(Exception):
    pass
class UserExcpetion(Exception):
    pass

class InvalidBalance(Exception):
    pass

class OptionError(Exception):
    pass

con = mysql.connector.connect(host="localhost",user ="root",password ="root")
mycursor = con.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS BankManagementDatabase")
mycursor.execute("use BankManagementDatabase")
mycursor.execute("create table if not exists users (username varchar(50) primary key, password varchar(50), age int, dob date,balance int)")

def dep(balance):


    try:
        bal=int(input("Enter the amount for deposit: "))
        balance = balance+bal
    except ValueError:
        print("Enter valid value")
    return balance

def withdraw(balance):
    try:
        withd = int(input("Enter the amount to withdraw: "))
        if(balance<withd):
            raise InsufficientBalance
        balance=balance-withd
    except ValueError:
        print("Enter valid value")
    return balance

def view(balance):
    if (balance<100000):
        print("Current Balance:",balance)
    else:
        raise InvalidBalance
    

def exit():
    print("Exit")
    

try:
    option = int(input("Enter 1 or 2: "))

    if(option==1):
        while True:
            print("Register to create account")
            user = input("Enter username: ")
            password = input("Enter Password: ")
            age = int(input("Enter your age: "))
            Dob = input("Enter your Date Of Birth (YYYY-MM-DD): ")

            try:
                balance = 20000
                mycursor.execute("insert into users(username,password,age,dob,balance) values (%s,%s,%s,%s,%s)",(user,password,age,Dob,balance))
                con.commit()
                print("Registration successfully!")
                break

            except IntegrityError as e:
                print("Username already exists please enter another username")

         
    elif (option==2):
        luser = input("Enter your username: ")
        lpassword = input("Enter your Password: ")

        mycursor.execute("Select balance from users where username = %s and password = %s",(luser,lpassword))
        result=mycursor.fetchone()

        if result is None:
            raise UserExcpetion("Invalid username or password")
        else:
            balance = result[0]

        print("Login successfuly")

        
        while True:
            a = int(input("Enter 1 to deposit\nEnter 2 to withdraw\nEnter 3 to display balance\nEnter 4 to exit\n"))
            
            if(a==1):
                balance=dep(balance)
                print("Updated balance is: ",balance)
                mycursor.execute("update users set balance = %s where username = %s",(balance,luser))
                con.commit()
                
            elif(a==2):
                balance=withdraw(balance)
                print("Updated balance is: ",balance)
                mycursor.execute("Update users set balance = %s where username = %s",(balance,luser))
                
            elif(a==3):
                balance=view(balance)
                
                

            elif(a==4):
                exit()
                break
            

    else:
        raise OptionError
            
except ValueError:
    print("Enter valid value")

except TypeError:
    print("Enter valid input")

except InsufficientBalance:
    print("Insufficient Balance")

except InvalidBalance:
    print("You can not hold Balance greater than 1000000")

except OptionError:
    print("Enter 1 or 2 only")