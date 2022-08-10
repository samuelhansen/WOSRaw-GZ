
import WOSRaw as wos
from pathlib import Path

# Path where to save the WoS dbgz archive
WOSArchivePath = Path("/gpfs/sciencegenome/WOS/WoS_2022_All.dbgz")

# Path to the generated 
WOSIndexPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_All_byUID.idbgz")

# This may take several hours to complete
wos.archive.createIndexByUID(WOSArchivePath, WOSIndexPath)


