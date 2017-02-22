def genTranscript(inFile, out, testOut):
    testTranscript = ""
    lines = []
    with open(inFile, 'r') as f:
        lines = list(f)
    with open(out, 'w') as of:
        for line in lines:
            num = int(line[:line.find('.')])
            s = line[line.find(' '):]
            if s[-1:] == '\n' or s[-1:] == '\r':
                s = s[:-1]
            if num % 5 != 0:
                of.write("<s> %s </s> (%d_0)\n" % (s, num))
            else:
                testTranscript += "<s> %s </s> (%d_0)\n" % (s, num)
    with open(testOut, 'w') as tf:
        tf.write(testTranscript)

genTranscript('transcriptionInput.txt',
              'transcript.txt',
              'voiceVim_test.transcription')
