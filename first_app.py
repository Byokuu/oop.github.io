from flask import Flask, render_template, request, send_from_directory
import json
import os

app = Flask(__name__)

folder = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(folder, "orders.json")

@app.route('/templates/<path:filename>')
def serve_template_css(filename):
    template_dir = os.path.join(app.root_path, 'templates')
    return send_from_directory(template_dir, filename)

def save_to_json(new_data):
    data = []
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
        except:
            data = []

    data.append(new_data)

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        new_consultation = {
            "client_name": request.form.get("Name"),
            "collection": request.form.get("HTML List Type Selector One"),
            "zip_code": request.form.get("Zip"),
            "color": request.form.get("color"),
            "time": request.form.get("time")
        }

        save_to_json(new_consultation)

        return render_template("print.html", new_order=new_consultation)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
