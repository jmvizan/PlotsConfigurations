#!/bin/bash
#
echo "Purging " Datacards$1
#
rm -r Datacards$1/*/SR*
rm -r Datacards$1/*/*.txt
#

