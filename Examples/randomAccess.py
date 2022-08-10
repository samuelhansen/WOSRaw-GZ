
from pathlib import Path
from timeit import default_timer as timer
import dbgz
from tqdm.auto import tqdm
import random 
import WOSRaw as wos


# Path to the existing dbgz file
WOSArchivePath = Path("/gpfs/sciencegenome/WOS/WoS_2022_All.dbgz")

# Path to the generated index file
WOSIndexPath = Path("//home/filsilva/WOS/WoS_2022_All_byUID.idbgz")


print("Loading the index dictionary")
indexDictionary = dbgz.readIndicesDictionary(WOSIndexPath)

# Finding a specific entry using UID
wosUID = "WOS:000200919700142" # or any other UID
with dbgz.DBGZReader(WOSArchivePath) as fd:
    filePosition = indexDictionary[wosUID][0]
    wosEntry = fd.readAt(filePosition)[0] # only one entry per UID
    assert wosEntry["UID"] == wosUID # checking if the UID is correct
    title = wos.utilities.getTitle(wosEntry)
    ...


# Shuffling the keys to test accessing the entries randomly
keysShuffled = list(indexDictionary.keys())
random.shuffle(keysShuffled)
with dbgz.DBGZReader(WOSArchivePath) as fd:
    for wosUID in tqdm(keysShuffled):
        filePosition = indexDictionary[wosUID][0]
        wosEntry = fd.readAt(filePosition)
        assert wosEntry["UID"] == wosUID 

