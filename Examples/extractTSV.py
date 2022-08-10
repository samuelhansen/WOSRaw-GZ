import dbgz
from pathlib import Path
from tqdm.auto import tqdm
import WOSRaw as wos
import ujson

WOSArchivePath = Path("//home/filsilva/WOS/WoS_2022_All.dbgz")



WOSTSVPath = Path("/gpfs/sciencegenome/WOS/WoS_2022.tsv")
WOSTSVExtraDataPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_extra.tsv")
WOSTSVAbstractPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_abstract.tsv")
WOSTSVReferencesPath = Path("/gpfs/sciencegenome/WOS/WoS_2022_references.tsv")



tsvFile = open(WOSTSVPath, "wt")
tsvExtraDataFile = open(WOSTSVExtraDataPath, "wt")
tsvAbstractFile = open(WOSTSVAbstractPath, "wt")
tsvReferencesFile = open(WOSTSVReferencesPath, "wt")


def parseEntry(entry):
    if(isinstance(entry,list)):
        return "; ".join([v.replace(";",",.") for v in entry]).replace("\t","    ")
    else:
        return entry.replace("\t","    ")

header=True
with dbgz.DBGZReader(WOSArchivePath) as fd:
    for wosEntry in tqdm(fd.entries, total=fd.entriesCount):
        fieldsData = wos.utilities.getAllFields(wosEntry)
        if(header):
            tsvFields = [key for key in fieldsData.keys() if len(key)==2 and key!="AB"]
            extraFields = ["UT"]+[key for key in fieldsData.keys() if len(key)==3 and key!="AB"]
            abstractFields = ["UT","AB"]
            referencesFields = ["Citing","Cited"]
            tsvFile.write("\t".join(tsvFields)+"\n")
            tsvExtraDataFile.write("\t".join(extraFields)+"\n")
            tsvAbstractFile.write("\t".join(abstractFields)+"\n")
            tsvReferencesFile.write("\t".join(referencesFields)+"\n")
            header=False
        tsvLine = "\t".join([parseEntry(fieldsData[key]) for key in tsvFields]).replace("\n","  ")+"\n"
        tsvFile.write(tsvLine)
        tsvExtraDataLine = "\t".join([ujson.dumps(fieldsData[key]) for key in extraFields]).replace("\n","  ")+"\n"
        tsvExtraDataFile.write(tsvExtraDataLine)
        tsvAbstractLine = "\t".join([parseEntry(fieldsData[key]) for key in abstractFields]).replace("\n","  ")+"\n"
        tsvAbstractFile.write(tsvAbstractLine)
        fromUID = fieldsData["UT"]
        for toUID in fieldsData["CI"]:
            if(toUID):
                tsvReferencesLine = fromUID+"\t"+toUID+"\n"
                tsvReferencesFile.write(tsvReferencesLine)
        
            





# Closing files
tsvFile.close()
tsvExtraDataFile.close()
tsvAbstractFile.close()
tsvReferencesFile.close()
