""" 
> Here We're Gonna Use Flask + Marshmallow + SQLALchemy +
> request_html to make a lyrics scrapping API and we're
> Gonna Scrap Lyrics From Google.
"""
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os.path import (
    abspath,
    dirname,
    join,
)
from requests_html import HTMLSession

basedir = abspath(dirname(__name__))

# Initializing Flask App
app = Flask(__name__)
app.secret_key = "@#%^FDSTW$^WSGBS%#W$YHUR"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + join(basedir, "db.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# A SQLAlchemy Model Class acting as Database
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    singer = db.Column(db.String(100))
    lyrics = db.Column(db.Text)
    def __init__(self, name, singer, lyrics):
        self.name = name
        self.singer = singer
        self.lyrics = lyrics
    def __repr__(self):
        return "<Song: %r>" % self.name

class SongSchema(ma.Schema):
    class Meta:
        fields = ("name", "singer", "lyrics")
    

def url(song_name):
    list_ = song_name.split()
    list_.append("lyrics")
    name = "+".join(list_)
    # print(name)
    return "https://www.google.com/search?safe=active&sxsrf=ALeKk03EbjukJL_bDCCTT_keRhTcYUFBBw%3A1585116544851&ei=gPV6XobMM4r2rQHMoqWgCg&q="+ name + "&oq="+ name + "+&gs_l=psy-ab.3.0.0i20i263j0l8j0i20i263.356254.360799..361918...0.1..0.396.4843.0j5j8j6......0....1..gws-wiz.......0i71j35i39j0i67.Hqqc8FjDoP0"

def get(url):
    session = HTMLSession()
    r = session.get(url)
    singer = r.html.find("div[class='wwUB2c PZPZlf'] span a", first=True)
    name = r.html.find(".gsmt span", first=True)
    temp = r.html.find("span[jsname='YS01Ge']")
    lyrics = []
    for l in temp:
        lyrics.append(l.text)
    return {"song_name": name.text, "singer_name": singer.text, "lyrics": lyrics}

song_schema = SongSchema()
# Routing Section
@app.route('/')
def index():
    return render_template("index.html")

# !NOTE: If there are no result in the database then it'll
# !NOTE: return an empty list i.e '[]' i.e len(object) = 0
@app.route('/api/get_lyrics', methods=['GET', 'POST'])
def get_lyrics():
    if request.method == "POST":
        name = request.form['name']
        if name != "":
            print("Fetching From Google.")
            url_ = url(name)
            a = get(url_)
            song = Song(name=a['song_name'], singer=a['singer_name'], lyrics=str(a['lyrics']))
            db.session.add(song)
            db.session.commit()
            return jsonify(a)
    else: 
        return "NOT DONE YET"

    
if __name__ == "__main__":
    app.run(debug=True)




