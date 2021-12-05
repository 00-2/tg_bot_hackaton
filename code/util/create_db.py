import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tg_bot",
  password="gjikbgbnmgbdj",
  database="tg_bot"
)

mycursor = mydb.cursor()
# create table with user-data
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS users_data(
            users_data_id INT NOT NULL AUTO_INCREMENT,
            first_name varchar(20),
            last_name varchar(20),
            surname varchar(20),
            tg_client_id varchar(30) UNIQUE,
            PRIMARY KEY(users_data_id)
        );
    """)

# create table with level-of-user-data

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS users_level(
            users_level_id INT NOT NULL AUTO_INCREMENT,
            tg_client_id varchar(30),
            level_number INT,
            PRIMARY KEY(users_level_id),
            FOREIGN KEY (tg_client_id) REFERENCES users_data(tg_client_id)
        );
    """)

# create table of modules

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS module(
            module_id INT NOT NULL AUTO_INCREMENT,
            title varchar(100),
            data MEDIUMTEXT,            
            PRIMARY KEY(module_id)
        );
    """)
#create common table of questions
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS questions(
            questions_id INT NOT NULL AUTO_INCREMENT,
            module_id INT,
            task varchar(100),
            answers JSON,
            PRIMARY KEY(questions_id),
            FOREIGN KEY (module_id) REFERENCES module(module_id)   
        );
    """)

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS texts(
            texts_id INT NOT NULL AUTO_INCREMENT,
            module_id INT,
            data MEDIUMTEXT,
            PRIMARY KEY(texts_id),
            FOREIGN KEY (module_id) REFERENCES module(module_id)   
        );
    """)