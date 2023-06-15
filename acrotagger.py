import os
import pathlib
import re
import sys
import time

from lxml import etree
from tqdm import tqdm

from common_functions import Exclusion, Write_DMC
from validateEntities import valent


class AcronymTagging():
    def __init__(self, dirpath, allfiles, option):
        ACR = {}
        ACF = []

        print('\n')
        for file in tqdm(allfiles, desc="Finding acronym table"):
            print('\n', file)
            if (file.startswith('DMC-HON')) and (file.endswith('.xml') or file.endswith('.XML')):
                acrodm = valent(file, dirpath)
                dmcparser = etree.XMLParser(no_network=True, recover=True)
                acroroot = etree.parse(acrodm, dmcparser).getroot()
                acrotable = acroroot.find('.//table')
                if acrotable != None:
                    acrotabtitle = acrotable.find('.//title')
                    if acrotabtitle != None:
                        acrotabtxt = acrotabtitle.text
                        if acrotabtxt == 'List of Acronyms and Abbreviations':
                            ACF.append(acrodm)
                            print('\nFound ACRONYMS at {0}'.format(acrodm))
                            acrobody = acrotable.find('.//tbody')
                            acrorow = acrobody.findall('.//row')
                            for ro in acrorow:
                                abbr = ro.find('entry[1]/para').text
                                expansion = ro.find('entry[2]/para').text
                                if abbr.isupper() == True:
                                    ACR.update({abbr: expansion})
                            break
        if option == True:
            self.remove_acronyms(allfiles, ACF, dirpath)
            self.tag_acronyms(allfiles, ACR, ACF, dirpath)
        else:
            self.remove_acronyms(allfiles, ACF, dirpath)

    def remove_acronyms(self, allfiles, ACF, dirpath):
        print('\n')
        for each in tqdm(allfiles, desc="Removing previous acronyms"):
            print('\n', each)
            if (each.startswith('DMC-HON')) and (each.endswith('.xml') or each.endswith('.XML')):
                if each != ACF[0]:
                    xeach = valent(each, dirpath)
                    par = etree.XMLParser(no_network=True, recover=True)
                    dmroot = etree.parse(xeach, par).getroot()
                    self.del_preacro(dmroot)
                    Write_DMC(dmroot, each, dirpath)

    def tag_acronyms(self, allfiles, ACR, ACF, dirpath):
        print('\n')
        for f in allfiles:
            for ix, acr in enumerate(ACR):
                if (f.startswith('DMC-HON')) and (f.endswith('.xml') or f.endswith('.XML')):
                    if f != ACF[0]:
                        f = valent(f, dirpath)
                        xmlpar = etree.XMLParser(no_network=True, recover=True)
                        froot = etree.parse(f, xmlpar).getroot()
                        fcont = froot.findall('.//content')
                        paralist = fcont[0].xpath(
                            './/*[self::para or self::note]')
                        acr_count = []
                        for para in paralist:
                            textpara = etree.tostring(para).decode()
                            acrcompile = re.compile(
                                r'\b{0}\b'.format(re.escape(acr).upper()))
                            acrfind = re.findall(acrcompile, textpara)
                            acr_count.append(len(acrfind))
                            if acrfind != []:
                                for aix, abbr in enumerate(acrfind):
                                    textpara = re.sub(
                                        acrcompile, '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"), textpara)
                                    #textpara = str(textpara).replace(abbr, '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"))
                                    #text0 = re.sub(acrcompile, '<acronym id="acro-{0}"><acronymTerm>{1}</acronymTerm><acronymDefinition>{2}</acronymDefinition></acronym>'.format(f"{int(ix+1):04}", acr, ACR[acr]), textpara)
                                    if aix == (len(acrfind)-1):
                                        self.acro_replace(
                                            textpara, abbr, para, ix)
                        remtheadlist = fcont[0].findall(
                            './/thead//acronymTerm')
                        for remthead in remtheadlist:
                            remthead.tail = acr + remthead.tail if remthead.tail else acr
                            etree.strip_elements(
                                remthead.getparent(), 'acronymTerm', with_tail=False)
                        refcontxt = str(etree.tostring(fcont[0]).decode())
                        refcont = refcontxt.replace('<acronymTerm internalRefId="acro-{0}"/>'.format(
                            f"{int(ix+1):04}"), '<acronym id="acro-{0}"><acronymTerm>{1}</acronymTerm><acronymDefinition>{2}</acronymDefinition></acronym>'.format(f"{int(ix+1):04}", acr, ACR[acr]), 1)
                        refcont = refcont.replace('<acronymTerm internalRefId="acro-{0}"/>'.format(
                            f"{int(ix+1):04}"), '<acronymTerm internalRefId="acro-{0}">{1}</acronymTerm>'.format(f"{int(ix+1):04}", acr))
                        new_cont = etree.fromstring(refcont)
                        fcont[0].addnext(new_cont)
                        fcont[0].getparent().remove(fcont[0])
                        print('\n '+f+' :: '+str(sum(acr_count))+' - '+acr)
                        Write_DMC(froot, f, dirpath)

    def del_preacro(self, dmroot):
        X = []
        dmainlist = dmroot.xpath(
            './/content//*[self::description or self::procedure]')
        if dmainlist != []:
            dmain = dmainlist[0]
            preacrolist = dmain.findall('.//acronym/[acronymTerm]')
            if preacrolist != []:
                for ip, preacro in enumerate(preacrolist):
                    preacroname = preacro.xpath('acronymTerm/text()')

                    preacro.tail = preacroname[0] + \
                        preacro.tail if preacro.tail else preacroname[0]
                    preacro.tail = str(preacro.tail).replace(
                        '\n', ' ').replace('\t', ' ')
                    X.append(str(preacroname[0]).replace(
                        '\n', '').replace('\t', ''))
                    #print(preacro, preacro.tail)

                    if ip == len(preacrolist)-1:
                        WID = {}
                        withidlist = dmain.findall('.//acronym/[@id]')

                        if withidlist != []:
                            for withid in withidlist:
                                l_widtext = withid.xpath('acronymTerm/text()')
                                for widtext in l_widtext:
                                    widtext = str(widtext).replace(
                                        '\n', '').replace('\t', '')
                                    WID.update({widtext: withid.attrib['id']})

                        if WID != {}:
                            for tx in WID:
                                for x in list(dict.fromkeys(X)):
                                    if tx == x:
                                        l_xwidref = dmain.findall(
                                            './/acronymTerm/[@internalRefId="{0}"]'.format(WID[tx]))
                                        for xwidref in l_xwidref:
                                            xwidref.tail = tx + xwidref.tail if xwidref.tail else tx

                etree.strip_elements(dmain, 'acronym', with_tail=False)
                etree.strip_elements(dmain, 'acronymTerm', with_tail=False)

    def acro_replace(self, textpara, abbr, para, ix):
        try:
            new_para = etree.fromstring(textpara)
        except etree.XMLSyntaxError:
            time.sleep(0.01)
            textpara2 = textpara.replace(
                '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"), abbr)
            parax = etree.fromstring(textpara2)
            parax.text = str(parax.text).replace(
                abbr, '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"))
            l_sub_parax = parax.findall('.//*')
            for sub_parax in l_sub_parax:
                time.sleep(0.01)
                if sub_parax.tail != None:
                    sub_parax.tail = str(sub_parax.tail).replace(
                        abbr, '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"))
            xnew_para = etree.tostring(parax).decode()
            xnew_para2 = str(xnew_para).replace('&lt;acronymTerm internalRefId="acro-{0}"/&gt;'.format(
                f"{int(ix+1):04}"), '<acronymTerm internalRefId="acro-{0}"/>'.format(f"{int(ix+1):04}"))
            new_para = etree.fromstring(xnew_para2)
        para.addnext(new_para)
        para.getparent().remove(para)


def choose_bool(user_ip):
    if user_ip == 1:
        bool_ip = True
    else:
        bool_ip = False
    return bool_ip


folderpath = pathlib.Path(sys.argv[1])
files_list = Exclusion().parsable_list(folderpath)
input_choice = int(sys.argv[2])
os.chdir(folderpath)
boolean_input = choose_bool(input_choice)
AcronymTagging(folderpath, files_list, boolean_input)
