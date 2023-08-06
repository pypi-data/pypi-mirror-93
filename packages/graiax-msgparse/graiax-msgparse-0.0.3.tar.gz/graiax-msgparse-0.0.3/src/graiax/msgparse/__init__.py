from graia.application.message.elements.internal import *
from graia.application.message.chain import MessageChain
from argparse import *
from io import StringIO
from typing import Union
import pickle
import base64
import shlex
import regex

try:
	import ujson as json
except ImportError:
	import json

class ParserExit(RuntimeError):
    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message

class MsgString:
	"""
	将String与MessageChain无丢失互相转化的办法
	使用方法
	>>> message = MessageChain.create([Plain('-s '), At(123)])
	>>> parser = MessageChainParser()
	>>> parser.add_argument('-s', type = MsgString.decode())
	>>> args = parser.parse_args(message)
	>>> args.s
	__root__ = [At(123)]

	method默认为'json'(可选'pickle'，前提是parse_obj的method也为'pickle')
	"""

	@classmethod
	def encode(cls, method: str='json'):
		all_method = {'json': cls.json_string, 'pickle': cls.pickle_string}
		if method not in all_method:
			raise ValueError('Unsupport method')
		return all_method[method]

	@classmethod
	def decode(cls, method: str='json'):
		all_method = {'json': cls.json_msg, 'pickle': cls.pickle_msg}
		if method not in all_method:
			raise ValueError('Unsupport method')
		return all_method[method]

	@staticmethod
	def json_msg(string: str) -> MessageChain:
		result = []
		for match in regex.split(r'(\[json_element:.+?\])', string):
			if element := regex.fullmatch(r'(\[json_element:(.+?)\])', match):
				try:
					result.append(json.loads(base64.b64decode(element.group(2))))
				except:
					result.append({'type': 'Plain', 'text': match})
			elif match:#去除空字符串
				result.append({'type': 'Plain', 'text': match})
		return MessageChain.parse_obj(result)

	@staticmethod
	def pickle_msg(string: str) -> MessageChain:
		result = []
		for match in regex.split(r'(\[pickle_element:.+?\])', string):
			if element := regex.fullmatch(r'(\[pickle_element:(.+?)\])', match):
				try:
					result.append(pickle.loads(base64.b64decode(element.group(2))))
				except:
					result.append(Plain(match))
			elif match:#去除空字符串
				result.append(Plain(match))
		return MessageChain.create(result)

	@staticmethod
	def json_string(message_arg: MessageChain, space_in_gap: bool=False) -> list:
		str_input = ''
		gap = ' ' if space_in_gap else ''
		hyper_message = message_arg.dict()['__root__']
		for n, element in enumerate(hyper_message):
			if element.get('type') == 'Plain':
				if (last_mes := hyper_message[n-1]).get('type') != 'Plain':
					str_input += gap
				str_input += element.get('text','')
			else:
				json_element = base64.b64encode(json.dumps(element).encode('UTF-8'))
				if (last_mes := hyper_message[n-1]).get('type') == 'Plain':
					str_input += '' if last_mes.get('text','').endswith(' ') else gap
				else:
					str_input += gap
				str_input += '[json_element:{}]'.format(
					json_element.decode("ascii"))
		return str_input

	@staticmethod
	def pickle_string(message_arg: MessageChain, space_in_gap: bool=False) -> list:
		str_input = ''
		gap = ' ' if space_in_gap else ''
		hyper_message = message_arg.__root__
		for n, element in enumerate(hyper_message):
			if type(element) is Plain:
				if not type(last_mes := hyper_message[n-1]) is Plain:
					str_input += gap
				str_input += element.text
			else:
				pickle_element = base64.b64encode(pickle.dumps(element))
				if type(last_mes := hyper_message[n-1]) is Plain:
					str_input += '' if last_mes.text.endswith(' ') else gap
				else:
					str_input += gap
				str_input += '[pickle_element:{}]'.format(
					pickle_element.decode("ascii"))
		return str_input

class Element2Mirai:
	def __init__(self, method: str = 'json'):
		if method in ('json', 'pickle'):
			self.method = Element2Msg(method)
		else:
			raise ValueError(f'no such a method:{method}')

	def __call__(self, string: str):
		return self.method(string).asSerializationString()

class MessageChainParser(ArgumentParser):
	"""
	为MessageChain设计的Parser
	继承自标准库的ArgumentParser
	注:此模块仅验证了add_argument和parse_args的部分功能
	　　其他功能暂未验证其是否能够正常工作
	"""

	def __init__(self, *args, **kwargs):
		self.start = kwargs.pop('start_string', None)
		self.method = kwargs.pop('method', 'json')
		self.std = kwargs.pop('std', StringIO())
		if self.method not in ('json', 'pickle'):
			raise ValueError('Unsupport method')
		super().__init__(*args, **kwargs)

	def _print_message(self, message, file=None):
		self.std.write(message)

	def exit(self, status=0, message=None):
		raise ParserExit(status=status, message=message)

	def parse_args(self, message: Union[MessageChain, str], space_in_gap: bool = False):
		if type(message) is MessageChain:
			message_arg = message.asMerged().asHypertext()
			if self.start and message.asDisplay().startswith(self.start):
				message_arg = message_arg[(0,len(self.start)):]
			message_string = MsgString.encode(self.method)(message_arg, space_in_gap)
		elif type(message) is str:
				message_string = message[len(self.start):] if self.start else message
		else:
			raise ValueError('Unsupport message type')
		return super().parse_args(shlex.split(message_string))