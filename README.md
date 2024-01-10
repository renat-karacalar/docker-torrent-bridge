qBittorrent Web Interface with Flask
Overview

This Flask-based web application provides a secure web interface for interacting with a local qBittorrent server. Users can add magnet URLs to initiate downloads, view torrent progress, and authenticate using TOTP (Time-Based One-Time Password) codes.
Features

    Secure Authentication: Utilizes TOTP codes for user authentication. (via pyotp, you will need to create a own secret, and add it to your authenticator)
    Magnet URL Handling: Parses magnet URLs from user inputs to add them to qBittorrent.
    Torrent Progress: Allows users to monitor the progress of downloading torrents.
    Random GIFs: Displays random GIFs from a specified directory as a visual element.

Setup & Installation

    Clone the repository.
    Install the required Python packages: pip install -r requirements.txt.
    Set up the qBittorrent credentials and user credentials in the credentials.json and users_credentials.json files respectively.
    Run the Flask application:
        For local development: python app.py
        For Docker: Build and run the Docker image with appropriate volume mappings and environment variables.

Usage

    Navigate to the application's URL in your web browser.
    Log in using your username and TOTP code.
    Add magnet URLs through the web interface.
    Monitor torrent progress on the main dashboard.
    Enjoy random GIFs while interacting with the application.

Technologies Used

    Flask
    pyotp
    qbittorrentapi
    Docker
