Running the Tornado URLWordCloud example app
====================================
This demo is a simple app displays WordCloud using most common 100 words fetched at a given URL. The app uses SQLite to store salt-hashed and encrypted words and their frequencies. 

If you have `docker` and `docker-compose` installed, you can use "docker build -t octopus_app ." to install the preqrequites and "docker-compose up" to run the app.

The app has two pages:
"/" - index.html that generates the Word Cloud
"/admin" - admin.html that shows stored word-frequency pairs