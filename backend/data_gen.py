# backend/data_gen.py
import json, random, uuid
import os
areas = ["Connaught Place","Hauz Khas","Saket","Karol Bagh","Chanakyapuri","Lajpat Nagar","Greater Kailash","Rajouri Garden","Dwarka","Vasant Kunj","Noida Sector 18","Cyber City Gurgaon","MG Road Gurgaon","Punjabi Bagh","Khan Market"]
cuisines = ["Indian","Italian","Chinese","Continental","Mexican","Thai","Japanese","Cafe"]
ambiences = ["cozy","family","business","casual"]
def gen_tables(capacity):
    # simple heuristic: mix of 2/4/6/8 seat tables
    tables=[]
    remaining=capacity
    while remaining>0:
        t=random.choice([2,4,4,6])
        if t>remaining: t=remaining
        tables.append(t)
        remaining-=t
    return tables

restaurants=[]
for i in range(100):
    cap=random.choice([10,20,30,40,50,60,70,80,90,100])
    r={
        "id": f"R{1000+i}",
        "name": f"{random.choice(['Spice','Casa','Green','Blue','Pasta','Sakura','Mango','Olive'])} {random.choice(['House','Bistro','Kitchen','Garden','Corner','Palace'])}",
        "area": random.choice(areas),
        "cuisine": random.choice(cuisines),
        "capacity": cap,
        "tables": gen_tables(cap),
        "avg_spend": random.choice([300,400,500,800,1000,1500]),
        "rating": round(random.uniform(3.5,4.9),1),
        "ambience": random.choice(ambiences),
        "open_hours": {"mon":"11:00-23:00","tue":"11:00-23:00","wed":"11:00-23:00","thu":"11:00-23:00","fri":"11:00-00:00","sat":"11:00-00:00","sun":"11:00-23:00"}
    }
    restaurants.append(r)

os.makedirs("data", exist_ok=True)

with open("data/restaurants.json", "w") as f:
    json.dump(restaurants, f, indent=2)

print("Generated", len(restaurants))
