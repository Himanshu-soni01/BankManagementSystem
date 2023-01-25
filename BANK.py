import sqlite3
import BMS
x=BMS.cur

def DOB():
    while True:
        db=list(map(str,input().split()))
        if len(db)!=3:
            print("INVALID...")
            continue
        elif int(db[1])==2:
            if int(db[0])<0 or int(db[0])>28:
                continue
        elif int(db[1]) in [4,6,9,11]:
            if int(db[0])<0 or int(db[0])>30:
                continue
        elif int(db[0])>31 or int(db[0])<0:
            print("INVALID  DATE...")
            continue
        elif int(db[1])<0 or int(db[1])>12:
            print("INVALID MONTH...")
            continue
        elif int(db[2])<1950 or int(db[2])>2022:
            print("INVALID YEAR...")
            continue
        return '.'.join(db)
    
def AccNo():
    res=x.execute('select AccNo from account')
    last=res.fetchall()[-1][0]
    return last+1

def cn():
    while True:
        c=int(input())
        if len(str(c))!=10 and c>0:
            continue
        return c

def ob():
    while True:
        ob=int(input())
        if ob<0:
            continue
        return ob

def pas():
    while True:
        try:
            p=int(input())
        except ValueError:
            print("INVALID PASSWORD...")
            continue
        else:
            if p<1001 or p>9999:
                print("INVALID PASSWORD..")
                continue
            return p

def chkpwd(ac,pwd):
    q='select Password from account where AccNo=(?)'
    x.execute(q,(ac,))
    res=x.fetchone()
    if res[0]==pwd:
        return True
    return False

def openAcc():
    n=input("Enter the Name: ")
    print("Enter Date of birth DD//MM//YY with spaces: ",end=" ")
    db=DOB()
    print("Enter Password for your Account: ",end=" ")
    p=pas()
    add=input("Enter the Address: ")
    print("Enter your Contact number: ",end=" ")
    c=cn()
    print("Enter the Opening Balance: ",end=" ")
    b=ob()
    d1=(n,AccNo(),p,c,db,add,b)
    d2=(AccNo(),p,b)
    q1=('INSERT INTO account values (?,?,?,?,?,?,?)')
    q2=('INSERT INTO amount values (?,?,?)')
    x.execute(q1,d1)
    x.execute(q2,d2)
    BMS.conn.commit()
    ac=AccNo()-1
    print("Your Account Number is : ",ac)
    print("...DATA ENTERED SUCCESSFULLY...")
    main()

def deptAmt():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        amt=int(input("Enter the amount you want to deposit: "))
        a='select Balance from amount where AccNo=(?)'
        x.execute(a,(ac,))
        result=x.fetchone()
        t=result[0]+amt
        sql='update amount set Balance=(?) where AccNo=(?)'
        d=(t,ac,)
        x.execute(sql,d)
        BMS.conn.commit()
    else:
        print("...INVALID PASSWORD...")
        deptAmt()
    main()

def withAmt():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        amt=int(input("Enter the withdrawl amount: "))
        q1='select balance from amount where AccNo=(?)'
        x.execute(q1,(ac,))
        result=x.fetchone()
        t=result[0]-amt
        q2='update amount set balance=(?) where AccNo=(?)'
        d2=(t,ac,)
        x.execute(q2,d2)
        BMS.conn.commit()
    else:
        print("...INVALID PASSWORD...")
        withAmt()
    main()

def balEnq():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        q1='select Balance from amount where AccNo=(?)'
        x.execute(q1,(ac,))
        result=x.fetchone()
        print('Balance from Account: ',ac," is ",result[0])
    else:
        print("...INVALID PASSWORD...")
        balEnq()
    main()

def tnfAmt():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        amt=int(input("Enter the Amount: "))
        q1='select Balance from amount where AccNo=(?)'
        x.execute(q1,(ac,))
        result=x.fetchone()    
        print(result)
        t=result[0]-amt
        q11='update amount set Balance=(?) where AccNo=(?)'
        d11=(t,ac,)
        x.execute(q11,d11)

        tac=int(input("Enter the transferer Account number: "))
        q2='select balance from amount where AccNo=(?)'
        x.execute(q2,(tac,))
        result=x.fetchone()
        r=result[0]+amt
        q22='update amount set Balance=(?) where AccNo=(?)'
        d22=(r,tac,)
        x.execute(q22,d22)
        BMS.conn.commit()
    else:
        print("...INVALID PASSWORD...")
        tnfAmt()
    main()

def dispDet():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        # q='select * from  account where AccNo=(?)'
        q='create view display AS select Name,AccNo,Contact,DOB,Address,OpeningBalance from account'
        x.execute(q)
        q1='select * from display where AccNo=(?)'
        x.execute(q1,(ac,))
        res=x.fetchall()
        for record in res:
            print(*record,sep="|\t")
        # print(res)
        x.execute('drop view display')
        BMS.conn.commit()
    else:
        print("...INVALID PASSWORD...")
        dispDet()
    main()

def closeAcc():
    ac=int(input("Enter your Account number: "))
    pwd=int(input("Enter Password: "))
    if chkpwd(ac,pwd):
        q1='delete from account where AccNo=(?)'
        q2='delete from amount where AccNo=(?)'
        d=(ac,)
        x.execute(q1,d)
        x.execute(q2,d)
        BMS.conn.commit()
    else:
        print("...INVALID PASSWORD...")
        closeAcc()
    main()

def main():
    print('''
            1. New Account Open
            2. Deposit Amount
            3. Withdraw Amount
            4. Balance Enquiry
            5. Transfer Amount
            6. Display Customer Details
            7. Close an Account''')
        
    choice=input("Enter your Task you want to perform: ")
    if(choice=='1'):
        openAcc()
    elif(choice=='2'):
        deptAmt()
    elif(choice=='3'):
        withAmt()
    elif(choice=='4'):
        balEnq()
    elif(choice=='5'):
        tnfAmt()
    elif(choice=='6'):
        dispDet()
    elif(choice=='7'):
        closeAcc()
    else:
        print("...INVALID ENTRY...")
main()