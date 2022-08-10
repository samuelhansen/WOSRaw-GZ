
from pathlib import Path
from timeit import default_timer as timer
import dbgz
from tqdm.auto import tqdm
import WOSRaw as wos

# Path to the existing dbgz file
WOSArchivePath = Path("/gpfs/sciencegenome/WOS/WoS_2022_All.dbgz")


# Reading the file sequentially
with dbgz.DBGZReader(WOSArchivePath) as fd:
    # getting the number of entries
    print("\t Number of entries: ", fd.entriesCount)
    # getting the schema (currently UID and data)
    print("\t Scheme: ", fd.scheme)
    # TQDM can be used to print the progressbar
    for wosEntry in tqdm(fd.entries, total=fd.entriesCount):
        UID = wosEntry["UID"]
        entryData = wosEntry["data"] # XML records data
        wos.utilities.getTitle(wosEntry) # Extracting the title
        ... # do something with the data



