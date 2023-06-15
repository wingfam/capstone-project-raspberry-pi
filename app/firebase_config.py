# Import Firebase REST API library
import firebase

# Firebase configuration
config = {
    "apiKey": "AIzaSyAPTtDwvK8tZ8H1pwUsQkVOWqxwWYsK35k",
    "authDomain": "slsd-capstone-project.firebaseapp.com",
    "databaseURL": "https://slsd-capstone-project-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "slsd-capstone-project",
    "storageBucket": "slsd-capstone-project.appspot.com",
    "messagingSenderId": "523851281455",
    "appId": "1:523851281455:web:e865c67e7c8bf8133f82da",
}

# Instantiates a Firebase app
firebaseApp = firebase.initialize_app(config)

# Firebase Realtime Database
firebaseDB = firebaseApp.database()

# Identification
identity = {
    "email": "supmangcua970@gmail.com",
    "password": "123456789"
}