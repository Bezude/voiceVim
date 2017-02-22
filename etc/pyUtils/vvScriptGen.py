# create voice vim scripts from vim log files created with -w option
import ast
import math
import numpy as np


def getLogFromFile(filename):
    """Get contents of filename as one big string"""
    with open(filename) as f:
        s = f.read()
        return s


def genCommandMap(mapfile):
    commandMap = {}
    with open(mapfile) as f:
        all_lines = list(f)
    for line in all_lines:
        end_of_key = line.find(' ')
        key = line[:end_of_key]
        first_char_of_value = line[end_of_key+1]
        if first_char_of_value == '{':
            commandMap[key] = ast.literal_eval(
                line[end_of_key+1:-1].encode('string-escape'))
        else:
            commandMap[key] = line[end_of_key+1:-1]
    return commandMap


def genScript(log, commandMap):
    """Create a script of voiceVim commands from a vim log based on a given
    command map."""
    charCount = len(log)
    charIndex = 0
    keys = commandMap.keys()
    keys.sort(key=len, reverse=True)
    scriptItems = []
    keyEnders = {" ": " ", "\r": "\r", ":": ":", "\n": "\n", "(": "(",
                 "\x09": "\x09", "\x1b": "\x1b"}
    keys.remove("")
    while charIndex < charCount:
        c = log[charIndex]
        charsLeft = charCount - charIndex
        interpretAs = None
        for k in keys:
            if len(k) <= charsLeft and k == log[charIndex:charIndex+len(k)]:
                if (len(k) == 1 or (charsLeft == len(k) or
                                    log[charIndex+len(k)] in keyEnders)):
                    charIndex += len(k)
                    interpretAs = commandMap[k]
                    break
        if interpretAs is None:  # might be processing an invisible keystroke
            invisibleChar = r"\x" + "{0:02x}".format(ord(c))
            if invisibleChar == r"\x80" and log[charIndex+1] == 'k':
                # special vim control character sequence
                vimCodeChar = log[charIndex+2]
                controlMap = commandMap[invisibleChar]
                interpretAs = controlMap[vimCodeChar]
                charIndex += 3  # these control sequences are 3 char long
            else:
                try:
                    interpretAs = commandMap[invisibleChar]
                except KeyError:
                    print "Don't know how to interpret %s" % c
                charIndex += 1
        if interpretAs:
            scriptItems.append(interpretAs)

    return distillScriptFromScriptItems(scriptItems)


def distillScriptFromScriptItems(items):
    """Determine which possible intepretation of a given key is correct based
    on the mode vim is currently in."""
    mode = "normal"
    script = []
    for x in items:
        if type(x) is dict:
            s = x[mode]
            if s == "insert" or s == "newline" or s == "append":
                mode = "insert"
            elif s == "visualmode" or s == "visualline" or s == "visualblock":
                mode = "visual"
            script.append(s)
        elif type(x) is str:
            if x == "escape":
                mode = "normal"
            elif x == "sierra":
                mode = "insert"
                # elif x == "charlie": # TODO: react to change operation
            script.append(x)
    script = findShortHands(script)
    script = filter(lambda a: a != "", script)
    return script


def findShortHands(script):
    """Some character sequences are common enough to warrant their own
    command word. Find those sequences and replace them with their word."""
    short = ["space", "equals", "space"]
    word = "assign"
    index = 0
    size = len(script)
    while index < size:
        if (index + len(short) < size):
            match = True
            for i in xrange(len(short)):
                if short[i] != script[index+i]:
                    match = False
                    break
            if match:
                for i in xrange(len(short)):
                    script[index+i] = ""  # delete the sequence
                script[index] = word  # replace it with the shorthand
        index += 1
    return script


def writeScriptToFile(script,
                      filename="script.txt",
                      lineLenMean=20,
                      lineStdDev=3,
                      countFrom=1):
    """Split a script into a series of lines with length determined by a normal
    distribution. For constant length lines set lineStdDev to 0. Lines are
    prepended with a number unless countFrom is set to 0."""
    with open(filename, 'a') as f:
        index = 0
        print "script is %d words long" % len(script)
        while index < (len(script) - 1):
            if lineStdDev:
                l = np.random.normal(lineLenMean, lineStdDev)
                l = math.floor(l) if l - math.floor(l) < 0.5 else math.ceil(l)
            else:
                l = lineLenMean
            l = min(int(l), len(script) - index - 1)
            prefix = str(countFrom) + ". " if countFrom else ""
            print "%d:%d" % (index, index+l)
            f.write(prefix + " ".join(script[index:index+l]) + "\n")
            index += max(1, l)
            if countFrom:
                countFrom += 1


def testIt(logFile, cm='commandMap.txt', target=None):
    comap = genCommandMap(cm)
    testLog = getLogFromFile(logFile)
    script = genScript(testLog, comap)
    writeScriptToFile(script, filename=target if target else "script.txt")
