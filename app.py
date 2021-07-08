from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from backend import *
from datetime import date, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "ThisIsHokkyss"

@app.route("/", methods=["GET"])
def fill_input():
    session.clear()
    return render_template('index.html', step=1)

@app.route("/", methods=["POST"])
def fill():
    sender:str = request.form.get("sender")
    sent_on:str = request.form.get("sent_on")
    speed:float = request.form.get("speed")

    if sent_on == "":
        sent_on = str(date.today())
    
    session["sender"] = sender
    session["sent_on"] = sent_on
    session["speed"] = speed
    return redirect(url_for('second_step'))

@app.route("/input", methods=["GET"])
def second_step():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))

    return render_template('index.html', step=2)

@app.route("/input", methods=["POST"])
def second_step_validation():
    locations = request.form.get("locations")
    
    try:
        locations = Location.convert_to_list_from_string(locations)
    except:
        return jsonify(error="No locations provided")

    session["locations"] = locations
    return redirect(url_for('third_step'))

@app.route("/file", methods=["GET"])
def second_step_file():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))
    
    return render_template('index.html', step=3)

@app.route("/file", methods=["POST"])
def second_step_file_validation():
    files = request.files.getlist("file")

    session["locations"] = []

    for file in files:
        content = file.stream.read().decode("UTF8")
        content = from_JSON(content)
        for location in content:
            loc = Location.from_dict(location)
            session["locations"].append(loc)

    return redirect(url_for('third_step'))

@app.route("/final", methods=["GET"])
def third_step():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))
    
    filled = filled and not(session.get("locations") == None)
    if not(filled):
        return redirect(url_for('second_step'))
    
    return render_template('index.html', step=4, locations=session["locations"])

@app.route("/final", methods=["POST"])
def third_step_validation():
    start = request.form.get("start")
    session["start"] = start

    locations: list = session["locations"]
    N: int = len(locations)
    matrix: list = [[-1 for j in range(N)] for i in range(N)]
    city_list: list = [city["name"] for city in locations]

    for i in range(N):
        for j in range(N):
            if (i == j):
                matrix[i][j] = -1
            else:
                matrix[i][j] = Location.haversine(locations[i], locations[j])
    
    graph = Graph(first_city_name=start, adj_matrix=matrix, city_list=city_list)
    path, distance = graph.BranchAndBound()
    path.append(start)

    duration_in_seconds = 3600 * float(distance) / float(session.get("speed"))
    duration = timedelta(seconds=duration_in_seconds)
    duration = str(duration)
    # remove the miliseconds
    duration = duration[0 : len(duration) - 7 : 1]

    temp_result = {"duration": duration, "sender": session.get("sender"), "sent_on": session.get("sent_on"), "speed": session.get("speed"), "distance": distance, "path": [
        locations[city_list.index(city)] for city in path
    ]}

    push(sender=session.get("sender"), locations=session.get("locations"), result=temp_result, start=session.get("start"), speed=session.get("speed"), sent_on=session.get("sent_on"))

    if (session.get("start") == None):
        return redirect(url_for('third_step'))

    return redirect(url_for('result'))

@app.route("/path", methods=["GET", "POST"])
def result():
    if (request.method == "POST"):
        redirect(url_for("result"))

    if (request.form.get("sender") == None):
        sender = session.get("sender")
        sent_on = session.get("sent_on")
    else:
        session.clear()
        sender = request.form.get("sender")
        sent_on = request.form.get("sent_on")

    if(sender == None):
        return render_template('result.html', need_alert=False, locations=None, result=None)

    if(sent_on == None or sent_on == ""):
        sent_on = date.today()

    result = get_by_name_and_date(sender=sender, sent_on=sent_on)
    try:
        (_, sender, sent_on, locations, start, result, speed) = result
        locations = locations.decode("UTF8")
        locations = from_JSON(locations)
        result  = result.decode("UTF8")

        result = from_JSON(result)
        return render_template('result.html', need_alert=False, locations=locations, result=result)
    except:
        return render_template('result.html', need_alert=True, locations=None, result=None)

if __name__ == '__main__':
    app.run()