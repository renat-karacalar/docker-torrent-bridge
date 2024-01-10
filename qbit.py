from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pyotp
from datetime import timedelta
import qbittorrentapi
from typing import Optional, List
import re
import random
import os
from os import listdir
from os.path import join
import json

    

with open('/app/dockerbinding/credentials/credentials.json', 'r') as file:
    app_credentials = json.load(file)

with open('/app/dockerbinding/credentials/users_credentials.json', 'r') as file:
    users = json.load(file)
    
conn_info = app_credentials["connection_info"]

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=10)
app.secret_key = app_credentials["secret_key"]



def extract_magnet_strings(input_str: str) -> list:
    sanitized_str = input_str.strip()
    
    # Find all locations of 'magnet:' in the sanitized string
    locations = [match.start() for match in re.finditer(r'magnet:', sanitized_str)]
    extracted_strings = []
    
    # Construct and append the extracted strings to the list
    for i, location in enumerate(locations):
        if i == (len(locations) - 1):
            extracted_strings.append(sanitized_str[location:].strip())
        else:
            extracted_strings.append(sanitized_str[location:locations[i+1]].strip())
    
    return list(set(extracted_strings))


@app.route('/', methods=['GET', 'POST'])
def index():
    #test = ["dockerbinding/static/gifs_a/"+str(file) for file in [files[2] for files in os.walk("dockerbinding/static/gifs_a/")][0]]

    gif_folder_path = "static/gifs_a"
    gifs = [join(gif_folder_path, f) for f in listdir(gif_folder_path) if f.endswith(('.gif', '.png', '.jpg', '.jpeg'))]
    gif_url = random.choice(gifs)

    message = None
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        dropdown_value = request.form.get('dropdown')
        text_value = request.form.get('text_field')

        magnets = extract_magnet_strings(text_value)

        if magnets:
            # connect to qtb
            if dropdown_value == "option1":
                save_path = "/data/torrents/TVOD"
            elif dropdown_value == "option2":
                save_path = "/data/torrents/VOD"
            elif dropdown_value == "option3":
                save_path = "/data/torrents/RAW"
            qbt_client = qbittorrentapi.Client(**conn_info)
            try:
                qbt_client.auth_log_in()
                qbt_client.torrents_add(urls=magnets, save_path=save_path, is_paused=False)
                # if the Client will not be long-lived or many Clients may be created
                # in a relatively short amount of time, be sure to log out:
                qbt_client.auth_log_out()
                flash(f"Added {len(magnets)} magnet{'s' if len(magnets) > 1 else ''} to qBittorrent successfully!", 'success')
            except qbittorrentapi.LoginFailed as e:
                print(e)


    return render_template('index.html', gif=gif_url)

@app.route('/update_progress')
def update_progress():
    qbt_client = qbittorrentapi.Client(**conn_info)
    qbt_client.auth_log_in()
    downloading = []
    for element in qbt_client.torrents_info(status_filter="downloading"):
        downloading.append({"name":element.get('name'), "progress":element.get('progress')*100, "eta":element.get('eta')*100})
    # Fetch the progress from your governing Python script.
    # For demonstration purposes, I'll just simulate some progress.

    return jsonify(downloading)

@app.route('/loading', methods=['GET'])
def loading():
    gif_folder_path = "static/gifs_l/"
    gifs = [join(gif_folder_path, f) for f in listdir(gif_folder_path) if f.endswith(('.gif', '.png', '.jpg', '.jpeg'))]
    gif_url = random.choice(gifs)
    return render_template('loading.html', gif=gif_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("providing login")
    if request.method == 'POST':
        username = request.form.get('username')
        totp_code = request.form.get('totp_code')
        user = users.get(username)
        session['username'] = username
        if user:
            totp = pyotp.TOTP(user['secret_key'])
            if totp.verify(totp_code):
                session['logged_in'] = True
                return redirect(url_for('loading'))

    
    return render_template('login.html')


if __name__ == '__main__':
    # For running outside Docker (local development)
    #app.run(debug=True, port=5000, ssl_context=('cert.pem', 'key.pem'))
    
    # For running inside Docker
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=('/app/dockerbinding/ssl/cert.pem', '/app/dockerbinding/ssl/key.pem'))
