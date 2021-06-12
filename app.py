from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def home():
    print(request.form)
    return render_template('index.html')
    print(request.form)
    user = request.form["user"]
    date = request.form["date"]
    file = request.form["files"]
    return redirect(url_for("result", type=user))

@app.route("/res/<type>/name", methods=["GET"])
def result(type):
    return render_template('result.html')

if __name__ == '__main__':
    app.run()