## Overview

This is a database project that uses PostgreSQL and Python Flask to create a web application for managing a large dataset. The project involves loading the dataset into the database and launching a web interface to interact with it. Follow the steps below to set up and run the project.

## Getting Started

### Step 1: Initialize the database. This process may take a few minutes due to the large dataset.
python ./dbload.py

## step 2, launch the project
python app.py

## step 3, check the main page using the following link
http://127.0.0.1:5000

## Dependencies
Python>=3.7.9
Flask==1.1.2
psycopg2==2.7.7
Flask-WTF==0.14.3
WTForms==2.3.3
PostgreSQL>=12.1
tablefunc module installed for PostgreSQL to make pivot table.