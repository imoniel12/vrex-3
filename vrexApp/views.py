from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from .forms import Createschoolform

from .models import SchoolForm
from .forms import EventForm
from django.contrib.auth import get_user_model
from .models import Message
from .forms import MessageForm

#homepage
def home(request):

    return render(request,'vrexApp/index.html')

#register a user

def register(request):
     
     form = CreateUserForm()
     if request.method =="POST":
        
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    
     context = {'form':form}

     return render(request, 'vrexApp/register.html', context=context)


#register a user
def login(request):
    
    form = LoginForm()
    if request.method =="POST":
        
        form = LoginForm(request,data=request.POST)   

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request,user)
                return redirect ("dashboard")
                

    context = {'form':form}
    return render(request, 'vrexApp/login.html', context=context)



# @login_required(login_url='home')
# def home(request):

#     return render(request,'vrexApp/dashboard.html')
# - dashboard

@login_required(login_url='login')
def dashboard(request):

    return render(request,'vrexApp/dashboard.html')

# - dashboard

@login_required(login_url='announcement')
def announcement(request):

    return render(request,'vrexApp/announcement.html')



@login_required(login_url='formrequest')
def formrequest(request):
    if request.method == 'POST':
        form = Createschoolform(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the success page
            return render(request, 'vrexApp/success_page.html')
    else:
        form = Createschoolform()

    return render(request, 'vrexApp/formrequest.html', {'form': form})

@login_required(login_url='checkstatus')
def checkstatus(request):

    return render(request,'vrexApp/checkstatus.html')

@login_required(login_url='calendar')
def calendar(request):

    return render(request,'vrexApp/calendar.html')


#check status

@login_required(login_url='checkstatus')
def checkstatus(request):

    requested_forms = SchoolForm.objects.filter(user_type=request.user.user_type)

    return render(request, 'vrexApp/checkstatus.html', {'requested_forms': requested_forms})

#calendar
@login_required(login_url='calendar')
def calendar(request):
    form = EventForm()
    return render(request, 'vrexApp/calendar.html', {'form': form})


#chat
@login_required
def chat(request):
    admin_user = get_user_model().objects.filter(is_staff=True).first()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = admin_user
            message.save()
            # Redirect to the chat page after sending a message
            return redirect('chat')
    else:
        form = MessageForm()

    # Retrieve all messages between the current user and the admin
    user_messages = Message.objects.filter(sender=request.user, recipient=admin_user)
    admin_messages = Message.objects.filter(sender=admin_user, recipient=request.user)
    # Combine and order messages
    messages = user_messages.union(admin_messages).order_by('timestamp')

    return render(request, 'vrexApp/chat.html', {'form': form, 'messages': messages, 'recipient': admin_user})


#calendar
@login_required(login_url='financial')
def financial(request):
   
    return render(request, 'vrexApp/financial.html')


# - user logout

def logout(request):

    auth.logout(request)

    return redirect("login")

