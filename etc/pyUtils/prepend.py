def prepend(filename, p):
    with open(filename, 'r+') as f:
        lines = list(f)
        newLines = ""
        for line in lines:
            newLines += p + line
        f.seek(0)
        f.write(newLines)

prepend('voiceVim_train.fileids', 'cleaned/')
prepend('voiceVim_test.fileids', 'cleaned/')
