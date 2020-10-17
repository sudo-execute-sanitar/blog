import datetime
import flask


class Note:
    def __init__(self,
                 author="Alex_Designer",
                 title="Shark Sighting",
                 text="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem adipisci, distinctio qui "
                      "doloribus neque debitis. Vero accusamus dolorum rerum sed asperiores beatae earum vel. Maiores "
                      "eveniet iure delectus cum officiis!",
                 time=datetime.datetime.now(),
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
