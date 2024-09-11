import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from analysis import *
from dotenv import load_dotenv
import os

# Loading env to keep privite API
load_dotenv()

# Weather API from (https://openweathermap.org/api)
OMW_ENDPOINT = os.getenv('OMW_ENDPOINT')
API_KEY = os.getenv('API_KEY')
weather_params = {
    'lat':  54.51,  # Latitude
    'lon': 18.53,  # Longitude
    'cnt': 1,
    'appid': API_KEY,
}

data = requests.get(OMW_ENDPOINT, params=weather_params)
data = data.json()

# Nesting
temp_data = data['list'][0]['main']['temp']
cel_temp = temp_data - 273.15
cel_temp = round(cel_temp)
pressure_data = data['list'][0]['main']['pressure']
humidity_data = data['list'][0]['main']['humidity']
wind = data['list'][0]['wind']['speed']

# While loop
will_rain = False
for hour_data in data['list']:
    condition_code = hour_data['weather'][0]['id']
    if 200 < int(condition_code) <= 700:
        will_rain = True
        break

if will_rain:
    print(
        f'Take an umbrella, it will rain today. The temperature is around {cel_temp}°C. The wind is {wind} meters per second. Humidity is {humidity_data}%, and the pressure is {pressure_data} hPa.')
else:
    print(
        f'Today is sunny, the temperature is around {cel_temp}°C. The wind is {wind} meters per second. Humidity is {humidity_data}%, and the pressure is {pressure_data} hPa.')


# Mailing
mail = 'YOUR_EMAIL'
password = 'YOUR_PASSWORD'
recipients = ['RECIPIENT MAILS']
subject = 'Weather forecast'
smtp_server = 'smtp.PLATFORM.COM'
smtp_port = 587

# Create the email message
msg = MIMEMultipart()
msg['From'] = mail
msg['To'] = ', '.join(recipients)
msg['Subject'] = subject

# Email body
if will_rain:
    body = f'Take an umbrella, it will rain today. The temperature is around {cel_temp}°C. The wind is {wind} meters per second. Humidity is {humidity_data}%, and the pressure is {pressure_data} hPa.'
else:
    body = f'Today is sunny, the temperature is around {cel_temp}°C. The wind is {wind} meters per second. Humidity is {humidity_data}%, and the pressure is {pressure_data} hPa.'
msg.attach(MIMEText(body, 'plain'))

# List of image filenames, transfer from other file called analysis.py
filenames = ['temperature.png', 'humidity.png', 'windspeed.png']
paths = [os.path.join(os.getcwd(), filename) for filename in filenames]

# Attach each image file
for attachment_path in paths:
    if os.path.isfile(attachment_path):
        try:
            print(f"Attaching {attachment_path}")
            with open(attachment_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(
                    img_data, name=os.path.basename(attachment_path))
                msg.attach(image)
        except Exception as e:
            print(f"Error processing file {attachment_path}: {e}")
    else:
        print(f"File not found: {attachment_path}")
# Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(user=mail, password=password)
        connection.sendmail(
            from_addr=mail,
            to_addrs=recipients,
            msg=msg.as_string()
        )
    print('Email with images was sent successfully!')