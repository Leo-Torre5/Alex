from django.apps import AppConfig
from flask import Flask, render_template, request, redirect, url_for
from django.views.decorators.csrf import csrf_protect
import os

from django.shortcuts import render

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search_query', '')
        print(f"Received query: '{query}'")
        if query:
            results = search_project(query)
            return render(request, 'search_results.html', {'results': results, 'query': query})
        else:
            return render(request, 'search_results.html', {'results': [], 'query': query})
    else:
        # Handle GET requests or other cases
        return render(request, 'index.html')


def search_project(query):
    # Set the path to your PyCharm project directory
    project_path = '/path/to/your/project'

    results = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_results = search_in_file(file_path, query)
                if file_results:
                    results.append({'file_path': file_path, 'matches': file_results})

    return results

def search_in_file(file_path, query):
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if query in line:
                    matches.append({'line_number': line_number, 'line_content': line.strip()})

    except (IOError, UnicodeDecodeError):
        pass

    return matches

@csrf_protect
def search(request):
    if request.method == 'POST':
        query = request.POST.get('search_query')
        # Add your search logic here (e.g., querying a database)
        # For simplicity, let's assume we have a list of results
        results = ['Result 1', 'Result 2', 'Result 3']
        return render(request, 'search_results.html', {'results': results})
    else:
        # Handle GET requests or other cases
        return render(request, 'index.html')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('search_query')
    # Add your search logic here (e.g., querying a database)
    # For simplicity, let's assume we have a list of results
    results = ['Result 1', 'Result 2', 'Result 3']
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)


class MelodymatrixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MelodyMatrix'
