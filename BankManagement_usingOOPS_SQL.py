import mysql.connector
import os 
import random
import time

conn = mysql.connector.connect(host='localhost', database='bankdb2', user='root', password='1234',buffered = True)
cursor = conn.cursor()


def clear():
    os.system('cls')

class Admin:

    def __init__(self):
        self.id = "ADMIN123"
        self.passkey = "1234"
        self.access = False
        
    def admin_login(self):
        check_id = input("Enter admin id : ")
        check_pass = input("Enter passkey : ")
        if(check_id == self.id and check_pass == self.passkey):
            self.access = True
            
        else :
            print("Enter valid credentials.")  
    
    def view_closed(self):
        if(self.access == True):
            print("---------------CLOSED ACCOUNTS---------------")
            sql = """SELECT * FROM bankdb2.closedacc""" 
            cursor.execute(sql)  
            for i in cursor:
                print(i) 

class Bank:
    def __init__(self):
        self.client_details_list = []
        self.loggedin = False
        self.TransferCash = False
     

    def register(self, name ,address,acctype, password):

        accno=random.randint(10000,100000)
        cash = int(input("Enter opening balance(greater than 5K for current acc.) : "))
        conditions = True

        if(acctype=='current' and cash<5000):
            conditions = False
            print("For current accounts opening balance should be greater than 5000")
            time.sleep(3)
            return              

        if conditions == True:
            print("Account created successfully")
            self.client_details_list = [name , accno , password ,address,acctype, cash]
            if(acctype=='savings'):
                sql1='insert into savingsacc(naam,accno,passwd,address,acctype,cash) values (%s,%s,%s,%s,%s,%s);'
                cursor.execute(sql1,self.client_details_list)
            if(acctype=='current'):
                sql2='insert into currentacc(naam,accno,passwd,address,acctype,cash) values (%s,%s,%s,%s,%s,%s);'
                cursor.execute(sql2,self.client_details_list)
            print("Your account number is ",accno,".")
            conn.commit()
            return


    def login(self, name , accno , password):   
        
        actype = input("Enter your account type : ")
        if(actype == "savings"):
            sql = 'select * from bankdb2.savingsacc where accno ='+str(accno)+';'
        elif(actype == "current"):
            sql = 'select * from bankdb2.currentacc where accno ='+str(accno)+';'
        else :
            print("You entered wrong account type!")   
        cursor.execute(sql)
        result = cursor.fetchone()
    
        if result[1]==str(accno):
            self.loggedin = True


        if self.loggedin == True:
            print("You are logged in")
            self.client_details_list = [result[0],result[1],result[2],result[3],result[4],result[5]]
        else:
            print("Wrong details")

        time.sleep(2)    
    
    def add_cash(self,amount):
        if amount > 0:
            self.client_details_list[5] += amount
            if self.client_details_list[4] == 'savings' :
                cursor.execute('select * from bankdb2.savingsacc;')
                sql = """update bankdb2.savingsacc set cash = %s where accno = %s"""
                cursor.execute(sql,(self.client_details_list[5],self.client_details_list[1],))
                conn.commit()

            if self.client_details_list[4] == 'current' :
                cursor.execute('select * from bankdb2.currentacc;')
                sql = """update bankdb2.currentacc set cash = %s where accno = %s"""
                cursor.execute(sql,(self.client_details_list[5],self.client_details_list[1],))
                conn.commit()
           
            print("Amount added successfully")

        else:
            print("Enter correct value of amount")
    
        time.sleep(3)

    def draw_cash(self,amount):
        
        if self.client_details_list[4] =='savings':
            sql1 ='select * from bankdb2.savingsacc where accno ='+self.client_details_list[1]+';'
            cursor.execute(sql1)

        if self.client_details_list[4] == 'current':
            sql2 ='select * from bankdb2.currentacc where accno ='+self.client_details_list[1]+';'
            cursor.execute(sql2)

        result = cursor.fetchone()
        left_cash = self.client_details_list[5] - amount
        self.client_details_list[5] = left_cash

        if left_cash > 0 :
            if self.client_details_list[4] == 'savings' :
                cursor.execute('select * from bankdb2.savingsacc;')
                sql ="""update bankdb2.savingsacc set cash = %s where accno = %s"""
                cursor.execute(sql,(left_cash,self.client_details_list[1],))
                conn.commit()
                print("Balance updated")

            if self.client_details_list[4] == 'current' :
                cursor.execute('select * from bankdb2.currentacc;')
                sql ="""update bankdb2.currentacc set cash = %s where accno = %s"""
                cursor.execute(sql,(left_cash,self.client_details_list[1],))
                conn.commit() 
        else:
            print("Insufficient Balance.")
        
        time.sleep(2)

    def Transfer_cash(self, amount,accno,recacctype):

        
        if recacctype == 'savings' :
            sql3 = """select * from bankdb2.savingsacc where accno = %s"""
            cursor.execute(sql3,(accno,))
            result = cursor.fetchone()
            if result[1]==accno:
                self.TransferCash = True
            

        if recacctype == 'current' :
            sql3 = """select * from bankdb2.currentacc where accno = %s"""
            cursor.execute(sql3,(accno,))
            result = cursor.fetchone()
            if result[1]==accno:
                self.TransferCash = True


        if self.TransferCash == True:

                if self.client_details_list[4] =='savings':
                    sql1 ="""select * from bankdb2.savingsacc where accno = %s"""
                    cursor.execute(sql1,(self.client_details_list[1],))

                if self.client_details_list[4] == 'current':
                    sql2 ="""select * from bankdb2.currentacc where accno = %s"""
                    cursor.execute(sql2,(self.client_details_list[1],))

                result = cursor.fetchone()
                total_cash = result[5] + amount
                left_cash = self.client_details_list[5] - amount
                self.client_details_list[5] = left_cash
                if amount > 0:
                    if recacctype == 'savings' :
                        cursor.execute('select * from bankdb2.savingsacc')
                        result = cursor.fetchone()
                        sql3 = """update bankdb2.savingsacc set cash =%s where accno = %s"""
                        cursor.execute(sql3,(total_cash,accno,))
                        conn.commit()

                    if recacctype == 'current' :
                        cursor.execute('select * from bankdb2.currentacc')
                        result = cursor.fetchone()
                        sql3 = """update bankdb2.currentacc set cash =%s where accno = %s"""
                        cursor.execute(sql3,(total_cash,accno,))
                        conn.commit()

                    if self.client_details_list[4] == 'savings' :
                        cursor.execute('select * from bankdb2.savingsacc')
                        sql = """update bankdb2.savingsacc set cash =%s where accno = %s"""
                        cursor.execute(sql,(self.client_details_list[5],self.client_details_list[1],))  
                        conn.commit()

                    if self.client_details_list[4] == 'current' :
                        cursor.execute('select * from bankdb2.currentacc')
                        sql = """update bankdb2.currentacc set cash =%s where accno = %s"""
                        cursor.execute(sql,(self.client_details_list[5],self.client_details_list[1],))   
                        conn.commit() 

                    print("Amount Transfered Successfully to",accno)
                    print("Balance left =",self.client_details_list[5])
                    time.sleep(2)

        else :
            print("Receiver's account does not exist.")
            time.sleep(2)

        
    def address_change(self,new_address):
        if self.client_details_list[4] == 'savings' :
            cursor.execute('select * from bankdb2.savingsacc')
            sql = """update bankdb2.savingsacc set address = %s where accno = %s"""
            cursor.execute(sql,(new_address,self.client_details_list[1],))
            conn.commit()
            self.client_details_list[3] = new_address
            print("New address set up successfull")
            time.sleep(2)

        if self.client_details_list[4] == 'current' :
            cursor.execute('select * from bankdb2.currentacc')
            sql = """update bankdb2.currentacc set address = %s where accno = %s"""
            cursor.execute(sql,(new_address,self.client_details_list[1],))
            conn.commit()
            self.client_details_list[3] = new_address
            print("New address set up successfull")
            time.sleep(2)
        conn.commit()    
            
    def acc_close(self):
        clear()
        closed_date = input("Enter the closing date : ")
        if(self.client_details_list[4]=='savings'):

            sql='insert into closedacc(naam,accno,address,acctype,closedate) values (%s,%s,%s,%s,%s);'
            cursor.execute(sql,(self.client_details_list[0],self.client_details_list[1],self.client_details_list[3],self.client_details_list[4],closed_date,))

            sql1="""DELETE FROM savingsacc WHERE accno = %s"""
            cursor.execute(sql1,(self.client_details_list[1],))

            print("Account closed successfully!")
            
        if(self.client_details_list[4]=='current'):

            sql='insert into closedacc(naam,accno,address,acctype,closedate) values (%s,%s,%s,%s,%s);'
            cursor.execute(sql,(self.client_details_list[0],self.client_details_list[1],self.client_details_list[3],self.client_details_list[4],closed_date,))

            sql1="""DELETE FROM currentacc WHERE accno = %s"""
            cursor.execute(sql1,(self.client_details_list[1],))

            print("Account closed successfully!")

        time.sleep(2)
        conn.commit()
    
    def simpleinterest(self):
        if(self.client_details_list[4] == "savings"):
            interest = (self.client_details_list[5] * 1 * 7.5) / 100 
            print("Simple interest for a year on amount ",self.client_details_list[5],"is", interest)
        else:
            print("Your account type is unsuitable!")   
        time.sleep(3)    

        


if __name__ == "__main__":

    Bank_object = Bank()
    clear()
    print("-----------Welcome to PyBank-----------")
    print("[1].Login")
    print("[2].Create a new Account")
    print("[3].Admin Login")
    user = int(input("Select an option : "))

    if user == 1:
        clear()
        print("Logging in")
        name = input("Enter Name : ")
        accno = int(input("Enter account Number : "))
        password = input("Enter password : ")
        Bank_object.login(name, accno, password)
        while True:
            if Bank_object.loggedin:
                clear()
                print("[1].Add Amount")
                print("[2].Withdraw Amount")
                print("[3].Check Balance")
                print("[4].Transfer Money")
                print("[5].Edit Profile")
                print("[6].Close Account")
                print("[7].View Account Details")
                print("[8].Calculate interest on current balance")
                print("[9].Logout")
                print("Enter your choice : ")
                login_user = int(input())

                if login_user == 1:
                    print("Balance =",Bank_object.client_details_list[5])
                    amount = int(input("Enter amount : "))
                    Bank_object.add_cash(amount)
                    print("\n[1].Back menu")
                    print("\n[2].Logout")
                    print("Enter your choice : ")
                    choose = int(input())
                    if choose == 1:
                        continue
                    elif choose == 2:
                        break
                        
                elif login_user == 2:
                    print("Balance =",Bank_object.client_details_list[5])
                    amount = int(input("Enter amount : "))
                    Bank_object.draw_cash(amount)
                    print("\n[1].Back menu")
                    print("\n[2].Logout")
                    print("Enter your choice : ")
                    choose = int(input())
                    if choose == 1:
                        continue
                    elif choose == 2:
                        break
                
                elif login_user == 3:
                    clear()
                    print("Balance =",Bank_object.client_details_list[5])
                    print("\n[1].Back menu")
                    print("\n[2].Logout")
                    print("Enter your choice : ")
                    choose = int(input())
                    if choose == 1:
                        continue
                    elif choose == 2:
                        break

                elif login_user == 4:
                    clear()
                    print("Balance =",Bank_object.client_details_list[5])
                    amount = int(input("Enter amount : "))
                    if amount >= 0 and amount <= Bank_object.client_details_list[5]:
                        accno = input("Enter reciever's account number : ")
                        recacctype = input("Enter reciver's account type :")
                        Bank_object.Transfer_cash(amount,accno,recacctype)
                        print("\n[1].Back menu")
                        print("\n[2].Logout")
                        print("Enter your choice : ")
                        choose = int(input())
                        if choose == 1:
                            continue
                        elif choose == 2:
                            break
                    elif amount < 0 :
                        print("Enter please correct value of amount")

                    elif amount > Bank_object.client_details_list[5]:
                        print("Not enough balance")

                elif login_user == 5:
                    clear()
                    print("\n[1].Address change")
                    print("Enter your choice : ")
                    edit_profile = int(input())

                    if edit_profile == 1:
                        clear()
                        new_address = (input("Enter new address : "))
                        Bank_object.address_change(new_address)
                        print("\n[1].Back menu")
                        print("\n[2].Logout")
                        print("Enter your choice : ")
                        choose = int(input())
                        if choose == 1:
                            continue
                        elif choose == 2:
                            break
                
                elif login_user ==6:
                    clear()
                    Bank_object.acc_close()
                    break

                elif(login_user==7):
                    clear()
                    if(Bank_object.client_details_list[4]=='savings'): 
                        sql="""select* from savingsacc where accno=%s;"""   
                        cursor.execute(sql,(Bank_object.client_details_list[1],))   

                    elif(Bank_object.client_details_list[4]=='current'):
                        sql="""select* from currentacc where accno=%s;"""   
                        cursor.execute(sql,(Bank_object.client_details_list[1],))   

                    result=cursor.fetchone()
                    print("Name : {}\nAccount number : {}\nAddress : {}\nAccount type : {}\nBalance : {}".format(result[0],result[1],result[3],result[4],result[5]))
                    time.sleep(4)

                elif login_user == 8:
                    clear()
                    Bank_object.simpleinterest()

                elif login_user == 9:
                    break
                        
                
    if user == 2:
        clear()
        print("--------------------ACCOUNT CREATION--------------------")
        name = input("Enter Name : ")
        password =input("Enter password : ")
        address = input("Enter address : ")
        acctype = input("Enter account type : ")
        Bank_object.register(name, address, acctype, password)

    if user == 3:
        clear()
        Admin_object = Admin()
        Admin_object.admin_login()
        
        if(Admin_object.access == True):
            print("--------------------ADMIN ACCESS--------------------")
            print("\n[1].View closed accounts")
            print("\n[2].Logout")
            print("Enter your choice : ")
            choose = int(input())
            if choose == 1:
                Admin_object.view_closed()
            elif choose == 2:
                pass

        else:
            print("Cannot login!")
            

conn.close()