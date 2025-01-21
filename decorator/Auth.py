
CACHE=[]
user_list = {
    "teacher": "qwer1234",
    "admin": "admin"
}

def user_auth():
    global CACHE
    if len(CACHE) == 0:
        print(f"To use this command you must be authenticated")
    while (len(CACHE)==0):
        try:
            username = input("Username: ")
            password = input("Password: ")
            if user_list[username]==password:
                CACHE.append(username)
        except Exception:
            print(f"Wrong username or password")

