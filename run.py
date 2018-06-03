import argparse
import os
from worker import Analyzer
from custom_loger import Log

parser = argparse.ArgumentParser(description='Task script')

parser.add_argument('file', metavar='path', action="store", help='Path to input file')
parser.add_argument('-mode', dest='mode', action="store", help='Type of processing input file. \
	 "lines" -  Find lines in text file and put them in a new file.\
	 "words"  Find unique words in text file and put them in a new file \
	 Default - "lines"', default="lines", type=str)
parser.add_argument('-out', action="store", dest="out", help='Path to output file. Default - output.txt',
                    default="output.txt", type=str)
parser.add_argument('-log', action="store", dest="out", help='Path to output file. Default - output.txt',
                    default="output.txt", type=str)


def runner():
    Log.logger.debug('Start application.... ')
    try:
        args = parser.parse_args()
        f_path, f_out, mode = (args.file, args.out, args.mode)
    except:
        Log.logger.error('Missing required parameters')
        Log.logger.debug('Stop application....')
        exit()

    if mode != 'lines' and mode != 'words':
        Log.logger.error('Invalid mode!')
        Log.logger.debug('Stop application....')
        exit()

    if not os.path.exists(f_path):
        Log.logger.error('File not found!')
        Log.logger.debug('Stop application....')
        exit()
    elif f_path == f_out:
        Log.logger.error('File must be different!')
        Log.logger.debug('Stop application....')
        exit()

    elif os.path.exists(f_out):
        Log.logger.debug('Output file {} exists'.format(f_out))
        Log.logger.debug('Waiting for user confirmation...')
        choiсe = input('Data will be added to the existing file. Conitnue [y/n] ?\n')
        if choiсe.lower() == 'y':
            Log.logger.debug('Data will be added to the existing file')
            pass
        elif choiсe.lower() == 'n':
            Log.logger.debug('Negative answer is selected. The application will be closed')
            Log.logger.debug('Stop application....')
            exit()
        elif choiсe.lower() != 'n' and choiсe.lower() != 'y':
            Log.logger.error('Invalid choiсe')
            Log.logger.debug('Stop application....')
            exit()

    if mode == 'lines':
        Log.logger.debug('User choiсe: find lines in {} and put them in {}'.format(f_path, f_out))
        obj = Analyzer(args.file, args.out)
        obj.lines_processing()
        Log.logger.debug('Stop application....')
    elif mode == 'words':
        Log.logger.debug('User choiсe: find unique words in {} and put them in {}'.format(f_path, f_out))
        obj = Analyzer(args.file, args.out)
        obj.words_processing()
        Log.logger.debug('Stop application....')


if __name__ == '__main__':
    runner()

