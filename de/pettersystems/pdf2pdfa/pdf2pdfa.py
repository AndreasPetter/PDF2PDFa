import subprocess
import os
import sys
import re
from shutil import copyfile

jhoveExec = 'jhove'
ghostScriptExec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-sProcessColorModel=DeviceCMYK',
                   '-sDEVICE=pdfwrite', '-sPDFACompatibilityPolicy=1']

# check call of this script
if len(sys.argv) < 3:
    print("Usage pdf2pdfa: pdf2pdfa <input-directory> <output-directory>\n")
    sys.exit(1)

# rename pdf files to lowercase ending
def renameUppercasePDFs():
    for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
        for file in [f for f in filenames if f.lower().endswith("pdf") and (f[-4:].lower() != f[-4:])]:
            actualFile = dirpath + file
            if dirpath[-1:] != '/':
                actualFile = dirpath + '/' + file
            newFileName = actualFile[:-4] + actualFile[-4:].lower()
            print("WARNING: Renaming file: " + actualFile + " to " + newFileName + " because we need lowercase pdf ending!")
            os.rename(actualFile, newFileName)

# check if a file is already in pdf/a format. Path to file is absolute.
def checkOutputFromJHove(actualFile):
    outputLines = subprocess.check_output([jhoveExec, actualFile]).decode("utf-8").splitlines()
    result = False
    for line in [l for l in outputLines if re.match('^\s*Profile:', l)]:
        if 'PDF/A' not in line:
            print('WARNING: Unexpected profile information. Assuming the file to be in format different from PDF/A')
        else:
            result = True
    return result

# convert pdf to pdf/a
def convertPDF2PDFA(sourceFile, targetFile):
    # because of a ghostscript bug, which does not allow parameters that are longer than 255 characters
    # we need to perform a directory changes, before we can actually return from the method
    cwd = os.getcwd()
    os.chdir(os.path.dirname(targetFile))
    try:
        subprocess.check_output(ghostScriptExec +
                            ['-sOutputFile=' + os.path.basename(targetFile) , sourceFile])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    os.chdir(cwd)

# walk through directory tree and...
#    1. check that the files are not already in the target directory
#       if that file does not exist... (otherwise we are done for that file)
#       1.1 check if the source file is in pdf/a format
#           1.1.1 yes: just copy file to target dir
#           1.1.2 no: convert pdf file to pdf/a and store it in target directory
def checkAndTransformFiles():
    # fix directory ending to always contain a /
    targetDir = sys.argv[2]
    if targetDir[-1:] != '/':
        targetDir = targetDir + '/'
    sourceDir = sys.argv[1]
    if sourceDir[-1:] != '/':
        sourceDir = sourceDir + '/'

    # walk through directory tree
    for dirpath, dirnames, filenames in os.walk(sourceDir):
        for file in [f for f in filenames if f.upper().endswith("PDF")]:
            # normalize input file name to contain a / on correct position
            actualFile = dirpath + file
            if dirpath[-1:] != '/':
                actualFile = dirpath + '/' + file
            targetFileName = targetDir + re.sub('^' + sourceDir, '', actualFile)

            # 1. check that target file does not exist
            if not os.path.isfile(targetFileName):
                # 1.1 execute PDF/a checker
                isPDFA = checkOutputFromJHove(actualFile)

                # must create target directory if it does not exist...
                os.makedirs(os.path.dirname(targetFileName), exist_ok=True)

                if isPDFA:
                    # 1.1.1 copy file
                    copyfile(actualFile, targetFileName)
                    print("Copied " + actualFile + " because it did not exist in the target directory but already was in PDF/A format.")
                else:
                    # 1.1.2 invoke pdf conversion to pdf/a
                    convertPDF2PDFA(actualFile, targetFileName)
                    print("Converted " + actualFile + " because it did not exist in the target directory but was not in PDF/A format.")
            else:
                # print ( 'Skipping ' + targetFileName + ' because it already exists.')
                pass




print("Renaming files, if necessary...")
renameUppercasePDFs()

print('If not existing in target dir, transform files from PDF to PDFa, if necessary, copy otherwise')
checkAndTransformFiles()