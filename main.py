import datetime
import flask


class Note:
    def __init__(self,
                 author="Alex_Designer",
                 title="Shark Sighting",
                 text="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem adipisci, distinctio qui "
                      "doloribus neque debitis. Vero accusamus dolorum rerum sed asperiores beatae earum vel. Maiores "
                      "eveniet iure delectus cum officiis!",
                 time=datetime.datetime(2020, 10, 9),
                 image_address="../static/images/shark.jpg"):
        self.author = author
        self.title = title
        self.text = text
        self.time = time
        self.image_address = image_address


records = [
    [{'id': 1}, Note()],
]

app = flask.Flask(__name__)


@app.route('/notes')
def notes():
    return flask.render_template('notes.html', notes=records)


@app.route('/notes/new')
def notes_new():
    if 'userID' in flask.request.cookies:
        return flask.render_template('post_form.html', username=flask.request.cookies.get('userID'))
    return flask.render_template('post_form.html', username='')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if flask.request.method == 'POST':
        title = flask.request.form.get('title')
        text = flask.request.form.get('text')
        user = flask.request.form['nm']

    tmp = Note(user, title, text, datetime.datetime.now())
    records.append([{'id': records[-1][0]['id'] + 1}, tmp])

    resp = flask.make_response(flask.render_template('post_form.html'))
    resp.set_cookie('userID', user)
    flask.redirect(flask.url_for('notes'))
    return resp