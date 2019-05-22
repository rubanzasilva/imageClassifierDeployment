from flask import Flask, request, render_template  , redirect , url_for , flash , redirect , send_file
from commons import get_tensor
from inference import get_flower_name
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#create tables
class Uploads(db.Model):
	id = db.Column(db.Integer , primary_key=True)
	name = db.Column(db.String(100) , unique=True , nullable=False )
	image_file = db.Column(db.String(100)  , default='default.jpg')

	def __repr__(self):
		return f"Uploads('{self.name}' , '{self.image_file}')"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'GET':
		return render_template('index.html', value='hi')
	if request.method == 'POST':
		print(request.files)
		if 'file' not in request.files:
			print('file not uploaded')
			return
		file = request.files['file']
		image = file.read()
		category, flower_name = get_flower_name(image_bytes=image)
		get_flower_name(image_bytes=image)
		tensor = get_tensor(image_bytes=image)
		print(get_tensor(image_bytes=image))


		newFile = Uploads(name=file.filename , image_file=file.read())
		db.session.add(newFile)
		db.session.commit()

		#return file.filename
		return render_template('result.html', flower=flower_name, category=category )

		#return 'saved' +   file.filename + 'to the dataset'  

@app.route('/download')
def download():
	file_data = Uploads.query.filter.query.filter_by(id=1).first()
	return send_file(BytesIO(file_data.image_file) , attachment_filename='flask.jpg' , as_attachment=True)


if __name__ == '__main__':
	app.run(debug=True)