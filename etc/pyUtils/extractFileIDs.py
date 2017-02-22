def extractFileIDs(inFile, out):
    outString = ""
    with open(inFile, 'r') as f:
        lineNum = 1
        while lineNum < 133:
            line = f.readline()
            fileid = line[line.find('(')+1:line.find(')')]
            outString += fileid + "\n"
            lineNum += 1
    with open(out, 'w') as of:
        of.write(outString)

extractFileIDs('voiceVim_train.transcription', 'fileids.txt')
