from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from . import views
from .models import *
import bcrypt
import re
import _mysql
import MySQLdb
import datetime
from django.utils import timezone


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9]+@[A-Za-z0-9]+\.[a-zA-Z0-9]+$")

# Create your views here.
def index(request):
    return render(request,'wall/login.html')

def register(request):
    valid = True
    
    if len(request.POST['first_name'])<2:
        valid = False
        print('setted valid as False.')
        messages.error(request,"First Name needs at least 2 character!")
        
    if len(request.POST['last_name'])<2:
        valid = False
        messages.error(request,"Last Name needs at least 2 character!")
        
    if len(request.POST['email'])<2:
        valid = False
        messages.error(request,"Email needs at least 2 character!")
        
    if len(request.POST['password'])<2:
        valid = False
        messages.error(request,"Password needs at least 2 character!")
        
    if len(request.POST['confirm_password'])<2:
        valid = False
        messages.error(request,"Confirm password needs at least 2 character!")
        
    if request.POST['password']!=request.POST['confirm_password']:
        valid = False
        messages.error(request,"Password does not match!")
        
    if User.objects.filter(email=request.POST['email']).count()!=0:
        valid = False
        messages.error(request,"Email Was Already Registered!")
        
    if valid == False:
        print('before redirect to root!')
        return redirect('/')

    else:
        print('Trying to create record...')
        # create password hash
        encoded = request.POST['password'].encode('utf-8')
        #pwHash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        pwHash = bcrypt.hashpw(encoded,bcrypt.gensalt())
        print('created pwHash= ',pwHash)
        decoded = pwHash.decode('utf-8')
        print('decoded pwHash= '+decoded)
        User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],password=decoded,email=request.POST['email'])
        print(User.objects.all())
        return redirect('/')

def login(request):
    valid = True
    # input validations and login
    if len(request.POST['email'])<2:
        valid = False
        messages.error(request,"Name needs at least 2 character")
        
    if len(request.POST['password'])<2:
        valid = False
        messages.error(request,"password needs at least 2 character")
        
    if not EMAIL_REGEX.match(request.POST['email']):
        valid = False
        messages.error(request,"Invalid Email address!")

    if valid == False:
        return redirect('/')

    else:
        # get email
        # db = _mysql.connect(host,user,password,database)
        # db.query("""SELECT * FROM users WHERE email = ('%s')"""%email)
        #c = db.cursor()
        user = User.objects.get(email=request.POST['email'])
        inputpw = request.POST['password']
        print('before encode input='+inputpw)
        encoded = inputpw.encode('utf-8')
        print('after encode inputpw='+str(encoded))
        if bcrypt.checkpw(encoded, user.password.encode('utf-8')):
            print("password match")
            # store user and uid to session 
            request.session["first_name"] = user.first_name
            request.session["last_name"]=user.last_name
            request.session["uid"] = user.id    
            return redirect('/wall')
        else:
            print("failed password check!")
            messages.error(request,"Password Doesn't Match!")
            return redirect('/')
# >>> r.fetch_row()
# (('1', b'Edward', b'$2b$12$tLiLfCUwZ.Uzyubnor7W8ekyGnvXGtalc39QHOJ9/ikZlVxu2qT6K', b'sampleEmail@123.net', '2018-06-12 13:55:39'),)
# >>> r.fetch_row()
# (('2', b'Eugene', b'$2b$12$h4YFrpa78gUk6fFyzcZUsuxMG.F/5Rxefz7M1O5JWpZ9dI/aMqAX6', b'eugene123@mail.com', '2018-06-12 13:57:10'),)
# >>> r.fetch_row()

#after login successfully
def renderWall(request):
    # query messages and comments with uid in session
    current = User.objects.get(id=request.session["uid"])
    context={
        "messages":Message.objects.all().reverse().order_by("created_at"),
        "comments":Comment.objects.all().order_by("created_at")
        #"comments":Comment.objects.
    }
    return render(request,'wall/wall.html',context)

# post a message
def post_msg(request):  # note that user_id is the one in DB Browser !!!
    if 'errors' in request.session:
        del request.session['errors']
    Message.objects.create(message=request.POST['new_message'],user_id=request.session['uid'])
    return redirect('/wall')

# post a comment
def post_cmt(request): # user_id, message_id all find it in DB Browser!!!!  use hiddent form for message_id
    if 'errors' in request.session:
        del request.session['errors']
    Comment.objects.create(comment=request.POST['cmttext'],user_id=request.session['uid'],message_id=request.POST['msgid'])
    return redirect('/wall')

# delete message only if its made within 30 minutes
def del_msg(request,number):
    errors = []
    msg_id = int(number)
    the_msg = Message.objects.get(id=msg_id)
    if the_msg.user.id == request.session["uid"]: # this is the logged in user
        print(' you are the one who Posted it!')
    else:
        errors.append("You cannot delete other users' messages!")
        request.session['errors']=errors
        return redirect('/wall')
    now = timezone.now()
    print('Now is:'+str(now))
    diff = now - the_msg.created_at
    print('The Difference between now and created_at:')
    print(str(diff))
    delete_threshold = datetime.timedelta(minutes=30) # define a 30mins in timedelta
    print(diff > delete_threshold)
    if diff > delete_threshold:
        errors.append("You cannot Delete the Old Message!")
        request.session['errors']=errors
        return redirect('/wall')
    else:
       the_msg.delete()
       
    return redirect('/wall')

# delete comment
def del_cmt(request,number):
    cmt_id = int(number)
    the_cmt = Comment.objects.get(id=cmt_id)
    the_cmt.delete()
    return redirect('/wall')

# clear session
def logOut(request):
    request.session.flush()
    return redirect('/')