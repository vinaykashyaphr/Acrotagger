import os
import pathlib
import shutil
import subprocess
import sys

from lxml import etree
from tqdm import tqdm

from common_functions import Exclusion
from validateEntities import valent


class AcroLauncher():

    def __init__(self, app_path: pathlib.Path, dirpath: pathlib.Path, allfiles: list, choice: str):
        ALZ, ALL, AC, XALL = [], [], [], []
        k = 0
        for all in allfiles:
            if (all.startswith('DMC-HON')) and (all.endswith('.xml') or all.endswith('.XML')):
                ALL.append(all)
                XALL.append(all)
                k = k+1
                if k == 4:
                    ALZ.append(list(ALL))
                    ALL.clear()
                    k = 0

        for file in tqdm(allfiles, desc="Making files ready"):
            if (file.startswith('DMC-HON')) and (file.endswith('.xml') or file.endswith('.XML')):
                par = etree.XMLParser(no_network=True, recover=True)
                acrodm = valent(file, dirpath)
                acroroot = etree.parse(acrodm, par).getroot()
                acrotable = acroroot.find('.//table')
                if acrotable != None:
                    acrotabtitle = acrotable.find('.//title')
                    if acrotabtitle != None:
                        acrotabtxt = acrotabtitle.text
                        if acrotabtxt == 'List of Acronyms and Abbreviations':
                            AC.append(acrodm)
                            break

        AITM = [item for sublist in ALZ for item in sublist]
        uncommon = list(set(AITM) ^ set(XALL))
        [ALZ.append(uncommon) if uncommon != [] else None]
        mainfolder = dirpath.parent.joinpath('acro_output')
        self.build_dir(mainfolder)

        for group in ALZ:
            tempfolder = dirpath.parent.joinpath('temp_folder')
            self.build_dir(tempfolder)
            group = list(dict.fromkeys(group + AC))
            [shutil.copy(each, tempfolder) for each in group]
            subprocess.call('{0} "{1}" "{2}"'.format(
                app_path.joinpath(r"tagger\acrotagger.exe"), tempfolder, choice))
            [shutil.copy(tempfolder.joinpath(file), mainfolder)
             for file in group]
            shutil.rmtree(tempfolder)

        [shutil.copy(mainfolder.joinpath(item), dirpath)
         for item in os.listdir(mainfolder)]
        shutil.rmtree(mainfolder)

    def build_dir(self, folderpath: pathlib.WindowsPath):
        if not os.path.isdir(folderpath):
            folderpath.mkdir()
        else:
            shutil.rmtree(folderpath)
            folderpath.mkdir()
        return


current_loc = pathlib.Path(os.getcwd())
mainpath = pathlib.Path(sys.argv[1])
choice = sys.argv[2]
files_list = Exclusion().parsable_list(mainpath)
os.chdir(mainpath)

AcroLauncher(current_loc, mainpath, files_list, choice)
