def login_controller(username: str, password: str):
    
    # Simulation base de données
    if username == "ceo" and password == "123":
        return {"role": "ceo"}

    elif username == "sales" and password == "123":
        return {"role": "sales_manager"}

    elif username == "inventory" and password == "123":
        return {"role": "inventory_manager"}

    else:
        return {"error": "Invalid credentials"}