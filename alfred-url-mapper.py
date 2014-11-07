#!/opt/local/bin/python
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

	if len(sys.argv) > 1:
		input = sys.argv[1]
	else:
		input = ''

	alp_entries = []
	for key in commands:
		(matches, new_key) = match(input, key)
		command_entry = commands[key]
		command_entry.key = new_key
		if matches:
			add_alp_entry(alp_entries, command_entry)
	
	# Add code to search for entered key and create the alp entries with add_alp_entry
	alp.feedback(alp_entries)

def add_alp_entry(alp_entries, entry):
	title = entry.name
	subtitle = "[%s]" % entry.key
	if entry.subname:
		subtitle += " %s" % entry.subname
	arg = entry.url
	uid = "url-mapper-%s" % entry.key
	valid = not (None == entry.url)
	iDict = dict(title=title, subtitle=subtitle, arg=arg, uid=uid, valid=valid)
	alp_entries.append(alp.Item(**iDict))

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
	return Entry(key, name, subname, url)

def match(input, key):
	next_search_pos = 0
	new_key = key
	for char in input:
		next_search_pos = key.find(char, next_search_pos)
		if next_search_pos == -1:
			return (False, new_key)
		else:
			new_key = get_replaced_char_string(next_search_pos, new_key, key[next_search_pos].upper())
	return (True, new_key)

def get_replaced_char_string(pos, string, char):
	new = list(string)
	new[pos] = char
	return ''.join(new)

class Entry:
	def __init__(self, key, name, subname, url):
		self.key = key
		self.name = name
		self.subname = subname
		self.url = url
	def __str__(self):
		sb = []
		for key in self.__dict__:
			sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return ', '.join(sb)


if __name__ == '__main__':
	main()
