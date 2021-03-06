from flask import Flask, request, abort, redirect
import ML.interface as ML
from flask_cors import CORS

########################################################################################
# App Setup
########################################################################################
app = Flask("Opticus")
app.secret_key = "Not really very secret"
CORS(app)


########################################################################################
# Flask Routing
########################################################################################

#Overview page
@app.route("/", methods=["GET"])
def overview():
    return app.send_static_file("index.html")

#Redirect some static file paths
@app.route("/opticus-ui/static/<path:path>", methods=["GET"])
def getUIStatic(path):
    return app.send_static_file(path)

#If reloaded while at /measure
@app.route("/measure", methods=["GET"])
def measureGet():
    return redirect("/")

#Image post API endpoint
@app.route("/measure", methods=["POST"])
def measurePost():
    if "file" in request.files:
        f = request.files["file"]

        #Some file checking
        if f and (not f.filename == ""):
            if ("." in f.filename) and (f.filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}):
                measurements = ML.getFaceMeasurements(f)
                return {"success": True, "measurements": measurements}

    abort(400)


########################################################################################
# Start Flask App
########################################################################################
if __name__ == "__main__":
    app.run(ssl_context="adhoc", host="localhost", port=5000, debug=True)
