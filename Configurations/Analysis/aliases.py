##### aliases = {}

import os

includePath = 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE')
aliasDir = os.getenv('PWD')+'/aliases'

