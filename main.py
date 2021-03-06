from flask import Flask, redirect, url_for, request, render_template
import nginx_conf as nginx

app = Flask(__name__)
conf = nginx.NginxConf("./nginx.conf")

@app.route("/index")
@app.route("/")
def index():  
    res = conf.fetch_rtmp_conf()
    return render_template("index.html", result=res)

@app.route('/success/<results>')
def success(results):
   return 'results %s' % results

@app.route("/update", methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        if 'update' in request.form:
            for x, y in request.form.items():
                print("Received: ", x, y)
            conf.update_rtmp_conf(request.form)
        else:
            print("[INFO] Restarting the RTMP Nginx Server...")

        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
