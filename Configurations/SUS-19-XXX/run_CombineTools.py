#!/usr/bin/env python
import timeit
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools

# functions used in everyday life ...
from LatinoAnalysis.Tools.commonTools import *

COMBINE = os.getenv('COMBINE')
SUS19 = os.getenv('SUS19')
if(type(COMBINE) is None): COMBINE = " "
if(type(SUS19) is None): SUS19 = " "

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--outputDirDatacard' , dest='outputDirDatacard' , help='output directory'                          , default='./')   
    parser.add_option('--combineLocation'   , dest='combineLocation'   , help='Combine CMSSW Directory'                   , default=COMBINE)   
    parser.add_option('--combcfg'           , dest='combcfg'           , help='Combination dictionnary'                  , default='combineCards.py') 
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='Test')
    parser.add_option('--sigset'            , dest='sigset'            , help='Tag used for the sigset file name'           , default="")
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. \
Default: all'           , default="all")
    parser.add_option('--limits'            , dest='limits'            , help='Use higgs combine to calculate limits. Default=True'           , default=True)
    parser.add_option('--limrun'            , dest='limrun'            , help='Type of limit to be calculated. Default=blind'           , default='blind')
    

    parser.add_option('--test'              , dest='test'              , help='Run on test mode'           , default=False)
    parser.add_option('--sigmp'             , dest='signalMPcfg'      , help='Signal Mass Point cfg file'               , default='signalMassPoints.py')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()



    years=[]
    if opt.years =='2016':
        years=["2016"]
    elif opt.years == '2017':
        years=["2017"]
    else:
        years=["2016","2017","2018"]

    doTest=False
    if(opt.test=='True' or opt.test=='true' or opt.test=='T' or opt.test=='t'):
        doTest=True

    doLimits=False
    if(opt.limits=='True' or opt.limits=='true' or opt.limits=='T' or opt.limits=='t'):
        doLimits=True
    print "\n\t Optional arguments"
    print " tag                = ", opt.tag
    print " sigset             = ", opt.sigset
    print " Years              = ", years
    print " outputDirDatacard  = ", opt.outputDirDatacard
    print " combineLocation    = ", opt.combineLocation  
    print " Combination Cfg    = ", opt.combcfg
    print " Run on test mode   = ", doTest
    print " Calculate limits   = ", doLimits
    print "\n"

    if(doTest):
        print "On Test mode"
        opt.sigset="T2tt_mS-450_mX-350"

    # Create Needed dictionnary from other files
    variables = {}
    cuts = {}
    print "cuts file", opt.cutsFile
    if (os.path.exists(opt.variablesFile)):  exec(open(opt.variablesFile).read())
    if (os.path.exists(opt.cutsFile))     :  exec(open(opt.cutsFile).read())
    if (os.path.exists(opt.signalMPcfg))  :  exec(open(opt.signalMPcfg).read())
    cmsenv=' eval `scramv1 runtime -sh` '
    dirDC=''
    tagDC=''
    combCommand=opt.combcfg+' '
    #Loop over Signal mass points year cuts and variables, to get all Datacards
    for model in signalMassPoints:
        print "Model:", model,"\tSignal set", opt.sigset
        if model not in opt.sigset:  continue
        for massPoint in signalMassPoints[model]:
            #print opt.sigset, "<-sigset, masspoint->", massPoint
            if opt.sigset not in massPoint:  continue
            print "Mass Point:", massPoint
            for year in years:
                for cut in cuts: 
                    for variable in variables:
                        thisDC=year+'/'+massPoint+'/'+cut+'/'+variable+"/datacard.txt  "
                        tagDC =cut #Could be changed to more complex in the future
                        dirDC+=tagDC+'=./Datacards/'+thisDC
                        print "Datacard: ", thisDC
    finalDC='allDC.txt'
    #Actually combine the DC
    doCombcmsenv='cd '+opt.combineLocation+ ';'+cmsenv+'; cd -; '
    if(doTest is False):
        combCommand+=dirDC+">"+finalDC
        print "Combining Datacards:"
        os.system(doCombcmsenv+combCommand)
        print "Final Datacard:", finalDC
    else:
        print "In test. Thus,  no DC combination is done"
    #Calculate the limits
    if(doLimits is True):
        combCommand='combine -M AsymptoticLimits --run '+opt.limrun +' ' +finalDC+' -n allDC'+opt.limrun
        print "sending combination", combCommand
        os.system(doCombcmsenv+combCommand)
    else:
        print "Limit option set to false: no limits were calculated"
