import subprocess
try:
    from quart import Quart, redirect, url_for, render_template, send_file
    import configparser
    from analytics import analytics as runanalytics
except:
    subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"])
    from quart import Quart, redirect, url_for, render_template
    import configparser
    from analytics import analytics as runanalytics

config = configparser.ConfigParser()
config.read('config.properties')

app = Quart('', template_folder='templates', static_folder='templates/static')

@app.route('/')
async def reroute():
    youtube = config.get("variables", "youtube")
    instagram = config.get("variables", "instagram")
    twitter = config.get("variables", "twitter")
    return await render_template("main.html", youtube=youtube, instagram=instagram, twitter=twitter)

@app.route('/yt')
async def ytreroute():
    return redirect(config.get("variables", "youtube"))

@app.route('/insta')
async def instareroute():
    return redirect(config.get("variables", "instagram"))

@app.route('/twitter')
async def twitterreroute():
    return redirect(config.get("variables", "twitter"))

@app.route('/x')
async def xreroute():
    return redirect(url_for("twitterreroute"))

@app.route("/image")
async def image():
    return await send_file("./icon.jpeg", mimetype='image/png')

@app.route("/analytics", methods=["POST"])
async def analytics():
    if config.get("config", "analytics") == "true":
        json = await request.get_json()
        await runanalytics(json, app)
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"failure"})

@app.route("/js/analytics")
async def jsanalytics():
    return await send_file("./templates/static/analytics.js", mimetype="text/javascript")

@app.errorhandler(404)
async def notfound(*_):
    return redirect(url_for("reroute"))