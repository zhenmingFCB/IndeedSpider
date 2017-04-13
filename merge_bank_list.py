import os
import csv

with open('BankList.csv', 'r') as indeedFile, open('../Over 5 Billion Master Bank List.csv', 'r') \
    as allBanksFile, open('BankList_new.csv','w') as newBanksFile:
    indeedReader = csv.DictReader(indeedFile)
    allReader = csv.DictReader(allBanksFile)

    fieldNames = ['Bank Name', 'Ticker', 'conml', 'Indeed Link', 'BHC_Folder_ID']
    writer = csv.DictWriter(newBanksFile,fieldNames)
    writer.writeheader()

    indeedBanks = {}
    for row in indeedReader:
        name = row['Bank Name']
        indeedBanks[str.lower(name)] = row

    indeedBankNames = indeedBanks.keys()
    for row in allReader:
        name = row['name']
        name = str.lower(name)
        conml = row['conml']
        folderId = row['BHC_Folder_ID']
        entry = {'Bank Name':name, 'Ticker':'', 'conml':conml, 'Indeed Link':'', 'BHC_Folder_ID':folderId}
        if str.lower(name) in indeedBankNames:
            print('Name matched: %s ' % name)
            entry['Ticker'] = indeedBanks[name]['Ticker']
            entry['Indeed Link'] = indeedBanks[name]['link']
            indeedBanks.pop(name)
            indeedBankNames.remove(name)
        writer.writerow(entry)

    for name,row in indeedBanks.items():
        entry = {'Bank Name':name, 'Ticker':row['Ticker'], 'conml':'', 'Indeed Link':row['link'], 'BHC_Folder_ID':''}
        writer.writerow(entry)
