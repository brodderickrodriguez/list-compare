import logging
import sys
import builtins
import flask
from functools import partial
import re
from bs4 import BeautifulSoup


_app = flask.Flask(__name__)


class Namespace:
	linkedin_input = 'text_input_linkedin'
	excel_input = 'text_input_excel'
	linkedin_output = 'text_output_linkedin_only'
	both_output = 'text_output_both'
	excel_output = 'text_output_excel_only'


def print(*args, **kwargs):
	builtins.print(*args, **kwargs, file=sys.stderr)


data_dict = {
	'input': {
		Namespace.linkedin_input: '',
		Namespace.excel_input: ''
	},
	'output': {
		Namespace.linkedin_output: '',
		Namespace.both_output: '',
		Namespace.excel_output: ''
	}
}


def update_data_dict(d):
	for key, value in data_dict['input'].items():
		try:
			data_dict['input'][key] = d[key]
		except KeyError as e:
			logging.warning(f'could not update data dict for key={key}. excepted with e={e}')


def parse_excel(text):
	name_list = text.split('\r\n')

	ops = [
		partial(str.lower),
		partial(lambda old, new, s: s.replace(old, new), r'\r', ''),
		partial(re.sub, ' +', ' '),
	]

	for i, name in enumerate(name_list):
		for op in ops:
			name_list[i] = op(name_list[i])

	name_set = set(filter(lambda n: len(n) > 0, name_list))
	return name_set


def parse_ln_source(text):
	return ''


def log_user_data(request):
	logging.info(f'remote ip: {request.remote_addr}')
	logging.info(f'remote usr: {request.remote_user}')
	print('getting IP', request.remote_addr, request.remote_user)


@_app.route('/', methods=['POST'])
def compare():
	logging.info(f'requested: {flask.request.form}')
	log_user_data(flask.request)
	update_data_dict(flask.request.form)

	ln_name_set = parse_ln_source(flask.request.form[Namespace.linkedin_input])
	excel_name_set = parse_excel(flask.request.form[Namespace.excel_input])

	data_dict['output'][Namespace.linkedin_output] = ln_name_set
	data_dict['output'][Namespace.excel_output] = str(excel_name_set)

	logging.info(f'returning: {data_dict}')
	return flask.render_template('index.html', data=data_dict)


@_app.route('/list-compare', methods=['POST'])
def _():
	return compare()


@_app.route('/')
def entry():
	return flask.render_template('index.html', data=data_dict)


application = _app
logging.basicConfig(level=logging.DEBUG, filename='instance.log')
