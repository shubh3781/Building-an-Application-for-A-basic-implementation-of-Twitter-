# Flask-based Social Media Web Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

This project is a Flask-based web application designed to simulate a simple social media platform. Users can sign in, create and update profiles, post tweets, follow/unfollow other users, and search for users or tweets. The backend integrates with Google Cloud services for authentication and data storage, utilizing Google Cloud Datastore and Google Cloud Storage.

## Features

- **User Authentication**: Users can sign in and their session is managed using Google Cloud's authentication services.
- **User Profile Management**: Users can create profiles, edit profile details, and view other users' profiles.
- **Post Tweets**: Users can create, update, and delete tweets. Tweets may contain text and optional media.
- **Follow/Unfollow Functionality**: Users can follow or unfollow other users, with real-time updates on follower counts.
- **Search**: Users can search for tweets or other users using a search filter.
- **Google Cloud Integration**: User data and media files are stored in Google Cloud Datastore and Google Cloud Storage respectively.

## Requirements

- Python 3.x
- Flask
- Google Cloud SDK
- Google Cloud Datastore
- Google Cloud Storage
- Werkzeug

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/social-media-flask-app.git
   cd social-media-flask-app
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Google Cloud**

   - Ensure that you have Google Cloud SDK installed and authenticated.
   - Create a Google Cloud project and enable Datastore and Storage APIs.
   - Add your project configuration to `constants.py` for project-specific settings like `PROJECT_NAME` and `PROJECT_STORAGE_BUCKET`.

6. **Run the Flask Application**

   ```bash
   python app.py
   ```

## Usage

1. **Sign In**: Users are redirected to the sign-in page where they authenticate using Google Cloud's OAuth.
2. **Create a Tweet**: After signing in, users can create tweets that may include text and images.
3. **Follow Users**: Users can follow/unfollow others and see tweets from those they follow in their timeline.
4. **Edit Profile**: Users can update their personal information such as name and profile picture.
5. **Search**: Users can search for tweets or other users using the search bar.
6. **View Timeline**: The timeline displays tweets from the users one follows, providing a real-time feed.

## API Endpoints

- **`GET /signin`**: Render the sign-in page.
- **`GET /timeline`**: Displays the user's timeline with tweets from followed users.
- **`GET /profile`**: Displays the user's profile.
- **`POST /addfollower`**: Adds a follower for a specific user.
- **`POST /removefollower`**: Removes a follower from a user's list.
- **`POST /addtweet`**: Adds a tweet to the user’s timeline.
- **`POST /updatetweet`**: Updates an existing tweet.
- **`POST /deletetweet`**: Deletes a tweet.
- **`GET/POST /search`**: Allows users to search for tweets or other users.

## Error Handling

- **Authentication Errors**: Handled gracefully if the user is not authenticated or if the Google Cloud service returns an error.
- **File Upload Errors**: Errors in file uploads such as invalid file types or exceeding size limits are handled with appropriate messages.
- **Data Validation**: Proper validation for input fields like username, email, etc., is in place to prevent invalid data submissions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Google Cloud](https://cloud.google.com/) for storage and authentication services.
- [Werkzeug](https://werkzeug.palletsprojects.com/) for file handling utilities.
