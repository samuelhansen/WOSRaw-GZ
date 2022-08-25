import dbgz
from pathlib import Path
from tqdm.auto import tqdm
import WOSRaw as wos
import ujson

WOSArchivePath = Path("//home/filsilva/WOS/WoS_2022_All.dbgz")


WOSReducedPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_dehydrated.dbgz")
WOSReducedAbstractPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_abstract.dbgz")

errorFilePath = Path("errors.log")

reducedSchemaDictionary = wos.utilities.getScheme(invalid={"AB"})
abstractSchemaDictionary = wos.utilities.getScheme(valid={"UT","AB"})

DBGZReducedFile = dbgz.DBGZWriter(WOSReducedPath,list(reducedSchemaDictionary.values()))
DBGZReducedAbstractFile = dbgz.DBGZWriter(WOSReducedAbstractPath, list(abstractSchemaDictionary.values()))
errorFile = open(errorFilePath, "wt", encoding="utf-8")



with dbgz.DBGZReader(WOSArchivePath) as fd:
    for wosEntry in tqdm(fd.entries, total=fd.entriesCount):
        try:
            fieldsData = wos.utilities.getAllFields(wosEntry)
            reducedData = {propertyName:fieldsData[key] for key,(propertyName,_) in reducedSchemaDictionary.items()}
            abstractData = {propertyName:fieldsData[key] for key,(propertyName,_) in abstractSchemaDictionary.items()}
            DBGZReducedFile.write(**reducedData)
            DBGZReducedAbstractFile.write(**abstractData)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(str(e))
            errorFile.write(str(wosEntry["UID"])+"\t"+str(e).replace("\n","  ")+"\n")



# Closing files
DBGZReducedFile.close()
DBGZReducedAbstractFile.close()
errorFile.close()
