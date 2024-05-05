#from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
import json
from pytube import Youtube
import assemblyai as ai
import openai

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        #get title
        title = yt_link(yt_link)


        #get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "failed to get transcript"}, status=500)

        
        #use open ai to generate blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': 'Invalid request method'}, status=500)

        #save blog article to database
        #return blog article as a response
        

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    def yt_link(link):
        yt = Youtube(link)
        title = yt.title
        return title
    
    def download_audio(link):
        yt = Youtube(link)
        video = yt.streams.filter(only_audio=True).first()
        out_fle = video.download(output_path=setting.MEDIA_ROOT)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    def get_transcription(link):
        audio_file = download_audio(link)
        aai.setting.api_key = "935b4aaf3cca4728b00efebc3f5b7a0d"

        transcriber = aai.Transcriber()
        transcriber = transcriber.transcribe(audio_file)
        return transcriber.text
    
    def generate_blog_from_transcription(transcription):
        

        prompt = f"Based on the following transcript from a Youtube video, write a comprehensive blog article, write it based on the transcript,but do not make it look like a youtube video, maike it look like a proper blog article:\n\n{transcription}\n\nArticle:"
        response = openai.completions.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )

        generate_content = response.choices[0].text.strip()
        return generated_content

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message - "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
            return render(request, 'login.html')


    return render(request, 'login.html')
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        retypePassword = request.POST['retypePassword']
        if password == retypePassword:
            try:
                user = user.object.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'error creating account'
                return render(request, 'signup.html', {'error_message'})
                
        else:
            error_message = 'password donot match'
    return render(request, 'signup.html', {'error_message'})
    
def user_logout(request):
    logout(request)
    return redirect('/')