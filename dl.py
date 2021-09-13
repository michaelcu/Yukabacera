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

### Headers
# System Data
striveCharacterTableHeader = ['Name','Defense','Guts','Prejump','Backdash','Weight','Unique Movement Options']
# Normals and Other
striveNormalsTableHeader = ['Input', ' Damage', 'Guard', 'Startup', 'Active', 'Recovery', 'onBlock', 'onHit', 'riscGain', 'Level', 'Invuln', 'Prorate']
# Specials and Super
striveSpecialsTableHeader = ['Input', ' Damage', 'Guard', 'Startup', 'Active', 'Recovery', 'onBlock', 'onHit', 'riscGain', 'Level', 'Invuln', 'Prorate']
# Special Case
striveSpecialCase = {
    'Reflect_Projectile':'F.D.B.'
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
def moveStriveImage(character, move):
    try:
        reqImg = requests.get(f'https://dustloop.com/wiki/index.php?title=File:GGST_{character}_{move}.png').text
        soupImg = BeautifulSoup(reqImg, 'html.parser')
        findRef = soupImg.find('div', {'id':'file'}, {'class':'fullImageLink'}).find('a').get('href')
        imgLink = f'https://dustloop.com{findRef}'
        print(f'This is the link: {imgLink}')
        return imgLink
    except AttributeError:
        print('Object not found')
        return ''
    #return findRef

def characterStriveImage(character):
    print(character)
    try:
        reqImg = requests.get(f'https://dustloop.com/wiki/index.php?title=File:GGST_{character}_Portrait.png').text
        soupImg = BeautifulSoup(reqImg, 'html.parser')
        findRef = soupImg.find('div', {'id':'file'}, {'class':'fullImageLink'}).find('a').get('href')
        imgLink = f'https://dustloop.com{findRef}'
        #print(f'This is the link: {imgLink}')
        return imgLink
    except AttributeError:
        print('Object not found')
        return ''
    #return findRef


def findStriveSystemData(character):
    r = requests.get(f'https://dustloop.com/wiki/index.php?title=GGST/{character}/Frame_Data').text
    soup = BeautifulSoup(r, 'html.parser')

    findTable = soup.find('table', {'class':'cargoTable'})
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
    characterInfoTable.append(striveCharacterTableHeader)
    characterInfoTable.append(infoTable)
    
    return characterInfoTable

# Perhaps have dictionary for throw names if it's just 'throw'
# need to do System data
def findStriveFrameData(character, moveName):
    r = requests.get(f'https://dustloop.com/wiki/index.php?title=GGST/{character}/Frame_Data').text

    # Beautiful Soup
    soup = BeautifulSoup(r, 'html.parser')
    #print(soup)
    #systemData = soup.find('table', {'class':'wikitable'}).text

    # Normal Moves Table
    normals = soup.find('table', {'class':'cargoDynamicTable'})
    # Trim excess information
    for extras in normals.find_all('td', {'class':'details-control'}):
        extras.decompose()


    # Specials Table
    specials = normals.find_next_sibling('table', {'class':'cargoDynamicTable'})
    # Trim excess information
    for extras in specials.find_all('td', {'class':'details-control'}):
        extras.decompose()


    # Supers Table
    supers = specials.find_next_sibling('table', {'class':'cargoDynamicTable'})
    # Trim excess information
    for extras in supers.find_all('td', {'class':'details-control'}):
        extras.decompose()


    # Throw Table
    other = supers.find_next_sibling('table', {'class':'cargoDynamicTable'})
    # Trim excess information
    for extras in other.find_all('td', {'class':'details-control'}):
        extras.decompose()
    

    # Place Normals into Normals List
    # Can probably combine these two for loops
    i = 0
    normalsList = []
    for td in normals.find_all('td'):
        normalsList.append(normals.find_all('td')[i].text)
        i+=1


    # Place special move data into specials list
    i = 0
    specialsList = []
    for td in specials.find_all('td'):
        specialsList.append(specials.find_all('td')[i].text)
        i+=1


    # Place supers into specials list
    i = 0
    for td in supers.find_all('td'):
        specialsList.append(supers.find_all('td')[i].text)
        i+=1


    # Place Other Data into list List
    i = 0
    for td in other.find_all('td'):
        normalsList.append(other.find_all('td')[i].text)
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

    # Specials and Supers have an extra column in the data table called name, messing up with the organization
    #['236S', 'Stun Edge', '30 [33]', 'All', '11', 'Until Hit', 'Total 54', '-17', '-14', '4', '2', 'none'], ['80%', 'DI 236S', 'Stun Edge', '30*
    # Format Normal Data into 1 Move 
    print(moveName)
    #print(normalsData)
    i = 0
    frameData = []
    for normal in normalsData:
        if normalsData[i][0] == moveName:
            frameData.append(striveNormalsTableHeader)
            frameData.append(normalsData[i])
            break
        i+=1
    if len(frameData) <= 0:
        i=0
        #print(len(specialsData))
        for special in specialsData:
            if specialsData[i][0] == moveName or specialsData[i][1] == moveName:
                frameData.append(striveSpecialsTableHeader)
                frameData.append(specialsData[i])
                break
            i+=1
    return frameData



#print(striveCharacters['ky'])
#print(moveStriveImage(striveCharacters['potemkin'],'Reflect Projectile'))
#print(moveStriveImage(striveCharacters['potemkin'],'c.S'))
#print(findNormalData(xrdCharacters['ky'],'5P'))
#print(findStriveFrameData(striveCharacters['ky'],'236K'))
#print(findStriveFrameData(striveCharacters['ky'],'c.S'))
#print(findStriveSystemData(striveCharacters['ky']))
#print(characterStriveImage(striveCharacters['ky']))

# DataTables_Table_0 - normals1
# DataTables_Table_1 - Specials
# DataTables_Table_2 - supers
# DataTables_Table_3 - other