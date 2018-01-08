PDF to PDF/A directory conversion tool
======================================

This tool helps converting a directory tree structure of PDF files into
an output tree structure consisting of PDF/A files. These have several 
properties which are good for long term storage, detecting file changes,
etc. It is also useful to try to fullfil legal properties for long term
storage of invoices in Germany (destroying the original paper version), 
which may reside in PDF/A format. I, as a freelancer, use it for achieving
a paperless office.

However, I cannot guarentee that files are in correct format using this
tool. To be save you must check your files using a PDF/A validator.

Installation
------------

The software has been tested under Linux. You can help testing the software
using different operating systems and providing feedback to me.
The following packages must be installed prior to running the software:
  * python3
  * jhove
  * ghostscript

You can install this software using your favourite package manager, e.g. 
for Ubuntu this will essentially boil down to: 
`sudo apt-get install python3 jhove ghostscript`

The python file `pdf2pdfa.py` can be copied to an arbitrary directory. 

Running
-------

The software is run similar to any other python3 software:
`python3 pdf2pdfa.py <INPUT-DIRECTORY-TREE> <OUTPUT-DIRECTORY-TREE>`

The first parameter is the input path containing the PDF-files used as
input to the process. The second parameter is the archive path where
converted and ready PDF/A files shall reside in.

License
-------
Apache Software License v2.0 applies as long as this is allowed.
Since the software is dependent on ghostscript it might be subject to GPLv2.

In any case... the software is provided as is and without any liabilities
or warranties whatsoever. It is possible - though unlikely - that due to 
some strange things I could not forsee (and never happened yet) harmful 
things happen like that you might loose your data or destroy anything on 
this world. Btw. this is the case for any software that has not undergone
a formal verification process... Some software seem to predestenid for these
sort of things (but not this one).

You can use it for free for any purpose you want except harming other 
people. Any useless legal pain in the ass will be rejected promptly.

Consulting
----------
If you need any consulting services for this software (new features, etc.)
please feel free to contact me.

