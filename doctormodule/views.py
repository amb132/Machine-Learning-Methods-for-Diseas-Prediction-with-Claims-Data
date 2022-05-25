from pydoc import Doc
from sklearn.ensemble import RandomForestClassifier
from django.shortcuts import render,redirect
from .models import Doctor
# Create your views here.
from .models import Patients
loginUser = ""
loginFlag = False
forgotEmpID = ""

def index(request):

    return render(request,'doctormodule/index.html')


def register(request):
    if request.method == 'POST':
        print()
        print(type(request.POST))
        print()

        doc_id = request.POST['doc_id']
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        dept = request.POST['dept']

        gender = request.POST['gender']
        phone = request.POST['phone']
        repeat_password = request.POST['repeat_password']
        hospital=request.POST['hospital']
        print(doc_id, name, password, email, dept,  gender, phone, repeat_password,hospital)
        count = 0
        message = ""
        searchObject = Doctor.objects.all()
        flag = 1
        for i in range(len(searchObject)):
            lst = str(searchObject[i]).split(";")
            print(lst[0], doc_id)
            if lst[0] == doc_id:
                message = message + "Doctor already exists.\n"
                flag = 0
                break
        if flag == 1:
            count = count + 1

        if password == repeat_password:
            if len(password) > 6:
                flag1, flag2, flag3 = 0, 0, 0
                for i in range(len(password)):
                    ele = ord(password[i])
                    if ele > 96 and ele < 123:
                        flag1 = 1
                    elif ele > 47 and ele < 58:
                        flag2 = 1
                    elif ele > 64 and ele < 91:
                        flag3 = 1
                if flag1 == 1 and flag2 == 1 and flag3 == 1:
                    count = count + 1
                else:
                    message = message + "Re-enter the Password.\n"
        else:
            message = message + "Passwords does not match.\n"

        print(count)
        if count == 2:
            raw_text = password
            encrypt_text = raw_text
            Doctor(doc_id=doc_id,
                     name=name,
                     password=encrypt_text,
                     email=email,
                     dept=dept,
                     hospital=hospital,
                     gender=gender,
                     phone=phone).save()

            message = message + "Account Successfully Created."
        print(message)
        context = {'message': message}
        return render(request, 'doctormodule/register.html', context)

    else:
        message = "Welcome To Registration Page"
        context = {"message": message}
        return render(request, 'doctormodule/register.html', context)


def login(request):
    global loginFlag, loginUser
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username, password)
        message = ""

        if len(Doctor.objects.filter(doc_id=username)) == 0:
            message = message + "No Matching Accounts Found"
        else:
            pass_hash = str(Doctor.objects.filter(doc_id=username)[0]).split(";")[4]
            decrypt_text = pass_hash
            if password == decrypt_text:
                message = message + "Welcome to the Home Page"
                loginFlag = True
                loginUser = username
                print(loginUser)
                return redirect('home')
            else:
                message = message + "Wrong Password Entered"

        print(message)
        context = {"message": message}
        return render(request, 'doctormodule/login.html', context)

    else:
        return render(request, 'doctormodule/login.html')


def home(request):

    return render(request, 'doctormodule/home.html')


def copdresults(request):

    return render(request, 'doctormodule/copdresults.html')

def copd(request):
    if request.method == 'POST':
        print()
        print(type(request.POST))
        print()
        name = request.POST['name']
        AID = request.POST['AID']
        email = request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']
        Weight = request.POST['Weight']
        lip = request.POST['lip']
        FEV = request.POST['FEV']
        si = request.POST['si']
        temp = request.POST['temp']
        message=''

        print( name, AID, email, age, gender, Weight, lip, FEV,si,temp)

        FEV=float(FEV)
        si=float(si)
        import pandas as pd
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split

        str = 'doctormodule/copd_2.xlsx'

        read = pd.read_excel(str)

        X = read.loc[0:, ['age', 'gender', 'weight', 'lipcolor', 'FEV1', 'smoking intensity', 'temperature']]
        print(X)

        Y = read.loc[0:, ['label']]

        # print(Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state = 1)

        # print(len(X_train))

        # print(len(Y_train))

        # print(len(X_test))

        # print(len(Y_test))
        name, AID, email, age, gender, Weight, lip, FEV, si, temp


        Descisiontree = DecisionTreeClassifier()
        Descisiontree.fit(X_train, Y_train.values.ravel())
        prediction2 = Descisiontree.predict(X_test)
        print('TREE algorithm ranges', accuracy_score(Y_test, prediction2) * 100)
        print('Tree Prediction', Descisiontree.predict([[age, gender, Weight, lip, FEV, si,temp]]))
        copdpred=Descisiontree.predict([[age, gender, Weight, lip, FEV, si,temp]])
        if copdpred=='severe':
            treat='1.quit smoking,pulmonary rehab,2.short-acting bronchodilators,long-acting bronchodilators,bullectomy,3.lung  transplant'
        elif  copdpred=='mild':
            treat='1.quit smcoking,pulmonary rehab,2.short-acting bronchodilators '
        else:
             treat='1.quit smoking,pulmonary rehab,2.short-acting bronchodilators,long-acting bronchodilators'

        descision_tree_predicted=Descisiontree.predict(X_test)
        print("Descion tree accuracy",accuracy_score(descision_tree_predicted,Y_test)*100)


        Randomforest=RandomForestClassifier(n_estimators=5)
        Randomforest.fit(X_train,Y_train)
        random_forest_predicted = Randomforest.predict(X_test)
        print("Randomforest  accuracy", accuracy_score(random_forest_predicted, Y_test) * 100)


        from sklearn.neighbors import KNeighborsClassifier

        KNN=KNeighborsClassifier()
        KNN.fit(X_train,Y_train)
        KNN_predicted=KNN.predict(X_test)
        print("KNN  accuracy", accuracy_score(KNN_predicted, Y_test) * 100)

        new_data = Patients(name=name,AID=AID,email=email,
                             age=age,
                             gender=gender, type='COPD',
                             stage=copdpred, treatement=treat
                             )
        new_data.save()

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "techcitiforyou@gmail.com"
        receiver_email = email
        password = 'techcititech@123'

        message = MIMEMultipart("alternative")
        message["Subject"] = "Patient Medical Report"
        message["From"] = sender_email
        message["To"] = receiver_email
        data = 'data'
        # Create the plain-text and HTML version of your message
        text = """\
        """
        html = """\
        <html>
          <body>
            <p>Hi,<br>
             <p ><span style="width" class="">Patient Name :{0}   </span></p>
        <p ><span style="width" class="">Patient AID : {1}  </span></p>
        <p ><span style="width" class="">Patient Email : {2}  </span></p>
        <p ><span style="width" class="">Patient Gender :{3}   </span></p>

        <p ><span style="width" class="">Patient Type : {4}  </span></p>
        <p ><span style="width" class="">Disease Stage :  {5} </span></p>
        <p ><span style="width" class="">Patient Treatment :{6}   </span></p>

            </p>
            <p>
          </body>
        </html>
        """.format(name,AID,email,gender,"COPD",copdpred,treat)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )


            from sklearn.metrics import confusion_matrix
            cm1 = confusion_matrix(descision_tree_predicted, Y_test)
            print(cm1)
            import seaborn as sns
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 7))
            sns.heatmap(cm1, annot=True)
            plt.ylabel('Truth')
            plt.xlabel('Tree_Predicted')
            plt.show()

            cm2 = confusion_matrix(random_forest_predicted, Y_test)
            plt.figure(figsize=(10, 7))
            sns.heatmap(cm2, annot=True)
            plt.ylabel('Truth')
            plt.xlabel('Forest_Predicted')
            plt.show()



        return render(request, 'doctormodule/copdresults.html', {'name':name,'AID':AID
                      ,'email':email,'gender':gender,'type':'COPD',
                      'stage':copdpred,'treatement':treat})

        message = message + "Account Successfully Created."
        print(message)
        context = {'message': message}

        return render(request, 'doctormodule/copd.html', context)

    return render(request, 'doctormodule/copd.html')




def diabetes(request):
    if request.method == 'POST':
        print()
        print(type(request.POST))
        print()


        name = request.POST['name']
        AID = request.POST['AID']
        email = request.POST['email']
        gender = request.POST['gender']
        Pregnancies = request.POST['Pregnancies']
        Glucose = request.POST['Glucose']
        BloodPressure = request.POST['BloodPressure']
        SkinThickness = request.POST['SkinThickness']
        Insulin = request.POST['Insulin']
        BMI = request.POST['BMI']
        DiabetesPedigreeFunction = request.POST['DiabetesPedigreeFunction']
        Age = request.POST['Age']
        message=''
        Insulin=float(Insulin)
        DiabetesPedigreeFunction=float(DiabetesPedigreeFunction)
        print( name, AID, email, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,BMI,DiabetesPedigreeFunction
                 ,Age)

        import pandas as pd
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split
        message=''
        str = 'doctormodule/diabetes.csv'

        read = pd.read_csv(str)

        X = read.loc[0:,
            ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age']]
        print(X)

        Y = read.loc[0:, ['Outcome']]

        # print(Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=42)

        # print(len(X_train))

        # print(len(Y_train))

        # print(len(X_test))

        # print(len(Y_test))

        model2 = DecisionTreeClassifier()
        model2.fit(X_train, Y_train.values.ravel())
        prediction2 = model2.predict(X_test)
        print('TREE algorithm Accuracy', accuracy_score(Y_test, prediction2) * 100)
        print('Tree Prediction', model2.predict([[  Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,BMI,DiabetesPedigreeFunction
                 ,Age]]))
        prediction = model2.predict([[  Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,BMI,DiabetesPedigreeFunction
                 ,Age]])
        print(prediction)




        if prediction == [0]:
            print('Moderate sugar , no need any treatement')
            treat='Moderate sugar , no need any treatement'
        elif prediction == [1]:
            print('Either oral medication or insulin should be taken accordingly')
            treat = 'Either oral medication or insulin should be taken accordingly'
        else:
            print(" couldn't able to find the stage ")

        Randomforest = RandomForestClassifier(n_estimators=5)
        Randomforest.fit(X_train, Y_train)
        random_forest_predicted = Randomforest.predict(X_test)
        print("Randomforest  accuracy", accuracy_score(random_forest_predicted, Y_test) * 100)

        from sklearn.neighbors import KNeighborsClassifier

        KNN = KNeighborsClassifier()
        KNN.fit(X_train, Y_train)
        KNN_predicted = KNN.predict(X_test)
        print("KNN  accuracy", accuracy_score(KNN_predicted, Y_test) * 100)

        new_data = Patients(name=name, AID=AID, email=email,
                            age=Age,
                            gender=gender, type='DIABETES',
                            stage=prediction, treatement=treat
                            )
        new_data.save()

        message = message + "Account Successfully Created."
        print(message)
        context = {'message': message}

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "techcitiforyou@gmail.com"
        receiver_email = email
        password = 'techcititech@123'

        message = MIMEMultipart("alternative")
        message["Subject"] = "Patient Medical Report"
        message["From"] = sender_email
        message["To"] = receiver_email
        data = 'data'
        # Create the plain-text and HTML version of your message
        text = """\
                Hi,
                How are you?
                Real Python has many great tutorials:
                www.realpython.com"""
        html = """\
                <html>
                  <body>
                    <p>Hi,<br>
                     <p ><span style="width" class="">Patient Name :{0}   </span></p>
                <p ><span style="width" class="">Patient AID : {1}  </span></p>
                <p ><span style="width" class="">Patient Email : {2}  </span></p>
                <p ><span style="width" class="">Patient Age :{3}   </span></p>

                <p ><span style="width" class="">Patient Type : {4}  </span></p>
                <p ><span style="width" class="">Disease Stage :  {5} </span></p>
                <p ><span style="width" class="">Patient Treatment :{6}   </span></p>

                    </p>
                    <p>
                  </body>
                </html>
                """.format(name, AID, email, Age, "Diabetes", prediction, treat)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

            from sklearn.metrics import confusion_matrix
            cm1 = confusion_matrix(prediction2, Y_test)
            print(cm1)
            import seaborn as sns
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 7))
            sns.heatmap(cm1, annot=True)
            plt.ylabel('Truth')
            plt.xlabel('Tree_Predicted')
            plt.show()

            cm2 = confusion_matrix(random_forest_predicted, Y_test)
            plt.figure(figsize=(10, 7))
            sns.heatmap(cm2, annot=True)
            plt.ylabel('Truth')
            plt.xlabel('Forest_Predicted')
            plt.show()

        return render(request, 'doctormodule/diabetesresults.html', {'name':name,'AID':AID
                      ,'email':email,'gender':gender,'type':'DIABETES',
                      'stage':prediction,'treatement':treat})

    return render(request, 'doctormodule/diabetes.html')



def heart(request):
    if request.method == 'POST':
        print()
        print(type(request.POST))
        print()


        name = request.POST['name']
        AID = request.POST['AID']
        email = request.POST['email']
        Age = request.POST['Age']
        sex = request.POST['sex']
        cp = request.POST['cp']
        trestbps = request.POST['trestbps']
        chol = request.POST['chol']
        fbs = request.POST['fbs']

        restecg = request.POST['restecg']
        thalach = request.POST['thalach']
        exang = request.POST['exang']
        oldpeak = request.POST['oldpeak']
        oldpeak=float(oldpeak)
        slope = request.POST['slope']
        ca = request.POST['ca']
        thal = request.POST['thal']
        print(name, AID, email, Age, sex, cp, trestbps, chol, fbs,
              restecg,thalach,exang,oldpeak,slope,ca,thal)
        import pandas as pd
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split

        str = 'doctormodule/heart.csv'

        read = pd.read_csv(str)

        X = read.loc[0:,
            ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca',
             'thal']]
        print(X)

        Y = read.loc[0:, ['target']]

        # print(Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=42)

        # print(len(X_train))

        # print(len(Y_train))

        # print(len(X_test))

        # print(len(Y_test))
        message=''
        model2 = DecisionTreeClassifier()
        model2.fit(X_train, Y_train.values.ravel())
        prediction2 = model2.predict(X_test)
        print('TREE algorithm ranges', accuracy_score(Y_test, prediction2) * 100)
        print('Tree Prediction', model2.predict([[Age, sex, cp, trestbps, chol, fbs,
              restecg,thalach,exang,oldpeak,slope,ca,thal]]))
        prediction = model2.predict([[Age, sex, cp, trestbps, chol, fbs,
              restecg,thalach,exang,oldpeak,slope,ca,thal]])
        print(prediction)
        if prediction == [0]:
            print('no heart disease')
            treat='no heart disease'
        elif prediction == [1]:
            print('medications should be given accordingly')
            treat ='medications should be given accordingly'
        else:
            treat=" couldn't able to find the stage "
            print(" couldn't able to find the stage ")

        new_data = Patients(name=name, AID=AID, email=email,
                            age=Age,
                            gender=sex, type='Heart',
                            stage=prediction, treatement=treat
                            )
        new_data.save()

        message = message + "Account Successfully Created."
        print(message)
        context = {'message': message}

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "techcitiforyou@gmail.com"
        receiver_email = email
        password = 'techcititech@123'

        message = MIMEMultipart("alternative")
        message["Subject"] = "Patient Medical Report"
        message["From"] = sender_email
        message["To"] = receiver_email
        data = 'data'
        # Create the plain-text and HTML version of your message
        text = """\
                        Hi,
                        How are you?
                        Real Python has many great tutorials:
                        www.realpython.com"""
        html = """\
                        <html>
                          <body>
                            <p>Hi,<br>
                             <p ><span style="width" class="">Patient Name :{0}   </span></p>
                        <p ><span style="width" class="">Patient AID : {1}  </span></p>
                        <p ><span style="width" class="">Patient Email : {2}  </span></p>
                        <p ><span style="width" class="">Patient Age :{3}   </span></p>

                        <p ><span style="width" class="">Patient Type : {4}  </span></p>
                        <p ><span style="width" class="">Patient Stage :  {5} </span></p>
                        <p ><span style="width" class="">Patient Treatment :{6}   </span></p>

                            </p>
                            <p>
                          </body>
                        </html>
                        """.format(name, AID, email, Age, type, prediction, treat)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return render(request, 'doctormodule/heartresults.html',{'name':name,'AID':AID
                      ,'email':email,'gender':sex,'type':'DIABETES',
                      'stage':prediction,'treatement':treat})

    return render(request, 'doctormodule/heart.html')



def accountUpdate(request):
    global loginUser,loginName
    message = ""
    print("Login Flag:",loginFlag)
    if loginFlag == False:
        return redirect('login')

    loginObj = str(Doctor.objects.filter(doc_id=loginUser)[0]).split(";")

    if request.method == 'POST':
        dept = request.POST['dept']
        contact = request.POST['contact']
        email = request.POST['email']
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        confnewpass = request.POST['confnewpass']

        if oldpass == "" or newpass == "" or confnewpass == "":
            Doc(doc_id=loginUser,name=loginObj[1],password=loginObj[4],dept=dept,phone=contact,
             email=email,gender=loginObj[2]).save()
            message = message + "Account Updated Successfully.\n"
        else:
            oldpassDB = loginObj[4]
            if oldpass == oldpassDB:
                if newpass == confnewpass:
                    if len(newpass)>6:
                        flag1,flag2,flag3 = 0,0,0
                        for i in range(len(newpass)):
                            ele = ord(newpass[i])
                            if ele>96 and ele<123:
                                flag1 = 1
                            elif ele>47 and ele<58:
                                flag2 = 1
                            elif ele>64 and ele<91:
                                flag3 = 1
                        if flag1 == 1 and flag2 == 1 and flag3 == 1:
                            encrpytPass = newpass
                            Doctor(doc_id=loginUser,name=loginObj[1],password=encrpytPass,dept=dept,phone=contact,
                            email=email,gender=loginObj[2]).save()
                            message = message + "Account Updated Successfully.\n"
                        else:
                            message = message +"Re-enter The Password. Does'nt Follow Password Constraints.\n"
                    else:
                        message = message + "Password Length is less than 7 Characters."
                else:
                    message = message + "New Passwords Does Not Match."
            else:
                message = message + "Old Password Does Not Match."

        loginObj = str(Doctor.objects.filter(doc_id=loginUser)[0]).split(";")

        context = {"empID":loginObj[0],"name":loginObj[1],"dept":loginObj[5],"contact":loginObj[6],"gender":loginObj[2],"email":loginObj[3],"message":message}
        return render(request,'doctormodule/account-update.html',context)
    else:
        # GET METHOD
        context = {"empID":loginObj[0],"name":loginObj[1],"dept":loginObj[5],"contact":loginObj[6],"gender":loginObj[2],"email":loginObj[3]}
        return render(request,'doctormodule/account-update.html',context)









def logout(request):
    global loginFlag, loginUser
    loginFlag = False
    loginUser = ""
    print("After Logout:", loginFlag, loginUser)
    return redirect('login')


def forgotpass(request):
    global forgotEmpID
    if request.method == "POST":
        forgotEmpID = request.POST['eid']
        if len(Doctor.objects.filter(doc_id=forgotEmpID)) == 0:
            message = "No Matching Employee ID Found."
            context = {"message": message}
            return render(request, "app1/forgotpass.html", context)

        return redirect("forgotpass2")
    else:
        return render(request, "app1/forgotpass.html")


def forgotpass2(request):
    global forgotEmpID
    message = ""
    if forgotEmpID == "":
        return redirect('forgotpass')

    forgotLst = str(Doctor.objects.filter(doc_id=forgotEmpID)[0]).split(";")
    if request.method == "POST":
        email = request.POST['email']
        quesID = request.POST['quesID']
        ans = request.POST['ans']
        psw = request.POST['psw']
        pswRep = request.POST['pswRep']

        if email == forgotLst[3]:
            if (quesID == "1" and ans == forgotLst[8]) or (quesID == "2" and ans == forgotLst[10]):
                if psw == pswRep:
                    if len(psw) > 6:
                        flag1, flag2, flag3 = 0, 0, 0
                        for i in range(len(psw)):
                            ele = ord(psw[i])
                            if ele > 96 and ele < 123:
                                flag1 = 1
                            elif ele > 47 and ele < 58:
                                flag2 = 1
                            elif ele > 64 and ele < 91:
                                flag3 = 1
                        if flag1 == 1 and flag2 == 1 and flag3 == 1:
                            encrpytPass = psw
                            Doctor(doc_id=forgotEmpID, name=forgotLst[1], password=encrpytPass, dept=forgotLst[5],
                                     phone=forgotLst[6],
                                     ques_1_id=forgotLst[7], ans_1=forgotLst[8], ques_2_id=forgotLst[9],
                                     ans_2=forgotLst[10], email=forgotLst[3], gender=forgotLst[2]).save()
                            message = "Password Updated Successfully."
                        else:
                            message = "Re-enter The Password. Does'nt Follow Password Constraints."
                    else:
                        message = "Password Length is less than 7 Characters."
                else:
                    message = "New Passwords Does Not Match."
            else:
                message = "Question and Answer Does Not Match."
        else:
            message = "Email ID Does Not Match."

        context = {"message": message, "ques1": ques1List[int(forgotLst[7])], "ques2": ques2List[int(forgotLst[9])],
                   "empID": forgotEmpID, "name": forgotLst[1]}
        return render(request, "app1/forgotpass2.html", context)
    else:
        context = {"ques1": ques1List[int(forgotLst[7])], "ques2": ques2List[int(forgotLst[9])], "empID": forgotEmpID,
                   "name": forgotLst[1]}
        return render(request, "app1/forgotpass2.html", context)


def addProduct(request):
    global loginFlag, loginName
    message = ""
    if loginFlag == False:
        return redirect('login')

    if request.method == "POST":
        pid = request.POST['pid']
        pname = request.POST['pname']
        pprize = request.POST['cprice']
        if len(Products.objects.filter(pId=pid)) == 0:
            Products(pId=pid, pName=pname, pPrize=pprize).save()
            message = "Added Product Successfully."
        else:
            message = "Product with this product ID already exists."

        context = {'message': message, 'name': loginName}
        return render(request, 'app1/addproduct.html', context)
    else:
        context = {'name': loginName}
        return render(request, 'app1/addproduct.html', context)
