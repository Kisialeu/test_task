#! /usr/bin/python3


import fileinput
import os
from custom_loger import Log


class Analyzer(Log):

    def __init__(self, input_file, output_file):
        '''	The constructor of the Analyzer class for further processing of text data.

		Accepts two arguments as required parameters - the name or path(str) 
		of the file with the text data for analysis
		and the file name or path(str) for the output data. 
		Example foo = Analyzer('/home/input.t','/home/output.t' )
		'''

        self.f_input = input_file
        Log.logger.debug('Set {} as input file to analyze'.format(self.f_input))
        Log.logger.debug('{} file size {} bytes'.format(self.f_input, Analyzer.filesize(self.f_input)))
        self.f_out = output_file
        Log.logger.debug('Set {} as output file to write data'.format(self.f_out))

    @staticmethod   
    def filesize(file_obj):
        '''Method that returns string the size of the file in bytes.

		Accepts one required parameter file name or path(str)
		'''

        Log.logger.debug('Return {} as file to size analyze'.format(file_obj))
        return str(os.stat(file_obj).st_size)

    def words_extractor(self):
        '''	The method of extracting all words from the input file.

		The file is read line by line, all words are reduced to lowercase, 
		punctuation marks and parentheses around files are deleted. 
		A list is created from all elements
		'''
        Log.logger.info('Start words-extracting method')
        self.words = []
        Log.logger.debug('Initalized empty list for add words')
        try:
            with open(self.f_input, 'r') as f:
                Log.logger.debug('Open {} file for analyzing'.format(self.f_input))
                Log.logger.debug('Start extract words in {}'.format(self.f_input))
                for line in f.readlines():
                    self.words += [word.strip('\'!,.?:;[]''') for word in line.lower().split()]
                Log.logger.debug('Stop extract words in {}'.format(self.f_input))
            Log.logger.debug('Close {} file after completing analysis.'.format(self.f_input))
            Log.logger.debug('List contains {} words'.format(len(self.words)))
        except:
            Log.logger.exception('')
            Log.logger.error('Stop words-extracting method')
        Log.logger.info('Stop words-extracting method')

    def words_processing(self):
        '''The method of analyzing the contents of the input file to find unique words and write to the output file.

			The method provides extraction of words from the incoming file, 
			deletion of elements not consisting of digits, creation of a set of unique words, 
			and transmission of a set of unique words to the recording method in the output file.
			For example, the "Guido" word is a word and will be written into the set but the element "Billy13Gates" will be excluded.
		'''
        Log.logger.info('Start words-processing method')
        Log.logger.debug('Launch words-extracting method')
        self.words_extractor()
        Log.logger.debug('Start create a list with unique words')
        self.words = [item for item in set(self.words) if item.isalpha()]
        Log.logger.debug('Stop create a list with unique words')
        Log.logger.debug('List contains {} unique words'.format(len(self.words)))
        Log.logger.debug('Launch words-writing method')
        self.words_writer()
        Log.logger.info('Stop words-processing method')

    def lines_processing(self):
        '''	The method line by line reads the input file and writes all the found lines to the output file.
		'''
        Log.logger.info('Start line-processing method')
        try:
            Log.logger.debug('Opening {} before writing all lines'.format(self.f_out))
            with open(self.f_out, 'a') as f:
                Log.logger.debug('File {} open'.format(self.f_out))
                Log.logger.debug('Start writing all lines to {} '.format(self.f_out))
                for line in fileinput.input(self.f_input):
                    f.write(line)
                Log.logger.debug('Stop writing all lines to {} '.format(self.f_out))
                Log.logger.debug('Closing {} after writing is successful'.format(self.f_out))
            Log.logger.debug('File {} closed'.format(self.f_out))
            Log.logger.debug('{} file size {} bytes'.format(self.f_out, Analyzer.filesize(self.f_out)))
        except:
            Log.logger.exception('')
            Log.logger.error('Stop line-processing method')
        Log.logger.info('Stop line-processing method')

    def words_writer(self, separator=' '):
        '''The method writes unique words to a file.
		The file specified as output is opened in the context manager,
		and then all the elements from the set of unique words after
		analysis are written to a file with a delimiter (by default - a space).
		'''
        Log.logger.info('Start words-writing method')
        try:
            Log.logger.debug('Opening {} before writing unique words'.format(self.f_out))
            with open(self.f_out, 'a') as f:
                Log.logger.debug('File {} open'.format(self.f_out))
                Log.logger.debug('Start writing unique words to {} '.format(self.f_out))
                for word in self.words:
                    f.write(word + separator)
                Log.logger.debug('Stop writing unique words to {} '.format(self.f_out))
                Log.logger.debug('Closing {} after writing is successful'.format(self.f_out))
            Log.logger.debug('File {} closed'.format(self.f_out))
            Log.logger.debug('{} file size {} bytes'.format(self.f_out, Analyzer.filesize(self.f_out)))
        except:
            Log.logger.exception('')
            Log.logger.error('Stop words-writing method')
        Log.logger.info('Stop words-writing method')
