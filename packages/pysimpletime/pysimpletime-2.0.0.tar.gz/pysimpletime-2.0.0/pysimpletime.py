from datetime import datetime
import inspect
import time

dictionaryStart = {}
dictionaryEnd = {}
dictionaryCallStart = {}
maximalKeyLength = -1
dictionaryCallEnd = {}
keySafe = False
keysStart = []
keysEnd = []

tRealtimeOutput = False
tColourfulOutput = True
tDecimalSpaces = 2
tSafeLog = False
tDebug = False

def writeLog(text):
    global keySafe
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open('pstLog.txt', 'a')
    if keySafe == False:
        keySafe = True
        f.write('\n')
    f.write(dtString + '     ' + text)
    f.close()

def tsetting(debug = False, realtimeOutput = False, decimalSpaces = 2, colorfulOutput = True, safeLog = False):
    global tRealtimeOutput, tDebug, tDecimalSpaces, tColourfulOutput, tSafeLog
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    log = '\n'

    if tColourfulOutput == False:
        color = '\033[0;0mm'
    else:
        color = '\033[1;31m'

    if isinstance(debug, bool) == False:
        log += ('''ValueError: Failed to call function "''' + color + '''tsetting\033[0;0m" on line ''' + str(i.lineno) + ''': "''' + color + '''debug\033[0;0m" must be bool\n''')
    if isinstance(realtimeOutput, bool) == False:
        log += ('''ValueError: Failed to call function "''' + color + '''tsetting\033[0;0m" on line ''' + str(i.lineno) + ''': "''' + color + '''realtimeOutput\033[0;0m" must be bool\n''')
    if isinstance(decimalSpaces, int) == False:
        log += ('''ValueError: Failed to call function "''' + color + '''tsetting\033[0;0m" on line ''' + str(i.lineno) + ''': "''' + color + '''decimalSpaces\033[0;0m" must be integer\n''')
    if isinstance(tColourfulOutput, bool) == False:
        log += ('''ValueError: Failed to call function "''' + color + '''tsetting\033[0;0m" on line ''' + str(i.lineno) + ''': "''' + color + '''colourfulOutput\033[0;0m" must be bool\n''')
    if isinstance(safeLog, bool) == False:
        log += ('''ValueError: Failed to call function "''' + color + '''tsetting\033[0;0m" on line ''' + str(i.lineno) + ''': "''' + color + '''safeLog\033[0;0m" must be bool\n''')

    if log == '\n':
        tRealtimeOutput = realtimeOutput
        tDecimalSpaces = int(decimalSpaces)
        tDebug = debug
        tSafeLog = safeLog
        tColourfulOutput = colorfulOutput
    else:
        print(log)

def __sPoint__(key, f):
    global tRealtimeOutput, tDebug, tDecimalSpaces, dictionaryStart, dictionaryEnd, dictionaryCallStart, dictionaryCallEnd, keysEnd, keysStart, tSafeLog
    key = str(key)

    if tRealtimeOutput == False:
        i = inspect.getframeinfo(f.f_back)

        dictionaryCallStart[key] = i.lineno
        dictionaryStart[key] = time.time()
        keysStart.append(key)

    else:
        i = inspect.getframeinfo(f.f_back)
        key = str(key)

        dictionaryCallStart[key] = i.lineno
        dictionaryStart[key] = time.time()
        keysStart.append(key)

        if dictionaryEnd.get(key) == None:
            pass
        else:
            sTime = dictionaryStart.get(key)
            eTime = dictionaryEnd.get(key)
            rTime = round(sTime - eTime - 0.0020, tDecimalSpaces)

            if tColourfulOutput == False:
                color = '\033[0;0mm'
            else:
                color = '\033[1;31m'

            if rTime < 0:
                rTime *= -1
            elif rTime == 0:
                rTime = 0

            if tDebug == False:
                print(('''Time required for key " ''' + color + '''%s\033[0;0m" is:   "'''%str(key) + color + str(rTime)) + '\033[0;0m" seconds')
                if tSafeLog == True:
                    writeLog(('''Time required for key "%s" is:   "'''%str(key) + str(rTime)) + '" seconds\n')
            else:
                print(('''Time required for key "''' + color + '''%s\033[0;0m" is:   "'''%str(key) + color + str(rTime)) + '''\033[0;0m" seconds      Start line: "''' + color + str(dictionaryCallStart.get(str(key))) + '''\033[0;0m"      End line: "''' + color + str(dictionaryCallEnd.get(str(key))) + '''\033[0;0m"\n''')
                if tSafeLog == True:
                    writeLog(('''Time required for key "%s" is:   "'''%str(key) + str(rTime)) + '" seconds      Start line: "' + str(dictionaryCallStart.get(str(key))) + '"      End line: "' +  str(dictionaryCallEnd.get(str(key))) + '"\n')

def __ePoint__(key, f):
    global tRealtimeOutput, tDebug, tDecimalSpaces, dictionaryStart, dictionaryEnd, dictionaryCallStart, dictionaryCallEnd, keysEnd, keysStart
    key = str(key)

    if tRealtimeOutput == False:
        i = inspect.getframeinfo(f.f_back)

        dictionaryCallEnd[key] = i.lineno
        dictionaryEnd[key] = time.time()
        keysEnd.append(key)

    else:
        i = inspect.getframeinfo(f.f_back)

        dictionaryCallEnd[key] = i.lineno
        dictionaryEnd[key] = time.time()
        keysEnd.append(key)

        if tColourfulOutput == False:
            color = '\033[0;0m'
        else:
            color = '\033[1;31m'

        key = str(key)
        if dictionaryStart.get(key) == None:
            pass
        else:
            sTime = dictionaryStart.get(key)
            eTime = dictionaryEnd.get(key)
            rTime = round(eTime - sTime - 0.0020, tDecimalSpaces)

            if tColourfulOutput == False:
                color = '\033[0;0m'
            else:
                color = '\033[1;31m'

            if rTime < 0:
                rTime *= -1
            elif rTime == 0:
                rTime = 0

            if tDebug == False:
                print(('''Time required for key "''' + color + '''%s\033[0;0m" is:   "'''%str(key) + color + str(rTime)) + '\033[0;0m" seconds')
                if tSafeLog == True:
                    writeLog(('''Time required for key "%s" is:   "'''%str(key) + str(rTime)) + '" seconds\n')
            else:
                print(('''Time required for key "''' + color + '''%s\033[0;0m" is:   "'''%str(key) + color + str(rTime)) + '''\033[0;0m" seconds      Start line: "''' + color + str(dictionaryCallStart.get(str(key))) + '''\033[0;0m"      End line: "''' + color + str(dictionaryCallEnd.get(str(key))) + '''\033[0;0m"\n''')
                if tSafeLog == True:
                    writeLog(('''Time required for key "%s" is:   "'''%str(key) + str(rTime)) + '" seconds      Start line: "' + str(dictionaryCallStart.get(str(key))) + '"      End line: "' +  str(dictionaryCallEnd.get(str(key))) + '"\n')

def point(key):
    global maximalKeyLength

    key = str(key)
    maximalKeyLength = max(len(key), maximalKeyLength)
    f = inspect.currentframe()

    if tColourfulOutput == False:
        color = '\033[0;0m'
    else:
        color = '\033[1;31m'

    if dictionaryStart.get(key) == None:
        __sPoint__(key, f)
    elif dictionaryEnd.get(key) == None:
        __ePoint__(key, f)
    else:
        i = inspect.getframeinfo(f.f_back)

        print('\n')
        print('''KeyError: Failed to call function "point" on line ''' + str(i.lineno) + ''': key "''' + color + str(key) + '''\033[0;0m" already exist ''')
        print('\n')


def __check__(debug, decimalSpaces, realtimeOutput):
    selfTimeStart = time.time()
    keysStart.sort()
    keysEnd.sort()

    if tColourfulOutput == False:
        color = '\033[0;0m'
    else:
        color = '\033[1;31m'

    if keysStart != keysEnd: 
        keysAll = keysEnd + keysStart
        log = '\n'

        for i in keysAll:
            if i in keysEnd:
                if i in keysStart:
                    pass
                else:
                    log += 'Excepted start key on line ' + str(dictionaryCallEnd.get(str(i))) + ''': "''' + color + str(i) + '''\033[0;0m"\n'''
            if i in keysStart:
                if i in keysEnd:
                    pass
                else:
                    log += 'Excepted end key on line ' + str(dictionaryCallStart.get(str(i))) + ''': "''' + color + str(i) + '''\033[0;0m"\n'''
        print(log)

    elif realtimeOutput == False:
        log = '\n'

        for i in keysStart:
            selfTimeEnd = time.time()
            sTime = dictionaryStart.get(i)
            eTime = dictionaryEnd.get(i)
            rTime = round(eTime - sTime - (selfTimeEnd - selfTimeStart) * 2, tDecimalSpaces)

            if rTime < 0:
                rTime *= -1
            elif rTime == 0:
                rTime = 0

            if debug == False:
                log += ('''Time required for key "''' + color + '''%s\033[0;0m" is:'''%str(i) + ' ' * (maximalKeyLength - len(i) + 3) + '''"''' + color + str(rTime)) + '\033[0;0m" seconds \n'
                if tSafeLog == True:
                    writeLog(('''Time required for key "%s" is:'''%str(i) + ' ' * (maximalKeyLength - len(i) + 3) + '''"''' + str(rTime)) + '''" seconds \n''')
            else:
                log += ('''Time required for key "''' + color + '''%s\033[0;0m" is:   '''%str(i) + ' ' * (maximalKeyLength - len(i) + 3) + '''"''' + color + str(rTime)) + '''\033[0;0m" seconds      Start line: "''' + color + str(dictionaryCallStart.get(str(i))) + '\033[0;0m"      End line: "' + color +  str(dictionaryCallStart.get(str(i))) + '''\033[0;0m"\n'''
                if tSafeLog == True:
                    writeLog(('''Time required for key "''' + '''%s" is:   '''%str(i) + ' ' * (maximalKeyLength - len(i) + 3) + '''"''' + str(rTime)) + '''" seconds      Start line: "''' + str(dictionaryCallStart.get(str(i))) + '''"      End line: "''' +  str(dictionaryCallStart.get(str(i))) + '''"\n''')
        print(log)


def tprint():
    global tRealtimeOutput, tDebug, tDecimalSpaces

    __check__(debug = tDebug, decimalSpaces = tDecimalSpaces, realtimeOutput = tRealtimeOutput)