
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat, UserProfile
from django.utils import timezone
from django.http import JsonResponse
import google.generativeai as genai
# Update the chatbot view to handle HTML responses
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from textblob import TextBlob
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from .forms import UserProfileForm
from django.contrib import messages
nltk.download('stopwords')
nltk.download('punkt')

import spacy
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from itertools import groupby
from django.utils.timezone import localtime

import joblib
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from .models import Chat
from django.utils import timezone
import random

def generate_fir_number():
    return f"DL{timezone.now().strftime('%Y%m%d')}{random.randint(1, 99):02d}"

def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')

        # Check if the message contains keywords related to filing a complaint
        if any(keyword in message.lower() for keyword in ['complaint', 'report', 'crime', 'hit', 'accident']):
            fir_number = generate_fir_number()
            response = f"""
            <h3>Hi Krishang! I am the Public Pulse Citizen Assistant.</h3>
            <p>Your complaint has been successfully lodged with the Delhi Police.</p>
            <p><strong>SHANTI SEWA NYAYA</strong></p>
            <p>Your FIR number is {fir_number}.</p>
            <p>This FIR has been registered regarding the incident you reported. The Delhi Police will investigate this matter and may contact you for further details. Please keep this FIR number for your records and future reference.</p>
            <p>If you have any additional information or questions about your case, don't hesitate to contact the local police station handling your complaint.</p>
            """
        else:
            # Use the existing ask_gemini function for other types of messages
            response = ask_gemini(message)

        # Save the chat to the database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': mark_safe(response)})

    return render(request, 'chatbot.html', {'chats': chats})

genai.configure(api_key='AIzaSyCYYO8mrdaJQl2thAoiqcRZZE-DVWVyiA0')
model = genai.GenerativeModel('gemini-pro')

def format_response(response):
    if "file a complaint" in response.lower() or "crime" in response.lower():
        return f"""
        <h3>Hi Shiva! I am the Public Pulse Citizen Assistant.</h3>
        <h4>Steps to File a Crime Complaint:</h4>
        <ol>
            <li><strong>Determine the Jurisdiction:</strong>
                <ul>
                    <li>Identify the location where the crime occurred.</li>
                    <li>Contact the local police department or sheriff's office in that jurisdiction.</li>
                </ul>
            </li>
            <li><strong>Contact the Police or Sheriff:</strong>
                <ul>
                    <li>Call the non-emergency line or visit the police station in person.</li>
                    <li>Explain the situation and request to file a crime report or complaint.</li>
                </ul>
            </li>
            <li><strong>Provide Details:</strong>
                <ul>
                    <li>Be clear and concise in describing the crime, including:</li>
                    <li>Date, time, and location</li>
                    <li>Type of crime committed</li>
                    <li>Description of any suspects or witnesses</li>
                    <li>Evidence or other relevant information</li>
                </ul>
            </li>
            <li><strong>Gather Documentation:</strong>
                <ul>
                    <li>Bring any evidence you have, such as:</li>
                    <li>Photos or videos</li>
                    <li>Receipts or invoices</li>
                    <li>Medical records</li>
                    <li>Witness statements</li>
                </ul>
            </li>
            <li><strong>Complete the Report:</strong>
                <ul>
                    <li>The police officer will take your statement and complete a formal crime report.</li>
                    <li>Read the report carefully and make sure all the information is accurate.</li>
                    <li>Sign and date the report.</li>
                </ul>
            </li>
            <li><strong>Follow Up:</strong>
                <ul>
                    <li>Once the report is filed, the police may contact you for additional information or to provide updates on the investigation.</li>
                    <li>Be patient as the investigation progresses.</li>
                </ul>
            </li>
        </ol>
        <h4>Additional Tips:</h4>
        <ul>
            <li>Stay calm and cooperative with the police.</li>
            <li>Provide as much detail as you can recall.</li>
            <li>Be honest even if the crime involves someone you know.</li>
            <li>Consider seeking legal advice if the crime is serious or involves substantial losses.</li>
            <li>Keep a copy of the crime report for your records.</li>
        </ul>
        <p><strong>Emergency Situations:</strong> In case of a life-threatening emergency or a crime in progress, call 911 immediately.</p>
        """
    return f"<p>Hi Shiva! I am the Public Pulse Citizen Assistant.</p><p>{response}</p>"

# Update the ask_gemini function to use the new format_response
def ask_gemini(message):
    try:
        response = model.generate_content(message)
        formatted_response = format_response(response.text.strip())
        return formatted_response
    except Exception as e:
        print(f"Error in ask_gemini: {e}")
        return format_response("I'm sorry, but I encountered an error while processing your request.")



def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message)
        category, sentiment = categorize_and_analyze_sentiment(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now(), category=category, sentiment_score=sentiment)
        chat.save()
        return JsonResponse({'message': message, 'response': mark_safe(response)})
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def sentiment_status(request):
    messages = Chat.objects.all()
    for message in messages:
        print(message.message, message.sentiment_status())

def analyze_keywords(messages):
    positive_keywords = []
    negative_keywords = []
    stop_words = set(stopwords.words('english'))
    messages = Chat.objects.all()

    for message in messages:
        analysis = TextBlob(message.message)
        keywords = [word for word in analysis.words.lower() if word not in stop_words]

        if analysis.sentiment.polarity > 0:
            positive_keywords.extend(keywords)
        elif analysis.sentiment.polarity < 0:
            negative_keywords.extend(keywords)
    positive_freq = Counter(positive_keywords)
    negative_freq = Counter(negative_keywords)
    top_positive = positive_freq.most_common(10)
    top_negative = negative_freq.most_common(10)
    return top_positive, top_negative

def matching_keywords(messages):
    # stemming
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(messages.lower())
    filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words and word.isalpha()]

    # lemmatization - bringing words to their dictionary form
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(messages.lower())
    lemmas = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

    return filtered_tokens, lemmas

def categorize_keywords(messages):
    categories = {
        'Transport': ['roads', 'road', 'potholes', 'pothole', 'accidents', 'accident'],
        'Health': ['hospital', 'hospitals', 'doctors', 'nurses'],
        'Education': ['schools', 'school', 'teacher', 'teachers', 'student', 'students', 'bursary', 'bursaries'],
    }
    for category, keywords in categories.items():
        if any(keyword in messages.lower() for keyword in keywords):
            return category
    return 'general'

def categorize_and_analyze_sentiment(messages):
    category = categorize_keywords(messages)
    sentiment = TextBlob(messages).sentiment.polarity

    return category, sentiment

def user_profile(request):
    form = UserProfileForm()
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been saved")
        else:
            form = UserProfileForm(instance=profile)
    return render(request, 'user/user_profile.html', {'form': form})

def chat_history(request):
    messages = Chat.objects.filter(user=request.user).order_by('created_at')
    grouped_messages = {}
    for message in messages:
        message_date = message.created_at.date()
        if message_date not in grouped_messages:
            grouped_messages[message_date] = [message]
        else:
            grouped_messages[message_date].append(message)

    return render(request, 'user/history.html', {'grouped_messages': grouped_messages})

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

def status_tracking(request):
    complaints = Chat.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/status_tracking.html', {'complaints': complaints})