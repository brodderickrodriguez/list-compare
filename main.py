import logging
import flask
from bs4 import BeautifulSoup


_app = flask.Flask(__name__)


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
		except KeyError as e:
			logging.warning(f'could not update data dict for key={key}. excepted with e={e}')


@_app.route('/', methods=['POST'])
def compare():
	logging.info(f'requested: {flask.request.form}')

	update_data_dict(flask.request.form)
	logging.info(f'returning: {data_dict}')
	return flask.render_template('index.html', data=data_dict)


@_app.route('/list-compare', methods=['POST'])
def _():
	return compare()


@_app.route('/')
def main():
	return flask.render_template('index.html', data=data_dict)


application = _app
logging.basicConfig(level=logging.DEBUG)
