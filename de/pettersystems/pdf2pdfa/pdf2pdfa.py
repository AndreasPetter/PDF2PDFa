import subprocess
import os
import sys
import re
from shutil import copyfile

jhoveExec = 'jhove'

if len(sys.argv) < 3:
    print("Usage pdf2pdfa: pdf2pdfa <input-directory> <output-directory>\n")
    sys.exit(1)

def renameUppercasePDFs():
    # rename pdf files to lowercase ending
    for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
        for file in [f for f in filenames if f.lower().endswith("pdf") and (f[-4:].lower() != f[-4:])]:
            actualFile = dirpath + file
            if dirpath[-1:] != '/':
                actualFile = dirpath + '/' + file
            newFileName = actualFile[:-4] + actualFile[-4:].lower()
            print("WARNING: Renaming file: " + actualFile + " to " + newFileName + " because we need lowercase pdf ending!")
            os.rename(actualFile, newFileName)

def checkOutputFromJHove(actualFile):
    outputLines = subprocess.check_output([jhoveExec, actualFile]).decode("utf-8").splitlines()
    result = False
    for line in [l for l in outputLines if re.match('^\s*Profile:', l)]:
        if 'PDF/A' not in line:
            print('WARNING: Unexpected profile information. Assuming the file to be in format different from PDF/A')
        else:
            result = True
    return result

def convertPDF2PDFA(sourceFile, targetFile):
    pass


def checkAndTransformFiles():
    targetDir = sys.argv[2]
    if targetDir[-1:] != '/':
        targetDir = targetDir + '/'
    sourceDir = sys.argv[1]
    if sourceDir[-1:] != '/':
        sourceDir = sourceDir + '/'

    for dirpath, dirnames, filenames in os.walk(sourceDir):
        for file in [f for f in filenames if f.upper().endswith("PDF")]:
            actualFile = dirpath + file
            if dirpath[-1:] != '/':
                actualFile = dirpath + '/' + file
            targetFileName = targetDir + re.sub('^' + sourceDir, '', actualFile)

            # check that target file does not exist
            if not os.path.isfile(targetFileName):
                # execute PDF/a checker
                isPDFA = checkOutputFromJHove(actualFile)

                # must create target directory if it does not exist...
                os.makedirs(os.path.dirname(targetFileName), exist_ok=True)
                #print ( targetFileName )
                if isPDFA:
                    # copy file
                    copyfile(actualFile, targetFileName)
                    print("Copied " + actualFile + " because it did not exist in the target directory but already was in PDF/A format.")
                else:
                    # invoke pdf conversion to pdf/a
                    convertPDF2PDFA(actualFile, targetFileName)
                    print("Converted " + actualFile + " because it did not exist in the target directory but was not in PDF/A format.")
            else:
                print ( 'Skipping ' + targetFileName + ' because it already exists.')

print("Renaming files, if necessary...")
renameUppercasePDFs()

print('If not existing in target dir, transform files from PDF to PDFa, if necessary, copy otherwise')
checkAndTransformFiles()