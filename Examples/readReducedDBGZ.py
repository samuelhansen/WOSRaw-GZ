import dbgz
from pathlib import Path
from tqdm.auto import tqdm
import WOSRaw as wos
import ujson

WOSArchivePath = Path("//home/filsilva/WOS/WoS_2022_All.dbgz")


WOSReducedPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_dehydrated.dbgz")

with dbgz.DBGZReader(WOSReducedPath) as archive:
    for entry in tqdm(archive.entries,total=archive.entriesCount):
        print("Reading ID: ",entry["id"], end="\r")
        break
