from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
from werkzeug.utils import secure_filename
import pymongo
from flask_pymongo import PyMongo
import subprocess
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/GamingSite"
mongo = PyMongo(app)

# app.config["IMAGE_UPLOADS"] = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Image"
# app.config["AUDIO_UPLOADS"] = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Audio"
# imagepath = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Image\swatishinde.jpg"
# audiopath = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Audio\Pitch.mp3"


app.config["IMAGE_UPLOADS"] = os.path.join('static',"Image")
app.config["AUDIO_UPLOADS"] = os.path.join('static',"Audio")
imagepath = "\static\Image\swatishinde.jpg"
audiopath = "\static\Audio\Pitch.mp3"

@app.route("/", methods=['GET', 'POST'])
def home():
    msg = " "
    if 'email' in session:
        msg = "you are already logged in with account:"+session['email']
        return render_template("upload.html")
    else:
        if request.method == "POST":
            email = request.form['usname']
            passd = request.form['upass']
            users = mongo.db.User
            loginuser = users.find_one({"email": email})

            if loginuser:
                gotpass = loginuser["password"]
                if passd == gotpass:
                    session['email'] = email
                    return render_template("upload.html", msg=session['email'])
                else:
                    msg = "Login Failed"
                    return render_template("login-register.html", msg=msg)
            else:
                msg = "userid or password is not correct"
                print(msg)
                return render_template("login-register.html", msg=msg)
            return render_template("login-register.html")
        cmd = f"python inference.py --checkpoint_path wav2lip_gan.pth  --face {imagepath} --audio {audiopath}"
        print(cmd)
        p = subprocess.Popen(cmd)
        p.terminate()
        out, err = p.communicate()
    return render_template("login-register.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        users = mongo.db.User
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        ucheck = users.find_one({'fname': fname, 'lname': lname})
        if ucheck is None:
            if pass1 != pass2:
                msg = "password does not match please enter valid password"
                return render_template("login-register.html", msg=msg)
            else:
                hashpass = pass1
                users.insert_one({'fname': fname, 'lname': lname,
                             'email': email, 'password': hashpass})
                return redirect('/')

    return render_template("login-register.html")


@app.route("/test", methods=['GET', 'POST'])
def tester():
    return render_template("translated-deepfake.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if 'email' in session:
        if request.method == "POST":
            if request.files:
                image = request.files["image"]
                audio = request.files["audio"]

                image.save(os.path.join(
                    app.config['IMAGE_UPLOADS'], image.filename))
                audio.save(os.path.join(
                    app.config['AUDIO_UPLOADS'], audio.filename))

                # imagepath = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Image\\" + \
                #     secure_filename(image.filename)
                # audiopath = "D:\DG_Work\Learning\Flask\WithMongo\Project\static\Audio\\" + \
                #     secure_filename(audio.filename)
                print("checkurl: ",os.path.join('static','Image'))
                imagepath = os.path.join('static','Image') +"\\"+ \
                    secure_filename(image.filename)
                audiopath = os.path.join('static','Audio') +"\\"+ \
                    secure_filename(audio.filename)
                print("imagpath: ",imagepath)
                print("Audipath: ",audiopath)
                cmd = f"python inference.py --checkpoint_path wav2lip_gan.pth  --face {imagepath} --audio {audiopath}"
                print(cmd)
                p = subprocess.Popen(cmd)
                out, err = p.communicate()
                return redirect("/showvid")
            else:
                return redirect('/upload')
        else:
            return redirect("/")
    return render_template('simple-deepfake.html')


@app.route("/showvid", methods=['GET', 'POST'])
def showvid():
    if 'email' in session:
        return render_template('showvideo.html')
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = "mysecret"
    app.run(debug=True)
