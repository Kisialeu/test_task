import unittest
import os
from worker import Analyzer


class InitTest(unittest.TestCase):
    def setUp(self):
        self.data = 'qwerty'
        self.file = 'filesize.tmp'
        self.len_data = str(len(self.data))
        with open(self.file, 'w') as f:
            f.write(self.data)

    def tearDown(self):
        os.unlink(self.file)

    def test_NoArguments(self):
        self.assertRaises(TypeError, Analyzer)

    def test_OneArgument(self):
        self.assertRaises(TypeError, Analyzer, self.file)

    def test_FileNotExist(self):
        self.assertRaises(OSError, Analyzer, self.data, self.file)

    def test_InstanceCreate(self):
        self.inst = Analyzer(self.file, self.data)
        self.assertIsInstance(self.inst, Analyzer)


class FilesizeTest(unittest.TestCase):

    def setUp(self):
        self.data = 'qwerty'
        self.file = 'filesize.tmp'
        self.len_data = str(len(self.data))
        with open(self.file, 'w') as f:
            f.write(self.data)

    def tearDown(self):
        try:
            os.unlink(self.file)
        except FileNotFoundError:
            pass

    def test_NoArgument(self):
        self.assertRaises(TypeError, Analyzer.filesize)

    def test_MoreArguments(self):
        self.assertRaises(TypeError, Analyzer.filesize, self.file, self.file)

    def test_UnsupportedArguments(self):
        self.assertRaises(OSError, Analyzer.filesize, int(10))

    def test_FileNotExist(self):
        os.unlink(self.file)
        self.assertRaises(FileNotFoundError, Analyzer.filesize, self.file)

    def test_Success(self):
        self.assertEqual(self.len_data, Analyzer.filesize(self.file))

    def test_Failed(self):
        self.assertNotEqual('8', Analyzer.filesize(self.file))

    def test_ReturnStr(self):
        self.assertMultiLineEqual(str(6), Analyzer.filesize(self.file))


class WordExtractorTest(unittest.TestCase):

    def setUp(self):
        self.textfile = 'in'
        self.emptyfile = 'out'
        self.data = 'qwerty \n Qwerty \n !,.?:QweRty;[] \n q1W34erT78y'
        with open(self.textfile, 'w') as f:
            f.write(self.data)
        with open(self.emptyfile, 'w') as f:
            f.write('')
        self.words_ext = Analyzer(self.textfile, self.emptyfile)
        self.words_ext_empty = Analyzer(self.emptyfile, self.textfile)

    def tearDown(self):
        os.unlink(self.textfile)
        os.unlink(self.emptyfile)

    def test_IsInstanceCreate(self):
        self.assertIsInstance(self.words_ext, Analyzer)

    def test_WordsListInit(self):
        self.words_ext_empty.words_extractor()
        self.assertListEqual(self.words_ext_empty.words, [])

    def test_EmptyFile(self):
        self.words_ext_empty.words_extractor()
        self.assertEqual(len(self.words_ext_empty.words), 0)

    def test_CounterSuccess(self):
        self.words_ext.words_extractor()
        self.assertEqual(len(self.words_ext.words), 4)

    def test_CounterFailed(self):
        self.words_ext.words_extractor()
        self.assertNotEqual(len(self.words_ext.words), not 4)

    def test_ValidData(self):
        self.words_ext.words_extractor()
        self.assertListEqual(self.words_ext.words, ['qwerty', 'qwerty', 'qwerty', 'q1w34ert78y'])


class WordProcessingTest(unittest.TestCase):

    def setUp(self):
        self.textfile = 'in'
        self.emptyfile = 'out'
        self.sample = 'no_file_disk'
        self.data = 'qwerty \n !,.?:QweRty;[] \n q1W34erT78y \t soFTeq 9Softeq9 sofTEQ\n'
        with open(self.textfile, 'w') as f:
            f.write(self.data)
        with open(self.emptyfile, 'w') as f:
            f.write('')
        self.words_ext = Analyzer(self.textfile, self.emptyfile)
        self.words_ext_empty = Analyzer(self.emptyfile, self.textfile)
        self.words_sample = Analyzer(self.textfile, self.sample)

    def tearDown(self):
        os.unlink(self.textfile)
        os.unlink(self.emptyfile)
        try:
            os.unlink(self.sample)
        except FileNotFoundError:
            pass

    def test_WordsExtractorRun(self):
        self.words_ext_empty.words_processing()
        self.assertListEqual(self.words_ext_empty.words, [])

    def test_WordsWriterRun(self):
        self.words_sample.words_processing()
        assert os.path.exists(self.sample) is True

    def test_WordsExtractorReturn(self):
        self.words_ext.words_extractor()
        self.assertEqual(len(self.words_ext.words), 6)

    def test_EmptyFileProcessing(self):
        self.words_ext_empty.words_processing()
        self.assertEqual(len(self.words_ext_empty.words), 0)

    def test_EmptyFileProcessingList(self):
        self.words_ext_empty.words_processing()
        self.assertListEqual(self.words_ext_empty.words, [])

    def test_RemoveNonAlphaWords(self):
        self.words_ext.words_processing()
        self.assertEqual(len(self.words_ext.words), 2)


class WordsWriterTest(unittest.TestCase):

    def setUp(self):
        self.textfile = 'in'
        self.emptyfile = 'out'
        self.nonemptyfile = 'nonempty'
        self.sample = 'no_file_disk'
        self.data = 'qwerty \n !,.?:QweRty;[] \n q1W34erT78y \t soFTeq 9Softeq9 sofTEQ\n'
        self.len_data = len(self.data)
        with open(self.textfile, 'w') as f:
            f.write(self.data)
        with open(self.emptyfile, 'w') as f:
            f.write('')
        with open(self.nonemptyfile, 'w') as f:
            f.write('data')
        self.file_ext = Analyzer(self.textfile, self.emptyfile)
        self.file_ext_empty = Analyzer(self.emptyfile, self.textfile)
        self.file_nonempty = Analyzer(self.textfile,self.nonemptyfile)
        self.file_sample = Analyzer(self.textfile, self.sample)

    def tearDown(self):
        os.unlink(self.textfile)
        os.unlink(self.emptyfile)
        os.unlink(self.nonemptyfile)
        try:
            os.unlink(self.sample)
        except FileNotFoundError:
            pass

    def test_EmptyFileWriteOnDisk(self):
        self.file_sample.words = []
        assert os.path.exists(self.sample) is False
        self.file_sample.words_writer()
        assert os.path.exists(self.sample) is True

    def test_NonEmptyFileWriteOnDisk(self):
        self.file_sample.words = [self.data]
        assert os.path.exists(self.sample) is False
        self.file_sample.words_writer()
        assert os.path.exists(self.sample) is True

    def test_ValidDataWrite(self):
        self.file_sample.words_processing()
        self.filesize = os.path.getsize(self.sample)
        self.lenght = 0
        for item in self.file_sample.words:
            self.lenght +=len(item)
            self.lenght +=1
        self.assertEqual(self.lenght,self.filesize)

    def test_AddDataToExistFile(self):
        self.file_ext.words_processing()
        self.filesize_before = os.path.getsize(self.emptyfile)
        self.file_ext.words_processing()
        self.filesize_after = int(os.path.getsize(self.emptyfile))
        self.lenght = 0
        for item in self.file_ext.words:
            self.lenght +=len(item)
            self.lenght +=1
        self.assertEqual(self.filesize_before + self.lenght, self.filesize_after)


class LineProcessingTest(unittest.TestCase):

    def setUp(self):
        self.textfile = 'in'
        self.emptyfile = 'empty'
        self.file_out = 'out'
        self.data = 'qwerty \n !,.?:QweRty;[] \n q1W34erT78y \n soFTeq \n 9Sof \n teq9 sofTEQ'
        with open(self.textfile, 'w') as f:
            f.write(self.data)
        with open(self.emptyfile, 'w') as f:
            f.write('')


    def tearDown(self):
        os.unlink(self.textfile)
        os.unlink(self.emptyfile)
        try:
            os.unlink(self.file_out)
        except FileNotFoundError:
            pass

    def test_FileCreateToWriteLines(self):
        self.tmp = Analyzer(self.textfile, self.file_out)
        assert os.path.exists(self.file_out) is False
        self.tmp.lines_processing()
        assert os.path.exists(self.file_out) is True

    def test_FileOpenToWriteLines(self):
        self.tmp = Analyzer(self.textfile, self.emptyfile)
        assert os.path.exists(self.emptyfile) is True
        self.tmp.lines_processing()
        assert os.path.exists(self.emptyfile) is True

    def test_WriteValidDataToEmptyFile(self):
        self.tmp = Analyzer(self.textfile, self.emptyfile).lines_processing()
        self.lines_in_data = len(self.data.split('\n'))
        with open(self.emptyfile) as f:
            self.lines_in_file = sum(1 for line in f)
        self.assertEqual(self.lines_in_data, self.lines_in_file)

    def test_WriteValidDataToNonEmptyFile(self):
        assert os.path.exists(self.file_out) is False
        self.tmp = Analyzer(self.textfile, self.file_out).lines_processing()
        assert os.path.exists(self.file_out) is True
        self.tmp = Analyzer(self.textfile, self.file_out).lines_processing()
        assert os.path.exists(self.file_out) is True
        with open(self.file_out) as f:
            self.lines_in_file = sum(1 for line in f)
        self.lines_in_data = len((self.data+self.data).split('\n'))
        self.assertEqual(self.lines_in_data, self.lines_in_file)


if __name__ == '__main__':
    import xmlrunner
    with open('results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False,
            buffer=False,
            catchbreak=False)
