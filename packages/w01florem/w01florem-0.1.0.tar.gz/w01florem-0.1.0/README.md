# w01florem

A lorem ipsum creator with the special feature of creating multiple 
files with different names and contents in different folders.

the background of the programme is to use it for tests of w01fm00n 
( https://github.com/w01fdev/w01fm00n ). it could also be useful for 
other programs for tests that have to do with a search of files.

## Mode 1 - Create a nested list of words for a given number of paragraphs

### load class from module
`from w01florem.main import Lorem`

### create instance of a class

#### all important parameters can be transferred in the process:
`lorem = Lorem(paragraphs=2, words_min=30, words_max=100)`

####the parameter values in the example are the default values and can therefore also be omitted:
`lorem = Lorem()`

#### run the program and get a nested list for each paragraph:
`paragraphs = lorem.run()`

#### the values of the respective parameters can be obtained via:
`lorem.get_paragraphs()`  
`lorem.get_words_min()`  
`lorem.get_words_max()`

#### Setting new values after instantiation:
`lorem.set_paragraphs(3)`  
`lorem.set_words_min(20)`  
`lorem.set_words_max(35)`

### Mode 2 - Create lorem ipsum text files in directories and subdirectories

Not yet implemented

## further information:

see docstrings in w01fm00n.py