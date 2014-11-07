#alfred-url-mapper

This little Python script for [Alfred](http://www.alfredapp.com) can be used to create shortcuts for urls easily.

## Installation
Simply check out the repo to a folder of your choice. After that you need to check out alp and put the [alp](https://github.com/phyllisstein/alp) library folder inside the installation path of the alfred-url-mapper.

## Setup in Alfred:
Create a new shortcut with following configuration:

1. Keyword: "-", with space: (deselected), "Argument Optional"
1. Placeholder title: "Shortcuts"
1. Placeholder Subtext: <empty>
1. "Please wait" subtext: "Loading shortcuts..."
1. Language: "/bin/bash"
1. Escaping (activate the following): Backquotes, Double Quotes
1. Script: "<path to script>/alfred-url-mapper.py {query}"

## Configuration
Make sure that you create a configuration file in the same directory as the script.
A sample for the configuration file can be found in this repository (alfred-url-mapper.yaml).