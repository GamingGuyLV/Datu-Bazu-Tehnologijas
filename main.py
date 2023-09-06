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

cur.execute('''
    CREATE TABLE IF NOT EXISTS genders (
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


# Add the genders to the table
try:
    cur.execute(f'''INSERT INTO genders (name) VALUES ("male")''')
    cur.execute(f'''INSERT INTO genders (name) VALUES ("female")''')
except sqlite3.IntegrityError as e:
    #print("Big yikes!")
    pass

con.commit()


# Read specific line from a file
def specific_line(stop: int, file: str):
    """
    Stop : Which line to read
    File : Which file to read from
    """


    openfile = open(file, "r")
    x = 0
    for line in openfile:
        x += 1
        line = line.strip()
        if x == stop:
            return str(line)


# Random user generator
def random_user_gen(amount: int):
    """
    Generates the chosen amount of random users and adds them to the database.
    """


    cur.execute('''SELECT COUNT(name) FROM professions''')
    professions = int(cur.fetchone()[0])
    print(f"Profession count: {professions}")


    cur.execute('''SELECT COUNT(name) FROM religions''')
    religions = int(cur.fetchone()[0])
    print(f"Religion count: {religions}")


    names = 0
    file = open("names.txt", "r")
    for line in file:
        names += 1
    print(f"Name count: {names}")

    for x in range(0, amount, 1):
        name = specific_line(random.randint(1, names), "names.txt")
        age = random.randint(1, 100)
        height = round(random.uniform(100, 200), 2)
        weight = round(random.uniform(30, 160), 2)
        gender = random.randint(1,2)
        religion = random.randint(1, religions)
        profession = random.randint(1, professions)
        annual_income = round(random.uniform(8000, 100000), 2)
        net_worth = round(random.uniform(5000, 1000000000), 2)

        cur.execute(f'''INSERT INTO people (name, age, height, weight, gender, religion, profession, annual_income, net_worth) VALUES (?,?,?,?,?,?,?,?,?)''', (str(name), int(age), float(height), float(weight), int(gender), int(religion), int(profession), float(annual_income), float(net_worth)))
        print(f"{x+1} - {name}, {age}, {height}, {weight}, {gender}, {religion}, {profession}, {annual_income}, {net_worth}")


    con.commit()


# Show random user
def random_user():
    cur.execute('''SELECT COUNT(id) FROM people''')
    users = int(cur.fetchone()[0])
    print(f"User count: {users}")

    randomUser = random.randint(1, users)

    cur.execute(f'''SELECT people.id, people.name, people.age, people.height, people.weight, genders.name, religions.name, professions.name, people.annual_income, people.net_worth FROM people LEFT JOIN genders ON people.gender = genders.id LEFT JOIN religions ON people.religion = religions.id LEFT JOIN professions ON people.profession = professions.id WHERE people.id={randomUser}''')
    user = cur.fetchone()
    return user


# Show all professions

# Show all religions

# Show all users with a certain criteria

# Drop all tables to start from scratch
def drop_tables():
    cur.execute('''DROP TABLE IF EXISTS people''')
    cur.execute('''DROP TABLE IF EXISTS professions''')
    cur.execute('''DROP TABLE IF EXISTS religions''')
    cur.execute('''DROP TABLE IF EXISTS genders''')
    cur.execute(f'''VACUUM''')
    con.commit()


while True:
    print("Choose an option:")
    print("1 - Generate random users")
    print("2 - Show random user")
    print("3 - Show all professions")
    print("4 - Show all religions")
    print("5 - Show all users with a certain criteria")
    print("8 - Exit")
    print("9 - Drop all tables and exit")

    option = input()

    try:
        option = int(option)
    except:
        pass

    match option:
        case 1:
            print("How many users to generate?")
            random_user_gen(int(input()))
            print("Done")
        
        case 2:
            print(random_user())
            input("Press enter to continue.")

        case 3:
            print("Case 3")
            continue

        case 4:
            print("Case 4")
            continue

        case 5:
            print("Case 5")
            continue

        case 8:
            con.commit()
            con.close()
            print("Goodbye!")
            break

        case 9:
            drop_tables()
            con.close()
            print("Tables dropped. Goodbye!")
            break

        case _:
            print("Not a valid choice!")
