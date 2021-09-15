import requests, json
from bs4 import BeautifulSoup
import re
from tabulate import tabulate     # Tabulate might be useless due to embed


# Might have some issues with Kum Haehyun, since they're named haehyun

xrdCharacters = {
    'ky':"Ky_Kiske",
    'sol':"Sol_Badguy",
    'may':"May",
    'axl':"Axl_Low",
    'millia':"Millia_Rage",
    'zato':"Zato-1",
    'potemkin':"Potemkin",
    'chipp':"Chipp_Zanuff",
    'faust':"Faust",
    'slayer':"Slayer",
    'venom':"Venom",
    'i-no':"I-No", # Jury Rig fix to find images
    'I-no':"ino", #
    'jam':"Jam_Kuradoberi",
    'ramlethal':"Ramlethal_Valentine",
    'elphelt':"Elphelt_Valentine",
    'baiken':"Baiken",
    'johnny':"Johnny",
    'sin':"Sin_Kiske",
    'kum':"haehyun", # Jury Rig Fix to image future image issue
    'haehyun':"Kum_Haehyun", #
    'dizzy':"Dizzy",
    'bedman':"Bedman",
    'jack-o':"jacko", # Jury rig fix to find images
    'jacko':"Jack-O", #
    'leo':"Leo_Whitefang",
    'raven':"Raven",
    'answer':"Answer"
}

striveCharacters = {
    'ky':'Ky_Kiske',
    'sol':'Sol_Badguy',
    'chipp':'Chipp_Zanuff',
    'potemkin':'Potemkin', 
    'pot':'Potemkin', # Potemkin nickname
    'may':'May',
    'zato-1':'Zato-1', 
    'zato':'Zato-1', # Name variation
    'zato1':'Zato-1', # Name variation
    'millia':'Millia_Rage',
    'leo':'Leo_Whitefang',
    'ramlethal':'Ramlethal_Valentine', 
    'ram':'Ramlethal_Valentine', # Ramlethal Nickname
    'axl':'Axl_Low',
    'faust':'Faust',
    'giovanna':'Giovanna',
    'nagoriyuki':'Nagoriyuki',
    'i-no':'I-No', 
    'ino':'I-No', # Name variation
    'goldlewis':'Goldlewis_Dickinson',
    'jack-o':'Jack-O', 
    'jacko':'Jack-O' # Name variation
}

# Table Headers not needed
# Dust Loop Xrd Table 
# Name, Damage, Guard, Startup, Active, Recovery, Frame Adv., Inv., RISC, Prorate, Cancel, Roman, Tension, Level, Hitbox
xrdTableHeader = ['Name', 'Damage', 'Guard', 'Startup', 'Active', 'Recovery', 'FrameAdv.', 'Inv.', 'RISC', 'Prorate', 'Cancel', 'Roman', 'Tension', 'Level'] 
outliers = ['ino', 'haehyun', 'jacko']

footer = {
    ' ':'Input Value in [] notate held input.',
    'Ky_Kiske':'Damage Values in [] are during Shock State',
    'Zato-1':'Input Value in ][ notate on button release',
    'Axl_Low':'Damage value in [] refers to max range'
}

striveSpecialCase = {
    'Reflect Projectile':'F.D.B.'
}


def findxrdFrameData(character, moveName):
    r = requests.get(f'http://www.dustloop.com/wiki/index.php?title=GGXRD-R2/{character}/Frame_Data').text
    #regex = '<.*?>(.+?)</>'

    # Beautiful Soup
    soup = BeautifulSoup(r, 'html.parser')
    #systemData = soup.find('table', {'class':'wikitable'}).text

    # Normal Moves Table
    normalMoves = soup.find('table', {'class':'wikitable'}).find_next_sibling('table', {'class':'wikitable'})
    #print(normalMoves)
    # Trim excess information
    for a in normalMoves.find_all('a'):
        normalMoves.a.decompose()
    for span in normalMoves.find_all('span'):
        normalMoves.find('span').decompose()
    for ul in normalMoves.find_all('ul'):
        normalMoves.find('ul').decompose()

    #Format Text to be ready for table
    normalTableData = normalMoves.text[normalMoves.text.find('5P'):].replace(' ', '').split()
    #print(normalTableData)
    normalsData = []
    normalsData.append(xrdTableHeader)

    move = []

    # Place Data into movelist
    i = 0
    for data in normalTableData:
        move.append(data)
        i+=1
        if i >= 14:
            normalsData.append(move)
            move = []
            i=0

    # Format Normal Data into 1 Move 
    i = 0
    frameData = []
    for normal in normalsData:
        if normalsData[i][0] == moveName:
            frameData.append(xrdTableHeader)
            frameData.append(normalsData[i])
            break
        i+=1
    return frameData

#print(findNormalData('Johnny','5P'))
#universalMechanics = soup.find(id='Universal_Mechanics')
#specialMoves = soup.find(id='Special_Moves')
#overDrives = soup.find(id='Overdrives')


def movexrdImage(character, move):
    reqImg = requests.get(f'https://dustloop.com/wiki/index.php?title=File:GGXRD_{character}_{move}.png').text
    soupImg = BeautifulSoup(reqImg, 'html.parser')
    findRef = soupImg.find('a', {'class':'internal'}).get('href')
    imgLink = f'https://dustloop.com/{findRef}'
    return imgLink

# Special case, Potemkin Reflect Projectile has no image need to omit this function.
# Change to normals
def moveStriveImage(character, move):
    lowerCasedChar = striveCharacters[character.lower()]
    moveRedirect = ''
    if( len(move) > 2):
        moves = move.split(' ')
        i = 0
        while i < len(moves)-1:
            moveRedirect+= moves[i].capitalize() +'_'
            i+=1
        moveRedirect += moves[i].capitalize()
    else:
        moveRedirect = move.upper()
    try:
        reqImg = requests.get(f'https://dustloop.com/wiki/index.php?title=File:GGST_{lowerCasedChar}_{moveRedirect}.png').text
        soupImg = BeautifulSoup(reqImg, 'html.parser')
        findRef = soupImg.find('div', {'id':'file'}, {'class':'fullImageLink'}).find('a').get('href')
        imgLink = f'https://dustloop.com{findRef}'
        return imgLink
    except AttributeError:
        print('Object not found')
        return ''
# Portrait URL for embed
def characterStriveImage(character):
    lowerCased = striveCharacters[character.lower()]
    try:
        reqImg = requests.get(f'https://dustloop.com/wiki/index.php?title=File:GGST_{character}_Portrait.png').text
        soupImg = BeautifulSoup(reqImg, 'html.parser')
        findRef = soupImg.find('div', {'id':'file'}, {'class':'fullImageLink'}).find('a').get('href')
        imgLink = f'https://dustloop.com{findRef}'
        return imgLink
    except AttributeError:
        print('Object not found')
        return ''
    #return findRef

def findStriveSystemData(character):
    convertedChar = striveCharacters[character]
    r = requests.get(f'https://dustloop.com/wiki/index.php?title=GGST/{convertedChar}/Frame_Data').text
    soup = BeautifulSoup(r, 'html.parser')

    findTable = soup.find('table', {'class':'cargoTable'})

    # System Data Table Header
    findTableHeader = findTable.find('tr').find_all('th') # Finds the header for another table if we just find 'th', I think
    tableHeaders = []
    for header in findTableHeader:
        tableHeaders.append(header.text)
    #tableHeaders.remove('')
    #print(f'Info Table: {infoTable}')

    for header in findTable.find_all('table', {'class':'headerSort'}):
        header.decompose()

    #print(infoTable.find_all('td'))

    i = 0
    infoTable = []
    for td in findTable.find_all('td'):
        if(findTable.find_all('td')[i].text == ''):
            infoTable.append('None')
        else:
            infoTable.append(findTable.find_all('td')[i].text)
        i+=1
    # cargoTable noMerge sortable jquery-tablesorter

    characterInfoTable = []
    characterInfoTable.append(tableHeaders)
    characterInfoTable.append(infoTable)
    
    return characterInfoTable

def findStriveFrameData(character, moveName):

    convertedChar = striveCharacters[character]
    r = requests.get(f'https://dustloop.com/wiki/index.php?title=GGST/{convertedChar}/Frame_Data').text

    # Beautiful Soup
    soup = BeautifulSoup(r, 'html.parser')

    # Normal Moves Table
    normals = soup.find('table', {'class':'cargoDynamicTable'})
    
    # Normals Table Header
    findNormalsHeader = normals.find('tr').find_all('th') # Finds the header for another table if we just find 'th', I think
    normalsHeaders = []
    for header in findNormalsHeader:
        normalsHeaders.append(header.text)
    normalsHeaders.remove('')


    # Trim excess information
    for extras in normals.find_all('td', {'class':'details-control'}):
        extras.decompose()


    # Specials Table
    specials = normals.find_next_sibling('table', {'class':'cargoDynamicTable'})

    # Specials Table Headers
    findSpecialsHeader = specials.find('tr').find_all('th')
    specialsHeaders = []
    for header in findSpecialsHeader:
        specialsHeaders.append(header.text)
    specialsHeaders.remove('')

    # Trim excess information
    for extras in specials.find_all('td', {'class':'details-control'}):    
        extras.decompose()
    # Supers Table
    supers = specials.find_next_sibling('table', {'class':'cargoDynamicTable'})
    for extras in supers.find_all('td', {'class':'details-control'}):
        extras.decompose()
    # Throw Table
    other = supers.find_next_sibling('table', {'class':'cargoDynamicTable'})
    for extras in other.find_all('td', {'class':'details-control'}):
        extras.decompose()
    

    # Place Normals into Normals List
    # Can probably combine these two for loops
    i = 0
    normalsList = []
    for td in normals.find_all('td'):
        normalsList.append(normals.find_all('td')[i].text)
        i+=1
    # Place Other Data into normals List
    i = 0
    for td in other.find_all('td'):
        normalsList.append(other.find_all('td')[i].text)
        i+=1


    # Place specials/supers data into specials list
    i = 0
    specialsList = []
    for td in specials.find_all('td'):
        specialsList.append(specials.find_all('td')[i].text)
        i+=1
    i = 0
    for td in supers.find_all('td'):
        specialsList.append(supers.find_all('td')[i].text)
        i+=1


    # Separate Specials Data
    normalsData = []
    move = []
    i = 0
    for data in normalsList:
        if data == '':
            move.append('none')
        else:
            move.append(data)

        i+=1
        if i >= 12:
            normalsData.append(move)
            move = []
            i=0

    # Separate Specials Data
    specialsData = []
    move = []
    i = 0
    for data in specialsList:
        if data == '':
            move.append('none')
        else:
            move.append(data)

        i+=1
        if i >= 13:
            specialsData.append(move)
            move = []
            i=0


    i = 0
    frameData = []
    for normal in normalsData:
        if normalsData[i][0] == moveName:
            frameData.append(normalsHeaders)
            frameData.append(normalsData[i])
            break
        i+=1
    if len(frameData) <= 0:
        i=0
        for special in specialsData:
            ## To lower both strings to avoid not printing.
            if specialsData[i][0].lower() == moveName.lower() or specialsData[i][1].lower() == moveName.lower():
                frameData.append(specialsHeaders)
                frameData.append(specialsData[i])
                break
            i+=1
 
    return frameData

def embedStriveTitle(character, move):
    temp = striveCharacters[character]
    try:
        underscore = temp.index('_')
        temp = f'{temp[0:underscore]} {temp[underscore+1:]} {move}'
    except ValueError:
        temp = f'{temp} {move}'
    return temp
    

def embedStriveUrl(character, move):
    moveRedirect = move
    try:
        if move.index(' '):
            moveRedirect=''
            # For abnormal moves in the table, ex. Reflect Projectile in Potemkin's Table
            try:
                moveRedirect = striveSpecialCase[move]
            except KeyError:
                moves = move.split(' ')
                i = 0
                while i < len(moves)-1:
                    moveRedirect+= moves[i].capitalize() +'_'
                    i+=1
                moveRedirect += moves[i].capitalize()
    except ValueError:
        print()
    url = f'https://dustloop.com/wiki/index.php?title=GGST/{striveCharacters[character]}#{moveRedirect}'
    return url
