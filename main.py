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
                 image_address="../static/images/shark.jpg",
                 rating=0):
        self.author = author
        self.title = title
        self.text = text
        self.time = time
        self.image_address = image_address
        self.rating = rating

    def __str__(self):
        return f"{self.author}, {self.title}, {self.text}, {self.image_address} \n"


notes = [
    [{'id': 1}, Note()],
]

app = flask.Flask(__name__)


@app.route('/')
def hello():
    return flask.redirect('/notes')


@app.route('/notes')
def notes_func():
    return flask.render_template('notes.html', records=notes)


@app.route('/notes/new')
def notes_new():
    if 'userID' in flask.request.cookies:
        return flask.render_template('post_form.html', username=flask.request.cookies.get('userID'))
    return flask.render_template('post_form.html', username='')


@app.route('/note/<int:note_id>')
def note(note_id):
    return flask.render_template('note.html', note=notes[note_id])


@app.route('/change_rating/<int:note_id>', methods=['POST'])
def change_rating(note_id):
    value = flask.request.args['value']  # ???
    notes[note_id][1].rating += int(value)
    return flask.jsonify({'id': note_id, 'rating': notes[note_id][1].rating})


@app.route('/note/<int:note_id>/edit', methods=['POST', 'GET'])
def edit(note_id):
    if flask.request.method == "POST":
        req = flask.request.form

        author = req.get("nm")
        title = req["title"]
        text = flask.request.form["text"]

        tmp = Note(author, title, text, datetime.datetime.now())

        for NOTE in notes:
            if NOTE[0]['id'] == note_id:
                NOTE[1] = tmp
                break

        return flask.redirect('/notes')

    return flask.render_template("edit_form.html", note=notes[note_id - 1])


@app.route('/note/<int:note_id>/delete', methods=['POST', 'GET'])
def delete(note_id):
    if flask.request.method == "GET":
        for i in range(note_id, len(notes)):
            notes[i][0]['id'] -= 1
        notes.remove(notes[note_id - 1])

        return flask.redirect('/notes')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if flask.request.method == 'POST':
        title = flask.request.form.get('title')
        text = flask.request.form.get('text')
        user = flask.request.form['nm']

    tmp = Note(user, title, text, datetime.datetime.now())
    if len(notes) == 0:
        notes.append([{'id': 1}, tmp])
    else:
        notes.append([{'id': notes[-1][0]['id'] + 1}, tmp])

    resp = flask.make_response(flask.render_template('post_form.html'))
    resp.set_cookie('userID', user)
    flask.redirect(flask.url_for('notes_func'))
    return resp
