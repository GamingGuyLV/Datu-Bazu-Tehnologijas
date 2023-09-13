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
        education INT,
        profession INT,
        has_car INT,
        annual_income INT,
        net_worth INT
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

cur.execute('''
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR UNIQUE
    )
''')



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


# Add all education to the table
file = open("education.txt", "r")
for line in file:
    try:
        line = line.strip()
        #print(line)
        cur.execute(f'''INSERT INTO education (name) VALUES ("{str(line)}")''')
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
    #print(f"Profession count: {professions}")


    cur.execute('''SELECT COUNT(name) FROM religions''')
    religions = int(cur.fetchone()[0])
    #print(f"Religion count: {religions}")


    cur.execute('''SELECT COUNT(name) FROM education''')
    educations = int(cur.fetchone()[0])
    #print(f"Religion count: {educations}")


    names = 0
    file = open("names.txt", "r")
    for line in file:
        names += 1
    #print(f"Name count: {names}")

    for x in range(0, amount, 1):
        name = specific_line(random.randint(1, names), "names.txt")
        age = random.randint(1, 100)
        height = round(random.uniform(100, 200), 2)
        weight = round(random.uniform(30, 160), 2)
        gender = random.randint(1,2)
        religion = random.randint(1, religions)
        education = random.randint(1, educations)
        profession = random.randint(1, professions)
        has_car = random.randint(0,1)
        annual_income = random.randint(8000, 20000)
        net_worth = random.randint(50000, 1000000)

        cur.execute(f'''INSERT INTO people (name, age, height, weight, gender, religion, education, profession, has_car, annual_income, net_worth) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (str(name), int(age), float(height), float(weight), int(gender), int(religion), int(education), int(profession), int(has_car), int(annual_income), int(net_worth)))
        print(f"{x+1} - {name}, {age}, {height}, {weight}, {gender}, {religion}, {education}, {profession}, {has_car}, {annual_income}, {net_worth}")


    con.commit()


# Show random user
def random_user():
    """
    Returns a random user from the database.
    """

    cur.execute('''SELECT COUNT(id) FROM people''')
    users = int(cur.fetchone()[0])
    print(f"User count: {users}")

    randomUser = random.randint(1, users)

    cur.execute(f'''SELECT people.id, people.name, people.age, people.height, people.weight, genders.name, religions.name, education.name, professions.name, people.has_car, people.annual_income, people.net_worth FROM people LEFT JOIN genders ON people.gender = genders.id LEFT JOIN religions ON people.religion = religions.id LEFT JOIN professions ON people.profession = professions.id LEFT JOIN education ON people.education = education.id WHERE people.id={randomUser}''')
    user = cur.fetchone()

    display = {}
    display["id"] = int(user[0])
    display["name"] = str(user[1])
    display["age"] = int(user[2])
    display["height"] = float(user[3])
    display["weight"] = float(user[4])
    display["gender"] = str(user[5])
    display["religion"] = str(user[6])
    display["education"] = str(user[7])
    display["profession"] = str(user[8])
    display["has a car"] = bool(int(user[9]))
    display["annual income"] = int(user[10])
    display["net worth"] = int(user[11])

    return display


# Show all users with a certain criteria
def get_users(criteria: str):
    """
    Returns a list of all users with the cerain criteria. ONLY ONE CRITERIA
    """

    criterias = False

    if "," in criteria:
        criterias = criteria.split(",")

    
    finalcriteria = ""

    if criterias:
        for criteria in criterias:
            criteria = criteria.strip()
            if "id" in criteria:
                criteria = "people." + criteria
            elif "name" in criteria:
                criteria = "people." + criteria
            elif "age" in criteria:
                criteria = "people." + criteria
            elif "height" in criteria:
                criteria = "people." + criteria
            elif "weight" in criteria:
                criteria = "people." + criteria
            elif "gender" in criteria:
                criteria = "genders.name" + criteria[6:]
            elif "religion" in criteria:
                criteria = "religions.name" + criteria[8:]
            elif "education" in criteria:
                criteria = "education.name" + criteria[8:]
            elif "profession" in criteria:
                criteria = "professions.name" + criteria[10:]
            elif "has_car" in criteria:
                criteria = "people." + criteria
            elif "annual_income" in criteria:
                criteria = "people." + criteria
            elif "net_worth" in criteria:
                criteria = "people." + criteria
            
            finalcriteria = f"{finalcriteria} AND {criteria}"
        finalcriteria = finalcriteria[4:]
    
    else:
        criteria = criteria.strip()
        if "id" in criteria:
            criteria = "people." + criteria
        elif "name" in criteria:
            criteria = "people." + criteria
        elif "age" in criteria:
            criteria = "people." + criteria
        elif "height" in criteria:
            criteria = "people." + criteria
        elif "weight" in criteria:
            criteria = "people." + criteria
        elif "gender" in criteria:
            criteria = "genders.name" + criteria[6:]
        elif "religion" in criteria:
            criteria = "religions.name" + criteria[8:]
        elif "education" in criteria:
            criteria = "education.name" + criteria[8:]
        elif "profession" in criteria:
            criteria = "professions.name" + criteria[10:]
        elif "has_car" in criteria:
            criteria = "people." + criteria
        elif "annual_income" in criteria:
            criteria = "people." + criteria
        elif "net_worth" in criteria:
            criteria = "people." + criteria
        
        finalcriteria = criteria
                

    #print(f"Criteria: {finalcriteria}")

    try:
        cur.execute(f'''SELECT people.id, people.name, people.age, people.height, people.weight, genders.name, religions.name, education.name, professions.name, people.has_car, people.annual_income, people.net_worth FROM people LEFT JOIN genders ON people.gender = genders.id LEFT JOIN religions ON people.religion = religions.id LEFT JOIN professions ON people.profession = professions.id LEFT JOIN education ON people.education = education.id WHERE {finalcriteria} ORDER BY RANDOM()''')
        users = cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"\n{e}")
        print("\nError ^^^ Returning nothing")
        users = []
    
    users_dict = []

    for user in users:
        #print(user)
        display = {}
        display["id"] = int(user[0])
        display["name"] = str(user[1])
        display["age"] = int(user[2])
        display["height"] = float(user[3])
        display["weight"] = float(user[4])
        display["gender"] = str(user[5])
        display["religion"] = str(user[6])
        display["education"] = str(user[7])
        display["profession"] = str(user[8])
        display["has a car"] = bool(int(user[9]))
        display["annual income"] = int(user[10])
        display["net worth"] = int(user[11])

        users_dict.append(display)

    return users_dict


# Delete a specific user
def delete_user(id: int):

    cur.execute(f'''SELECT * FROM people WHERE id={id}''')
    fetched = cur.fetchone()

    if fetched:
        cur.execute(f'''DELETE FROM people WHERE id={id}''')
        con.commit()
        print("Done")
        return
    
    else:
        print("User with that id does not exist.")
        return


# Delete all users with a certain criteria
def delete_users(criteria: str):
    criterias = False

    if "," in criteria:
        criterias = criteria.split(",")

    
    finalcriteria = ""

    if criterias:
        for criteria in criterias:
            criteria = criteria.strip()
            
            finalcriteria = f"{finalcriteria} AND {criteria}"
        finalcriteria = finalcriteria[4:]
    
    else:
        criteria = criteria.strip()
        
        finalcriteria = criteria
                

    #print(f"Criteria: {finalcriteria}")

  
    try:
        cur.execute(f'''DELETE FROM people WHERE {finalcriteria}''')
        con.commit()
    except sqlite3.OperationalError as e:
        print(f"\n{e}")
        print("\nError ^^^ Returning nothing")


# Drop all tables to start from scratch
def drop_tables():
    cur.execute('''DROP TABLE IF EXISTS people''')
    cur.execute('''DROP TABLE IF EXISTS professions''')
    cur.execute('''DROP TABLE IF EXISTS religions''')
    cur.execute('''DROP TABLE IF EXISTS genders''')
    cur.execute('''DROP TABLE IF EXISTS education''')
    cur.execute('''DROP TABLE IF EXISTS hobbies''')
    cur.execute(f'''VACUUM''')
    con.commit()


while True:
    print("Choose an option:")
    print("1 - Generate random users")
    print("2 - Insert a user")
    print("3 - Show random user")
    print("4 - Show all users with a certain criteria")
    print("5 - Delete a user (id)")
    print("6 - Delete all users with a certain criteria")
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
            name = str(input("\nInput a name. (string)\n"))
            age = int(input("\nInput age. (integer)\n"))
            height = float(input("\nInput height. (float)\n"))
            weight = float(input("\nInput weight. (float)\n"))
            gender = int(input("\nInput gender. (int: 1 - male, 2 - float)\n"))
            religion = int(input("\nInput religion. (int)\n"))
            education = int(input("\nInput education. (int)\n"))
            profession = int(input("\nInput profession. (int)\n"))
            has_car = int(input("\nInput if has a car. (int: 0 - No, 1 - Yes)\n"))
            annual_income = int(input("\nInput annual income. (int)\n"))
            net_worth = int(input("\nInput net worth. (int)\n"))

            cur.execute(f'''INSERT INTO people (name, age, height, weight, gender, religion, education, profession, has_car, annual_income, net_worth) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (str(name), int(age), float(height), float(weight), int(gender), int(religion), int(education), int(profession), int(has_car), int(annual_income), int(net_worth)))
            con.commit()
            print("Done\n")

        case 3:
            print(random_user())
            input("Press enter to continue.")

        case 4:
            print("\nExample: gender='male' OR id=1132 . If you want multiple, then add , between them. Word values need to be in quotes, numbers without.")
            criteria = input()

            users = get_users(criteria)

            for user in users:
                print(user)

            input("Press enter to continue.")

        case 5:
            id = int(input("Input the id. (int)"))
            delete_user(id)
            input("Press enter to continue.")

        case 6:
            print("\nExample: gender=1 OR id=1132 . If you want multiple, then add , between them. Only the ID of said criteria works.")
            criteria = input()

            delete_users(criteria)

            input("Press enter to continue.")


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
