import sqlite3
import os
import random

# Ensure Python always finds the database
DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

def get_meals_by_ingredient(ingredient):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM meals WHERE ingredients LIKE ?",
        ('%' + ingredient + '%',)
    )
    meals = cursor.fetchall()
    conn.close()
    return [m[0] for m in meals]

def weight_loss_meals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM meals WHERE calories < 450"
    )
    meals = cursor.fetchall()
    conn.close()
    return [m[0] for m in meals]

def budget_meals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM meals WHERE price < 120"
    )
    meals = cursor.fetchall()
    conn.close()
    return [m[0] for m in meals]

def random_response():
    responses = [
        "Hmm… let me think 🤔",
        "Okay I found something for you!",
        "Nice! Here are some ideas:",
        "You might enjoy these meals!"
    ]
    return random.choice(responses)