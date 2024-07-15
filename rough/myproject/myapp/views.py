# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# from django.http import JsonResponse
# import joblib
# import numpy as np
# import os
# from django.conf import settings

# # Define the path to the model file
# model_path = os.path.join(settings.BASE_DIR, 'fraud_detection_model.pkl')



from django.shortcuts import render, redirect
from django.http import JsonResponse
import joblib
import numpy as np
import os
from django.conf import settings



from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
# from .models import Data
 

# Define the path to the model file
model_path = os.path.join(settings.BASE_DIR, 'fraud_detection_model.pkl')

# Load the model
model = joblib.load(model_path)

def predict_fraud(request):
    if request.method == 'POST':
        # Extract features from the request
        type_ = int(request.POST.get('type'))
        amount = float(request.POST.get('amount'))
        oldbalanceOrg = float(request.POST.get('oldbalanceOrg'))
        newbalanceOrig = float(request.POST.get('newbalanceOrig'))
        
        # Prepare features for prediction
        features = np.array([[type_, amount, oldbalanceOrg, newbalanceOrig]])
        
        # Make prediction
        prediction = model.predict(features)
        
        # Result
        result = 'Fraud' if prediction[0] == 1 else 'No Fraud'
        
        # Render the result in a new template
        return render(request, 'result.html', {'prediction': result})
    
    return render(request, 'predict.html')

def home(request):
    return render(request, 'home.html')

# def register(request):
#     return render(request, 'register.html')

# def login(request):
#     return render(request, 'login.html')


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email already exists')
#                 return redirect('register')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already exists')
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password1)
#                 user.save()
#                 return redirect('login')
#         else:
#             messages.info(request, 'Passwords do not match')
#             return redirect('register')
#     return render(request,'register.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return render(request, 'home.html')
#         else:
#             messages.info(request, 'Invalid credentials')
#             return redirect('login')
#     else:
#         return render(request, 'login.html')
    
    
# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.contrib.auth import authenticate, login as auth_login

# User = get_user_model()

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email already exists')
#                 return redirect('register')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already exists')
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password1)
#                 user.save()
#                 messages.success(request, 'Account created successfully!')
#                 return redirect('login')
#         else:
#             messages.info(request, 'Passwords do not match')
#             return redirect('register')
#     return render(request, 'register.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             return render(request, 'home.html')
#         else:
#             messages.info(request, 'Invalid credentials')
#             return redirect('login')
#     else:
#         return render(request, 'login.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login

from .models import Data  # Import your Data model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Create a Data instance
                data = Data(name=username, email=email)
                data.save()

                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return render(request, 'home.html')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')






