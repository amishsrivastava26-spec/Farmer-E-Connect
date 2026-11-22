import database 

def register_farmer(name, mobile, village, village_pin, crop, password_hash=None):
    return database.add_farmer(name, mobile, village, village_pin, crop, password_hash)

def get_farmer_details(farmer_Id):
    database.get_details_by_id(farmer_Id)

def update_farmer_mobile(Farmer_Id, new_mobile):
    database.update_farmer_mobile(Farmer_Id, new_mobile)

def update_farmer_crop(Farmer_Id, new_crop):
    database.update_farmer_crop(Farmer_Id, new_crop)

def update_farmer_village(Farmer_Id, new_village):
    database.update_farmer_village(Farmer_Id, new_village)

def update_farmer_village_pin(Farmer_Id, new_village_pin):
    database.update_farmer_village_pin(Farmer_Id, new_village_pin)

def add_procurement(Farmer_id, Name, Procurement_token,Procurement_date, Quantity, Crop):
    database.add_procurement(Farmer_id, Name, Procurement_token,Procurement_date, Quantity, Crop)

def login_check(mobile):
    return database.login_check(mobile)

def activate_farmer(mobile, password_hash):
    return database.set_farmer_password(mobile, password_hash)

if __name__ == "__main__":
    debug=True
    
    
