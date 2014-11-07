#alfred-url-mapper

This little Python script for [Alfred](http://www.alfredapp.com) can be used to create shortcuts for urls easily.

## Installation
1. Clone the repo to a folder of your choice.
1. Install pyyaml e.g. with pip: `pip install pyyaml`.
1. Clone [alp](https://github.com/phyllisstein/alp) and put the library folder inside the installation path.

## Setup in Alfred:
Create a new shortcut with following configuration:

1. Keyword: "-", with space: (deselected), *Argument Optional*
1. Placeholder title: *Shortcuts*
1. Placeholder Subtext: *empty*
1. "Please wait" subtext: *Loading shortcuts...*
1. Language: */bin/bash*
1. Escaping (activate the following): Backquotes, Double Quotes
1. Script: `<path to script>/alfred-url-mapper.py {query}`

## Configuration

### Location
Make sure that you create a configuration file inside your home folder: `~/alfred-url-mapper.yaml`. Use the sample file provided from this repository (`alfred-url-mapper.yaml`) as starting point.

### Configuration structure
**TBD**