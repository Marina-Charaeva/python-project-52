from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Менеджер задач</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.2em;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Добро пожаловать!</h1>
            <p>Менеджер задач успешно развернут</p>
            <p style="font-size: 0.8em; margin-top: 30px;">Hexlet Code Project</p>
        </div>
    </body>
    </html>
    """)