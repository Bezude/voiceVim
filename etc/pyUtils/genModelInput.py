def genModelInput(inFile, out):
    outString = ""
    with open(inFile, 'r') as f:
        lines = list(f)
        for line in lines:
            outString += line[line.find(' ')+1:]
    with open(out, 'w') as of:
        of.write(outString)

genModelInput('transcriptionInput.txt', 'modelInput.txt')
