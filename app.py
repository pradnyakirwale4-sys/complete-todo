from flask import Flask , render_template, request
import json
app = Flask(__name__)
def read_todo():
  with open("db.json" , "r") as file:
    return json.load(file)
  
def create_todo(data):
  with open("db.json" , "w") as file:
    json.dump(data,file)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/todos" , methods=["GET"])
def get_all_todos():
  return read_todo()["notes"]

@app.route("/todos", methods=["POST"])
def create_new_todo():
  body = request.json
  all_notes = read_todo()

  id = len(all_notes["notes"]) + 1
  latest_note = {**body, "id":id}
  all_notes["notes"].append(latest_note)
  create_todo(all_notes)
  return{"message":"todo create success"}

@app.route("/todo/<int:tid>" , methods=["DELETE"])
def remove_todo(tid):
  #1 read todo
  all_notes = read_todo()

  #2 remove todo from notes
  result = []
  for item in all_notes["notes"]:
   if item["id"] != tid :
      result.append(item)
  all_notes["notes"] = result

  #3 write to db.json
  create_todo(all_notes)
  return {"messge":"todo remove success"}

if __name__ == "__main__":
 app.run(debug=True)