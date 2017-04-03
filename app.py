from flask import *
import os
from werkzeug.utils import *
from model.treeItem import TreeList
import mlab
from flask_login import  *
from model.useItem import User
from sessionuser import Sessionuser
app = Flask(__name__)

tree_list = [
    {"image_link":"https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17126240_605511066305000_7056512309618802688_n.jpg",
     "topic":"Tree Ngo Ngo",
     "text":"Chậu cây ngộ ngộ xinh xinh thế này mà đi tặng chị yêu cô giáo yêu thì thật là vui quá đi mất. Những điều ngọt ngào không cần đến từ những gì quá to tát hay lớn lao cả mà chỉ đơn giản ngộ nghĩnh như vậy thôi cũng đủ ấm lòng rất nhiều rồi"},
    {"image_link":"https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17126240_605511066305000_7056512309618802688_n.jpg",
     "topic":"Tree Ngo Ngo",
     "text":"Chậu cây ngộ ngộ xinh xinh thế này mà đi tặng chị yêu cô giáo yêu thì thật là vui quá đi mất. Những điều ngọt ngào không cần đến từ những gì quá to tát hay lớn lao cả mà chỉ đơn giản ngộ nghĩnh như vậy thôi cũng đủ ấm lòng rất nhiều rồi"},
    {"image_link": "https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17126240_605511066305000_7056512309618802688_n.jpg",
     "topic": "Tree Ngo Ngo",
     "text": "Chậu cây ngộ ngộ xinh xinh thế này mà đi tặng chị yêu cô giáo yêu thì thật là vui quá đi mất. Những điều ngọt ngào không cần đến từ những gì quá to tát hay lớn lao cả mà chỉ đơn giản ngộ nghĩnh như vậy thôi cũng đủ ấm lòng rất nhiều rồi"},
    {"image_link":"https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17077633_140162856505582_6864397593540034560_n.jpg",
     "topic":"Tree Ngo Nghe",
     "text":"Góc vườn nho nhỏ của bọ"},
    {"image_link": "https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17077633_140162856505582_6864397593540034560_n.jpg",
     "topic": "Tree Ngo Nghe",
     "text": "Góc vườn nho nhỏ của bọ"},
    {"image_link":"https://instagram.fhan2-2.fna.fbcdn.net/t51.2885-15/e35/17077633_140162856505582_6864397593540034560_n.jpg",
     "topic":"Tree Ngo Nghe",
     "text":"Góc vườn nho nhỏ của bọ"},
    {"image_link":"https://instagram.fhan2-1.fna.fbcdn.net/t51.2885-15/e35/17333025_418681021817660_1111101743053144064_n.jpg",
     "topic":"Tree inspire",
     "text":"Small beautiful conner"},
    {"image_link":"https://instagram.fhan2-1.fna.fbcdn.net/t51.2885-15/e35/17333025_418681021817660_1111101743053144064_n.jpg",
     "topic":"Tree inspire",
     "text":"Small beautiful conner"},
    {"image_link":"https://instagram.fhan2-1.fna.fbcdn.net/t51.2885-15/e35/17333025_418681021817660_1111101743053144064_n.jpg",
     "topic":"Tree inspire",
     "text":"Small beautiful conner"}
]

mlab.connect()

app.config["UPLOAD_PATH"] = os.path.join(app.root_path, "uploads")
if not os.path.exists(app.config["UPLOAD_PATH"]):
    os.makedirs(app.config["UPLOAD_PATH"])
# for tree in tree_list:
#     new_tree = TreeList()
#     new_tree.src = tree["image_link"]
#     new_tree.title = tree["topic"]
#     new_tree.description = tree["text"]
#     new_tree.save()

login_manager = LoginManager()
login_manager.init_app(app)

# admin_user = User()
# admin_user.username = "admin"
# admin_user.password = "password"
# admin_user.save()

app.secret_key = "tada"

@login_manager.user_loader
def user_loader(user_token):
    found_user = User.objects(token=user_token).first()
    if found_user:
        session_user = Sessionuser(found_user.id)
        return session_user

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
       return render_template("login.html")
    if request.method =="POST":
        user = User.objects(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            session_user = Sessionuser(user.id)
            user.update(set__token=str(user.id))
            login_user(session_user)
            return redirect(url_for("addtree"))
        else:
            return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/')
def hello_world():
    return render_template("home.html", tree_list=TreeList.objects())


@app.route('/addtree', methods=["GET", "POST"])
@login_required
def addtree():
    if request.method == "GET":
        return render_template('addtree.html')
    elif request.method == "POST":
        file = request.files["source"]
        if file:
            filename = secure_filename(file.filename)
            if os.path.join(app.config["UPLOAD_PATH"],filename):
                name_index=0
                # home.png # a.c.b
                original_name = filename.split(".")[0] #home
                original_extend = filename.split(".")[1] #png
                while os.path.exists(os.path.join(app.config["UPLOAD_PATH"],filename)):
                    name_index +=1
                    filename="{0} ({1}).{2}".format(original_name, name_index, original_extend)
            file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
        new_tree = TreeList()
        new_tree.src = url_for("uploads_file", filename=filename)
        new_tree.title = request.form["title"]
        new_tree.description = request.form["description"]
        new_tree.save()
        return render_template('addtree.html')

@app.route('/deltree', methods=["GET", "POST"])
def deltree():
    if request.method == "GET":
        return render_template('deltree.html')
    elif request.method == "POST":
        new_tree1 = TreeList.objects(title=request.form["title"]).first()
        if new_tree1 is not None:
            new_tree1.delete()
        return render_template('deltree.html')
@app.route('/updatetree')
def updatetree():
    if request.method == "GET":
        return render_template('updatetree.html')
    elif request.method == "POST":
        new_tree = TreeList.objects(title=request.form["title"]).first()
        if new_tree is not None:
            new_tree.description = request.form("descriptionupdate")
            new_tree.save()
            return render_template('updatetree.html')

@app.route('/uploads/<filename>')
def uploads_file(filename):
    return send_from_directory(app.config["UPLOAD_PATH"],   filename)

@app.route('/home')
def borua_home():
    return render_template('home.html', tree_list=TreeList.objects())


if __name__ == '__main__':
    app.run()

