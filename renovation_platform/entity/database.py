# Creates the SQLite database and gives every entity class a connection 

import os
import sqlite3
from werkzeug.security import generate_password_hash 
# It is a python import statement that loads the function used to 
# securely scramble and hash user passwords before saving them in a database.


# A database file created in the main project folder
DB_NAME =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "platform.db")


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row 
    return connection

def create_tables():
    connection = get_connection()
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS user_profile(
            profileID   INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE NOT NULL,
            description TEXT,
            permissions TEXT,
            status      TEXT DEFAULT 'Active'
        );

        CREATE TABLE IF NOT EXISTS user_account (
            accountID   INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            profileID   INTEGER NOT NULL,
            status      TEXT DEFAULT 'Active'
        );

        CREATE TABLE IF NOT EXISTS company_profile(
            companyID     INTEGER PRIMARY KEY AUTOINCREMENT,
            designerID    INTEGER UNIQUE NOT NULL,
            name          TEXT NOT NULL,
            description   TEXT,
            contactNumber TEXT,
            contactEmail  TEXT,
            address       TEXT
        );

        CREATE TABLE IF NOT EXISTS category(
            categoryID    INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT UNIQUE NOT NULL,
            description   TEXT
        );

        CREATE TABLE IF NOT EXISTS project(
            projectID       INTEGER PRIMARY KEY AUTOINCREMENT,
            designerID      INTEGER NOT NULL,
            title           TEXT NOT NULL,
            description     TEXT NOT NULL,
            designs         TEXT,
            materials       TEXT,
            status          TEXT NOT NULL, -- "current" or "past"
            completionDate  TEXT,          -- "only for past projects"
            categoryID      INTEGER,
            viewCount       INTEGER DEFAULT 0,
            shortlistCount  INTEGER DEFAULT 0,
            createdDate     TEXT DEFAULT (date('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS shortlist(
            customerID INTEGER NOT NULL,
            projectID  INTEGER NOT NULL,
            PRIMARY KEY (customerID, projectID)
        );

        CREATE TABLE IF NOT EXISTS activity_log(
            logID          INTEGER PRIMARY KEY AUTOINCREMENT,
            projectID      INTEGER NOT NULL,
            action         TEXT NOT NULL,
            logDate        TEXT DEFAULT (date('now','localtime'))
        );
    """)

    connection.commit()
    connection.close()

