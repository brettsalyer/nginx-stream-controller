from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

@app.route("/index")
@app.route("/")
def index():
    import nginx_conf as nginx
    conf = nginx.NginxConf("./nginx.conf")
    res = conf.fetch_rtmp_conf()
    return render_template("index.html", result=res)

@app.route('/success/<results>')
def success(results):
   return 'results %s' % results

@app.route("/update", methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        for x, y in request.form.items():
            print("Received: ", x, y)

        return redirect(url_for('index'))

    else:
        print("Received GET")
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)