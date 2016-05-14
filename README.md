# qmss2016
Repository for the QMSS2016 presentation

This repository contains files for preparing my presentation for the QMSS2016. These are:

* ipa.json - a JSON file mapping IPA symbols (including extendend symbols) to phonological descriptions and lists of 
distinctive features;
* piephono.txt - a TSV-like file with reflexes in some Indo-European languages (one per family) of original PIE-contexts; the 
data is an extremely simplified version of Mallory&Adams and Beekes
* process.phono.py - a simple python script to map the matrix of phonological reflexes above to a version using distinctive 
features
* piedata.csv - the result of process.phono.py processing
* csvtransp.py - an utility script to "transpose" a CSV file: `piedata.csv` is organized with contexts/features as rows, which 
is easier for humans to understand, but philogenetic analysis will work better with languages as observations

There are also file for preparing future work:

* extract.py - a simple scrapper to download cognate sets from Wikipedia
* pielex-1.txt - the output of extract.py

