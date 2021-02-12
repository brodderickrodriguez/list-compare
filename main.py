import flask
from bs4 import BeautifulSoup



app = flask.Flask(__name__)


data_dict = {
	'input': {
		'text_input_linkedin': '',
		'text_input_excel': ''
	},
	'output': {
		'text_output_linkedin_only': '',
		'text_output_both': '',
		'text_output_excel_only': ''
	}
}


def update_data_dict(d):
	for key, value in data_dict['input'].items():
		try:
			data_dict['input'][key] = d[key]
		except KeyError:
			pass





@app.route('/compare', methods=['POST'])
def compare():

	# print(flask.request.form, file=sys.stderr)
	# text_a = flask.request.form['text_list_a']
	# text_b = flask.request.form['text_list_b']

	update_data_dict(flask.request.form)


	return flask.render_template('index.html', data=data_dict)


@app.route('/')
def main():
	return flask.render_template('index.html', data=data_dict)
