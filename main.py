#!/usr/bin/python3

import requests, uuid, json
from datetime import date, timedelta

# gets next 5 days
def getFriday():
    friday = date.today() + timedelta(days=5)
    return friday

# canvas
canvas_key = "Bearer TOKEN"

# retrieves courses
courses = requests.get(
    "https://kls.instructure.com/api/v1/users/self/favorites/courses",
    headers = {
        "Authorization": canvas_key
    }
).json()

# retrieves tasks in courses
tasks = {}

for i in courses:
    tasks[i["course_code"]] = (requests.get(
        f"https://kls.instructure.com/api/v1/calendar_events?type=assignment&end_date={getFriday()}&context_codes[]=course_{i['id']}&per_page=200", # weekly
        headers = {
            "Authorization": canvas_key
        }
    ).json())

# todoist
todoist_key = "Bearer TOKEN"

# returns todoist projects
todoist = requests.get(
    "https://api.todoist.com/rest/v1/projects", 
    headers = {
        "Authorization": todoist_key
    }
).json()

# JSON stuff
f = open('data.json')
data = json.load(f)
  
with open('tasks.json') as g:
    names = json.load(g)

# output counter
counter = 0

# adds tasks
for i in tasks:
    if i in data:
        for j in tasks[i]:
            if j["title"] not in names:
                counter += 1
                requests.post(
                            "https://api.todoist.com/rest/v1/tasks",
                            data=json.dumps({
                                "project_id": data[i]["project_id"],
                                "section_id": data[i]["section_id"],
                                "content": j["title"],
                                "due_date": j["assignment"]["due_at"],
                            }),
                            headers={
                                "Content-Type": "application/json",
                                "X-Request-Id": str(uuid.uuid4()),
                                "Authorization": todoist_key
                            }).json()
                names.append(j["title"])
                with open('tasks.json', 'w') as g:
                    json.dump(names, g, ensure_ascii=False)               

if counter > 0:
    print(f"{counter} tasks added on {date.today()}")

f.close()