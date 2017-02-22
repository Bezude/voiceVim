def genFileIDs(out, testOut):
    testFiles = ""
    with open(out, 'w') as f:
        for i in xrange(265):
            if (i % 5 != 0):
                f.write(str(i) + "_0" + "\n")
            else:
                testFiles += str(i) + "_0" + "\n"
    with open(testOut, 'w') as tf:
        tf.write(testFiles)

genFileIDs('voiceVim_db_train.fileids', 'voiceVim_db_test.fileids')
