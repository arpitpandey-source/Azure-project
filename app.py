import os
from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Project Identity
USER_NAME = "Arpit Pandey"
USER_ID = "Arpit pandey-source"

# Azure Configuration - Replace with your actual experiment credentials
endpoint = "https://arpitocr.cognitiveservices.azure.com/" 
key = "YOUR_AZURE_LANGUAGE_KEY"

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment_result = None
    text_to_analyze = ""
    
    if request.method == 'POST':
        text_to_analyze = request.form.get('text_input')
        if text_to_analyze:
            client = authenticate_client()
            response = client.analyze_sentiment(documents=[text_to_analyze])[0]
            sentiment_result = response.sentiment

    return render_template('index.html', 
                           name=USER_NAME, 
                           user_id=USER_ID, 
                           result=sentiment_result,
                           input_text=text_to_analyze)

if __name__ == '__main__':
    app.run(debug=True)
