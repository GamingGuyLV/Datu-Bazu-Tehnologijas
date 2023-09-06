import sqlite3
import random

con = sqlite3.connect("main.db")
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR,
        age INT,
        height REAL,
        weight REAL,
        gender INT,
        religion INT,
        profession INT,
        annual_income REAL,
        net_worth REAL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS professions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR UNIQUE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS religions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR UNIQUE
    )
''')

# Genders = 1 Male, 2 Female


# Add all professions to the table
file = open("professions.txt", "r")
for line in file:
    try:
        line = line.strip()
        #print(line)
        cur.execute(f'''INSERT INTO professions (name) VALUES ("{str(line)}")''')
    except sqlite3.IntegrityError as e:
        #print("Big yikes!")
        continue


# Add all religions to the table
file = open("religions.txt", "r")
for line in file:
    try:
        line = line.strip()
        #print(line)
        cur.execute(f'''INSERT INTO religions (name) VALUES ("{str(line)}")''')
    except sqlite3.IntegrityError as e:
        #print("Big yikes!")
        continue


# Read specific line from a file
def specific_line(line: int, file: str):
    """
    Line : Which line to read
    File : Which file to read from
    """


    file = open(file, "r")
    x = 0
    for line in file:
        x += 1
        if x == line:
            return str(line)       
        
        else:
            continue


# Random user generator
def random_user_gen(amount: int):
    """
    Generates the chosen amount of random users and adds them to the database.
    """


    cur.execute('''SELECT COUNT(name) FROM professions''')
    professions = int(cur.fetchone())
    print(f"Profession count: {professions}")


    cur.execute('''SELECT COUNT(name) FROM religions''')
    religions = int(cur.fetchone())
    print(f"Profession count: {religions}")


    names = 0
    file = open("names.txt", "r")
    for line in file:
        names += 1


    for x in range(0, amount, 1):
        name = specific_line(random.randint(1, names))
        age = random.randint(1, 100)
        height = random.randrange(100, 200, 0.01)
        weight = random.randrange(30, 160, 0.01)
        gender = random.randint(1,2)
        religion = random.randint(1, religions)
        profession = random.randint(1, professions)
        annual_income = random.randrange(8000, 100000, 1)
        net_worth = random.randrange(5000, 1000000000, 1)

        cur.execute(f'''INSERT INTO people (name, age, height, weight, gender, religion, profession, annual_income, net_worth) VALUES (?,?,?,?,?,?,?,?,?)''', (str(name), int(age), float(height), float(weight), int(gender), int(religion), int(profession), float(annual_income), float(net_worth)))


    con.commit()


while True:
    print("Choose an option:")
    print("1 - Generate random users")
    print("2 - Show random user")
    print("")