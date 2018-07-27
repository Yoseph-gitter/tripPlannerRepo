from django.shortcuts import render, redirect
from .models import User, Job 
from django.contrib import messages
import bcrypt
import re


def index(request):
    return render(request, "my_app/index.html")
def login(request):
    # validate 
    if request.method == "POST" :
        # Validate User Here atleast the email is correct
        errors = User.objects.validate_userInputs_For_LoggedInUsers(request.POST)
        if ( errors ):
            for key, value in errors.items() :
                messages.error(request , value)
                return redirect("/")
        else:
            # No validation Errors
            # check user in db error out if they are new
            # This loggin validator checks for 
            # 1 - if user does not exist , INFO message is logged and redirect to login page
            # 2 - else if user is new , we register it for the first time
            # 3 - else an existing user so logged him in and save loggedin state in session
            user = User.objects.filter(email = request.POST['email'])
            if (user.count() == 0 ):
                messages.info(request, "User Does Not Exist in the system, Please register !" )
                return redirect("/")

            elif bcrypt.checkpw(request.POST['password'].encode() , user.values()[0]['password'].encode() ):
                messages.success(request , "Successfully logged in!")
                request.session['email'] = request.POST['email']
                print("Email for loged in user ")
                print(request.session['email'])
            else:
                messages.error(request , "Wrong Password, try relogging again !")
                return redirect("/")

    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    messages.success(request, "Successfully logged out !")
    return redirect("/")

def register(request):
    # what happens if a non-logged in user tries to login with out first_name/last_name
    errors = User.objects.validate_userInputs_NoneLoggedInUser(request.POST)
    if ( errors ):
        for key, value in errors.items() :
            messages.error(request , value)
            return redirect("/")
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        request.session['email'] = request.POST['email']
        print("Email for loged in user ")
        print(request.session['email'])
        messages.success(request, "Successfully registered !")
    return redirect("/dashboard") 

def dashboard(request):

    loggedin_user = User.objects.get(email= request.session['email'])
   
    jobs_by_me = loggedin_user.joined_jobs.values()
    jobs = Job.objects.exclude(id__in=( loggedin_user.joined_jobs.values('id') ) )
    
    flagged_trips = []
    for jb in jobs:
        user_trip = {}
        if jb.created_by_id == loggedin_user.id :
            user_trip['is_created'] = True
        else:
            user_trip['is_created'] = False
        user_trip['job'] = jb
        flagged_trips.append(user_trip)
    
    context = {
        'modified_jobs': flagged_trips ,
        'jobs_by_me' : jobs_by_me,
        'user': loggedin_user

    }
    return render(request, "my_app/dashboard.html", context )

def addJob(request):
    return redirect("/addJob_render")
def addJob_render(request):
    return render(request, "my_app/createJob.html")

def createJob(request):
    # create the Job and redirect
    if request.method == "POST" :
        errors = Job.objects.validate_userInputs_NoneLoggedInUserForTrip(request.POST)
        if ( errors ):
            for key, value in errors.items() :
                messages.error(request , value)
                return redirect("/addJob_render")
        else:
            loggedin_user = User.objects.get(email= request.session['email']) 
            job = Job.objects.create(
                title = request.POST['title'] ,
                desc = request.POST['title'] ,
                location = request.POST['title'] ,
                created_by = loggedin_user
            )
            # job.joined_users.add(loggedin_user)
            job.save()

    return redirect("/dashboard")


def edit(request, job_id):
    selected_job = Job.objects.get(id=job_id)

    context = {
        'job_id': selected_job.id ,
        'title': selected_job.title,
        'desc' : selected_job.desc,
        'location': selected_job.location
    }

    return render(request, "my_app/edit.html", context )

def editJob(request, job_id):
    loggedin_user = User.objects.get(email= request.session['email']) 
    
    job = Job.objects.get(id=job_id)
    job.title = request.POST['title']
    job.desc = request.POST['desc']
    job.location = request.POST['location']
    job.save()
    print("Edieted Jobs")
    return redirect("/dashboard")

def back(request):
    return redirect("/dashboard")

def add(request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(email=request.session['email'])
    user.joined_jobs.add(job)
    user.save()

    return redirect("/dashboard")

def view(request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(email=request.session['email'])


    context ={
        'user' : user ,
        'job' : job
    }

    return render(request, "my_app/checkout.html", context)

def cancel(request, job_id):
    Job.objects.get(id=job_id).delete()
    
    return redirect("/dashboard")

def done(request, job_id):
    Job.objects.get(id=job_id).delete()
    
    return redirect("/dashboard")