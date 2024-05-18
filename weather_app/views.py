import json
from django.shortcuts import render
from django.http import JsonResponse
import requests
import datetime
import os
import google.generativeai as genai
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

genai.configure(api_key=env('AI_KEY'))
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def index(request):
    weather_api_key = os.environ.get('WEATHER_KEY')
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1','')
        
        weather_data1 = fetch_weather_and_forecast(city1, weather_api_key, current_weather_url)
       
        context = {
            'weather_data1': weather_data1 
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 1),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    return weather_data


def get_ai_response(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        weather_data = data.get('weather_data')
        prompt = f"Using this weather data:{weather_data} answer the following prompt (please note temperature is in celcius):"+data.get('prompt')
        
        # Generate the AI response using your chosen method (e.g., OpenAI API, rule-based system, etc.)
        # Example using a rule-based system:
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        response= (convo.last.text)
        response = format_response(response)
        return JsonResponse({'response': response})
    
    return JsonResponse({'error': 'Invalid request method'})

def format_response(response):
    formatted_response = response.replace(" **", "<strong>").replace("**", "</strong>")
    formatted_response = formatted_response.replace("*", "<br><br>")
    return formatted_response
