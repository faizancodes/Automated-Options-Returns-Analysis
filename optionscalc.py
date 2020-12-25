import pyautogui
import time
import requests
from bs4 import BeautifulSoup
from itertools import cycle
import pyperclip

# # Get Proxies 
def getProxies(inURL):
    
    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    terms = soup.find_all('tr')
    IPs = []

    for x in range(len(terms)):  
        
        term = str(terms[x])        
        
        if '<tr><td>' in str(terms[x]):
            pos1 = term.find('d>') + 2
            pos2 = term.find('</td>')

            pos3 = term.find('</td><td>') + 9
            pos4 = term.find('</td><td>US<')
            
            IP = term[pos1:pos2]
            port = term[pos3:pos4]
            
            if '.' in IP and len(port) < 6:
                IPs.append(IP + ":" + port)
                #print(IP + ":" + port)

    return IPs 


#Cycle through the proxies and get one to use 
proxyURL = "https://www.us-proxy.org/"
pxs = getProxies(proxyURL)
proxyPool = cycle(pxs)


allData = []

# Go through different strike prices 
for i in range(3):

    
    if i == 0:
        
        time.sleep(2)
        
        #Get the location of Get Price button
        getPrice = list(pyautogui.locateAllOnScreen('getPrice.png', confidence = 0.95))
        getPriceButton = pyautogui.center((getPrice[0][0], getPrice[0][1], getPrice[0][2], getPrice[0][3]))


        # Type in stock ticker and get the price 
        stock = pyautogui.center((getPrice[0][0] - 200, getPrice[0][1], getPrice[0][2], getPrice[0][3]))

        pyautogui.click(stock, duration = 0.10) 
        pyautogui.write('AAPL', interval = 0.05)
        pyautogui.click(getPriceButton, duration = 0.10) 


    # Find all Select Option buttons and click the button corresponding to the back month
    selectOption = list(pyautogui.locateAllOnScreen('selectOption.png', confidence = 0.75))

    backMonthSelection = pyautogui.center((selectOption[0][0], selectOption[0][1], selectOption[0][2], selectOption[0][3]))
    pyautogui.click(backMonthSelection, duration = 0.10) 


    time.sleep(0.3)


    # Locate the text 'Choose an option' and click the corresponding month
    chooseOption = list(pyautogui.locateAllOnScreen('chooseOption.png', confidence=0.80))
    centerChooseOption = list(pyautogui.center((chooseOption[0][0], chooseOption[0][1], chooseOption[0][2], chooseOption[0][3])))

    if i == 0:
        march = centerChooseOption.copy()
        march[0] += 450
        march[1] += 150
        pyautogui.click(march, duration=0.10) 


    # Locate and click on an ask price
    ask = centerChooseOption.copy()
    ask[0] -= 300
    ask[1] += (885 + (i * 50))
    pyautogui.click(ask, duration=0.15) 


    # Copy and extract the option details for the Back Month
    time.sleep(0.2)
    
    distance = 50
    if i >= 1: distance = 350
        
    pyautogui.click(backMonthSelection[0] - distance, backMonthSelection[1], duration = 0.10, clicks=3) 
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.05) 

    backMonthOption = pyperclip.paste()
    backMonthOption = backMonthOption[0 : backMonthOption.find('Select')]


    # Find the select option button for the front month
    frontMonthSelection = pyautogui.center((selectOption[-1][0], selectOption[-1][1], selectOption[-1][2], selectOption[-1][3]))
    pyautogui.click(frontMonthSelection, duration=0.15) 

    
    if i == 0:
        # Click on a month that comes before the back month
        feb = centerChooseOption.copy()
        feb[0] += 50
        feb[1] += 150
        pyautogui.click(feb, duration=0.10) 


    # Click on the corresponding ask price 
    pyautogui.click(ask[0] + 30, ask[1] - 50, duration=0.2) 


    # Copy and extract the option details for the Front Month
    time.sleep(0.2)
    
    pyautogui.click(frontMonthSelection[0] - distance, frontMonthSelection[1], duration = 0.10, clicks=3) 
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.05) 

    frontMonthOption = pyperclip.paste()
    frontMonthOption = frontMonthOption[0 : frontMonthOption.find('Select')]



    # Find and click the calculate button
    calculate = list(pyautogui.locateAllOnScreen('calculate.png', confidence=0.85))
    centerCalculate = list(pyautogui.center((calculate[0][0], calculate[0][1], calculate[0][2], calculate[0][3])))
    pyautogui.click(centerCalculate, duration=0.10) 


    # Scroll down the webpage and copy the contents of the returns matrix and paste it into the notepad 
    time.sleep(1.2)
    pyautogui.scroll(-250)


    copyText = list(pyautogui.locateAllOnScreen('returns.png', confidence=0.75))
    centerText = list(pyautogui.center((copyText[0][0], copyText[0][1], copyText[0][2], copyText[0][3])))
    pyautogui.click(centerText[0], centerText[1] - 50, duration=0.10) 

    pyautogui.dragTo(3550, 1240, button='left', duration=0.25)
    pyautogui.hotkey('ctrl', 'c')

    notepad = list(pyautogui.locateAllOnScreen('notepad.png', confidence=0.85))
    centerNotepad = list(pyautogui.center((notepad[0][0], notepad[0][1], notepad[0][2], notepad[0][3])))
    pyautogui.moveTo(centerNotepad, duration=0.2)
    pyautogui.click()

    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.15)
    pyautogui.press('backspace')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.15)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.2)





    #Open text file which contains the matrix data and append it to a 2D list
    table = []
    adjTable = []

    rawEntryCostt = ''
    entryCost = 0
    maxRisk = 0
    maxReturn = []
    breakevens = []
    currPrice = 0

    f = open("optionData.txt", "r")
    rowNums = []
    appendNum = True


    for i, line in enumerate(f):

        if i == 0:
            currPrice = float(line[line.find('$') + 1 : line.find('on') - 1])


        if i == 1:

            rawEntryCostt = line[0 : line.find('see') - 1]
            rawEntryCost = line[13 : line.find('(')]
            entryCost = float(rawEntryCost.replace(',', '')) 

            if 'net debit' in line: entryCost = entryCost * -1


        if i == 3:

            rawMaxRisk = line[15 : line.find('at a') - 1]
            maxRisk = float(rawMaxRisk.replace(',', ''))


        if i == 5:

            rawMaxReturn = line[17 : line.find('at a') - 1]
            maxReturn.append(float(rawMaxReturn.replace(',', '')))
            
            rawMaxReturn2 = line[line.find('price of') + 10 : line.find('at exp') - 1]
            maxReturn.append(float(rawMaxReturn2.replace(',', '')))


        if i == 7:

            breakevens.append(float(line[line.find('$') + 1 : line.find(',')]))

            try:
                line = line[line.find(',') + 1 : ]
                breakevens.append(float(line[line.find('$') + 1 : line.find('.') + 2]))

            except:
                continue

        if i >= 13:

            if '%' not in line and appendNum != i:
                rowNums.append(float(line))
                appendNum = True

            elif '%' in line:

                rowNums.append(line.replace('\n', ''))
                table.append(rowNums)

                rowNums = []
                appendNum = i + 1


    f.close()


    '''
    Iterate through the 2D list and apply a multiplier function that adjusts 
    the values based on an approximate probability of the stock increasing or decreasing 
    by the specified percentage

    Append these new values to a new 2D list to accurately depict the risk/reward of the option
    ''' 

    summ = 0
    nums = 0

    posReturns = 0
    posSums = 0

    negReturns = 0
    negSums = 0

    for row in table:

        percent = float(row[-1][:-1])

        if percent != 0:
            multiplier = abs(50 / percent * 0.05)
        else:
            multiplier = 2

        temp = []

        for num in row:

            try:
                temp.append(float(multiplier * num))
                summ += num
                nums += 1

                if num >= 0:
                    posReturns += num
                    posSums += 1
                else:
                    negReturns += num
                    negSums += 1

            except:
                continue


        adjTable.append(temp)


    '''
    print('\nOriginal Matrix Avg:', summ / nums)
    print('\nAvg Positive Return:', posReturns / posSums)
    print('Avg Negative Return:', negReturns / negSums)
    '''


    overallSumm = 0
    overallNums = 0

    posReturns = 0
    posSums = 0

    negReturns = 0
    negSums = 0

    for row in adjTable:

        for num in row:

            try:
                overallSumm += num
                overallNums += 1
            except:
                print(num)

            if num >= 0:
                posReturns += num
                posSums += 1
            else:
                negReturns += num
                negSums += 1



    adjAvg = round(overallSumm / overallNums, 2)
    posScore = round(posReturns / posSums, 2)
    negScore = round(negReturns / negSums, 1)


    try:
        maxReturnScore = round(maxReturn[0] * (50 / ((abs(maxReturn[1] - currPrice) / currPrice) * 100.0) * 0.05), 1)
    except ZeroDivisionError:
        maxReturnScore = 0

    try:
        breakevenScore = 2 * ((abs(breakevens[0] - currPrice) / currPrice) * 100.0) 
        breakevenScore += 2 * ((abs(breakevens[1] - currPrice) / currPrice) * 100.0) 
        breakevenScore /= 2
    except: 
        breakevenScore = 0


    overallScore = ((adjAvg * 2) + (posScore + negScore) + ((posSums / overallNums) * 2) + (maxReturnScore * 2) - (breakevenScore * 2)) / 3


    print('\n\nReturns Analysis for', backMonthOption, frontMonthOption)

    print('\n\n' + rawEntryCostt)
    print('\nAdjusted Matrix Avg:', adjAvg)
    print('\nScore of Positive Returns:', posScore, round(posSums / overallNums, 2))
    print('Score of Negative Returns:', negScore, round(negSums / overallNums, 2))
    print('Max Return & Score', maxReturn[0], maxReturnScore)
    print('Breakevens & Score', breakevens, round(breakevenScore, 2))

    print('\nOverall Score:', round(overallScore, 2))
    
    allData.append([str(backMonthOption) + " " + str(frontMonthOption), overallScore, adjAvg, posScore, negScore, maxReturn[0], maxReturnScore, breakevens, breakevenScore])
    
    
    pyautogui.click(2155 ,240, duration=0.2, clicks=2)
    pyautogui.scroll(850)
