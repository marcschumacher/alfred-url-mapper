#!/usr/bin/env python
import yaml
import alp
import sys
from os.path import expanduser

def main():
	home = expanduser("~")
	stream = open("%s/.alfred-url-mapper.yaml" % home, 'r')
	configuration = yaml.load(stream)

	commands = {}
	collect_entries(commands, configuration)

	input_key = ''
	parameters = []
	if len(sys.argv) > 1:
		input = sys.argv[1]
		if len(input) > 0:
			split_input = input.split()
			input_key = split_input[0]
			parameters = split_input[1:]

	alp_entries = []
	for key in commands:
		(matches, new_key) = match(input_key, key)
		command_entry = commands[key]
		command_entry.key = new_key
		if matches:
			add_alp_entry(alp_entries, command_entry, parameters)
	
	# Add code to search for entered key and create the alp entries with add_alp_entry
	alp.feedback(alp_entries)

def add_alp_entry(alp_entries, entry, parameters):
	title = entry.name
	subtitle = "[%s]" % entry.key
	if entry.subname:
		subtitle += " %s" % entry.subname
	arg = None
	if entry.url:
		arg = entry.url + get_optional_parameter_string(entry.parameter, parameters, entry.url_prepend_string)
	uid = "url-mapper-%s" % entry.key
	valid = not (None == entry.url)
	iDict = dict(title=title, subtitle=subtitle, arg=arg, uid=uid, valid=valid)
	alp_entries.append(alp.Item(**iDict))

def get_optional_parameter_string(entry_parameter_array, parameters, prepend_string = '?'):
	output = ''
	if entry_parameter_array and len(entry_parameter_array) > 0:
		output = ''
		i = 0
		url_parameters = []
		for single_parameter in parameters:
			if len(entry_parameter_array) >= i+1:
				current_parameter = entry_parameter_array[i]
				url_parameters.append("%s=%s" % (current_parameter, single_parameter))
			i += 1
		output = '&'.join(url_parameters)
		if len(output) > 0 and prepend_string:
			output = prepend_string + output
	return output

def collect_entries(commands, configuration, prefix = ''):
	for key in configuration:
		search_key = "%s%s" % (prefix, key)
		entry = convert_entry(search_key, configuration[key])
		commands[search_key] = entry
		if 'subentries' in configuration[key]:
			collect_entries(commands, configuration[key]['subentries'], search_key)

def convert_entry(key, configuration):
	name = configuration.get('name')
	subname = configuration.get('subname')
	url = configuration.get('url')
	parameter = configuration.get('parameter')
	url_prepend_string = configuration.get('url_prepend_string')
	return Entry(key, name, subname, url, parameter, url_prepend_string)

def match(input, key):
	next_search_pos = 0
	new_key = key
	for char in input:
		pos = key.find(char, next_search_pos)
		if pos == -1:
			return (False, new_key)
		else:
			new_key = get_replaced_char_string(pos, new_key, key[pos].upper())
			next_search_pos = pos + 1
	return (True, new_key)

def get_replaced_char_string(pos, string, char):
	new = list(string)
	new[pos] = char
	return ''.join(new)

class Entry:
	def __init__(self, key, name, subname, url, parameter, url_prepend_string):
		self.key = key
		self.name = name
		self.subname = subname
		self.url = url
		self.parameter = parameter
		self.url_prepend_string = url_prepend_string
	def __str__(self):
		sb = []
		for key in self.__dict__:
			sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return ', '.join(sb)


if __name__ == '__main__':
	main()
