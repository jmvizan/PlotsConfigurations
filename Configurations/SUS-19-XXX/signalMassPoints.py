signalMassPoints = {}

def massPointPass(massPoint, sigSetItem):

    if sigSetItem.count('_')==0:
        if sigSetItem in massPoint:
            return True

    for model in signalMassPoints:
        if model in sigSetItem:

            massPointTerms = massPoint.split('_')
            
            sigSetItem = sigSetItem.replace(model+'_', '')
            signalSetConditions = sigSetItem.split('_')

            for condition in signalSetConditions:

                conditionApplied = False

                if 'dm-' in condition:
                    
                    deltaMass = float(massPointTerms[1].split('-')[1]) - float(massPointTerms[2].split('-')[1]) 

                    if 'to' not in condition:
                        if deltaMass!=float(condition.split('-')[1]):
                            return False
                    else:
                        massRange = condition.split('-')[1]
                        if deltaMass<float(massRange.split('to')[0]) or deltaMass>float(massRange.split('to')[1]):
                            return False

                    conditionApplied = True

                elif 'to' not in condition:

                    if condition!=massPointTerms[1] and condition!=massPointTerms[2]:
                        return False

                    conditionApplied = True

                else:
                    
                    massFlag = condition.split('-')[0] + '-'
                    massRange = condition.split('-')[1]

                    for massPointTerm in massPointTerms:
                        if massFlag in massPointTerm:

                            massPointTermValue = float(massPointTerm.replace(massFlag, ''))
                            
                            lowerMass  = float(massRange.split('to')[0]) 
                            higherMass = float(massRange.split('to')[1])
                            
                            if massPointTermValue<lowerMass or massPointTermValue>higherMass:
                                return False
                                
                            conditionApplied = True

                if conditionApplied==False:
                    return False

            return True

    # No known model found in sigSetItem
    return False

def massPointInSignalSet(massPoint, sigSet):

    signalSet = sigSet.replace('SM-', '')
    signalSet = signalSet.replace('Backgrounds-', '')
    signalSet = signalSet.replace('Data-', '')

    sigSetList = signalSet.split(',')

    if massPoint in sigSetList:
        return True

    for sigSetItem in sigSetList:

        if massPointPass(massPoint, sigSetItem):
            return True

    return False

signalMassPoints['T2tt'] = {}

for mStop in range( 150,  2001, 25):
    datasetName = 'T2tt__mStop-'
    if mStop<=250:
        datasetName += '150to250'
    elif mStop<350:
        datasetName += '250to350'
    elif mStop<=400:
        datasetName += '350to400'
    elif mStop<=1200:
        datasetName += '400to1200'
    elif mStop<=2000:
        datasetName += '1200to2000'
    else :
        print 'Squark top mass', mStop, 'not available'
    for mNeutralino in range( 0,  min(mStop-74, 1151), 25):
            
        if (mStop-mNeutralino>300 and (mStop%50!=0 or mNeutralino%50!=0)):
            continue
            
        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
        if mStop-mLSP==75: mLSP = mStop - 87 
            
        massPointName = 'T2tt' + '_mS-' + str(mStop) + '_mX-' + str(mLSP)
        massPointCut = '(susyMstop>=' + str(mStop) + '-4 && susyMstop<=' + str(mStop) + '+4 && susyMLSP>=' + str(mLSP) + '-2 && susyMLSP<=' + str(mLSP) + '+2)'

        massPoint = {}
        massPoint['massPointDataset'] = datasetName
        massPoint['massPointCut'] = massPointCut

        signalMassPoints['T2tt'][massPointName] = massPoint

signalMassPoints['T2bW'] = {}

for mStop in range( 200,  1501, 25):
    datasetName = 'T2bW'
    for mNeutralino in range( 0,  min(mStop-174, 651), 25):
            
        if (mStop%50!=0 or mNeutralino%50!=0):
            skipPoint = True
            if (mStop>=400 and mNeutralino>=150 and mStop-mNeutralino<=300):
                skipPoint = False
            if (mStop>=400 and mNeutralino==25):
                skipPoint = False
            if (mStop<400 and mStop%50==0 and mStop-mNeutralino==175):
                skipPoint = False
            if skipPoint==True:
                continue
            
        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
            
        massPointName = 'T2bW' + '_mS-' + str(mStop) + '_mX-' + str(mLSP)
        massPointCut = '(susyMstop>=' + str(mStop) + '-4 && susyMstop<=' + str(mStop) + '+4 && susyMLSP>=' + str(mLSP) + '-2 && susyMLSP<=' + str(mLSP) + '+2)'

        massPoint = {}
        massPoint['massPointDataset'] = datasetName
        massPoint['massPointCut'] = massPointCut

        signalMassPoints['T2bW'][massPointName] = massPoint

signalMassPoints['TChipmSlepSnu'] = {}

for mChipm in range( 100,  1501, 25):
    datasetName = 'TChipmSlepSnu'
    if mChipm>800:
        datasetName += '_mC1_825_1500'
    for mNeutralino in range( 0,  min(mChipm-49, 901), 25):
            
        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
            
        massPointName = 'TChipmSlepSnu' + '_mC-' + str(mChipm) + '_mX-' + str(mLSP)
        massPointCut = '(susyMChargino>=' + str(mChipm) + '-4 && susyMChargino<=' + str(mChipm) + '+4 && susyMLSP>=' + str(mLSP) + '-2 && susyMLSP<=' + str(mLSP) + '+2)'

        massPoint = {}
        massPoint['massPointDataset'] = datasetName
        massPoint['massPointCut'] = massPointCut

        signalMassPoints['TChipmSlepSnu'][massPointName] = massPoint

signalMassPoints['TChipmWW'] = {}

for mChipm in range( 100,  851, 25):
    datasetName = 'TChipmWW'
    for mNeutralino in range( 0,  min(mChipm-9, 601), 5):
            
        if ((mChipm-mNeutralino<=100 and (mChipm-mNeutralino)%10==0) or 
            (mChipm-mNeutralino> 100 and mNeutralino%25==0)):

            mLSP = mNeutralino
            if mLSP==0: mLSP = 1
            
            massPointName = 'TChipmWW' + '_mC-' + str(mChipm) + '_mX-' + str(mLSP)
            massPointCut = '(susyMChargino>=' + str(mChipm) + '-4 && susyMChargino<=' + str(mChipm) + '+4 && susyMLSP>=' + str(mLSP) + '-2 && susyMLSP<=' + str(mLSP) + '+2)'

            massPoint = {}
            massPoint['massPointDataset'] = datasetName
            massPoint['massPointCut'] = massPointCut

            signalMassPoints['TChipmWW'][massPointName] = massPoint

signalMassPoints['TSlepSlep']   = {}
signalMassPoints['TSlepSlepLH'] = {}
signalMassPoints['TSeleSeleLH'] = {}
signalMassPoints['TSmuoSmuoLH'] = {}
signalMassPoints['TSlepSlepRH'] = {}
signalMassPoints['TSeleSeleRH'] = {}
signalMassPoints['TSmuoSmuoRH'] = {}

import math
from LatinoAnalysis.NanoGardener.framework.samples.susyCrossSections import SUSYCrossSections
def getTSlepSlepCrossSection(susyModel, susyMass):

    susyProcess = susyModel.replace('TSelectronSelectron', 'Slepton').replace('TSmuonSmuon', 'Slepton')

    isusyMass = int(susyMass)

    if str(isusyMass) in SUSYCrossSections[susyProcess]['massPoints'].keys() :

        return float(SUSYCrossSections[susyProcess]['massPoints'][str(isusyMass)]['value'])

    else: # Try to extrapolate

        if isusyMass<=400: step = 20
        elif isusyMass<=440: step = 40
        elif isusyMass<=500: step = 60
        elif isusyMass<=1000: step = 100
        else: step = -1

        isusyMass1 = step*(isusyMass/step)
        isusyMass2 = step*(isusyMass/step+1)

        if step==60:
            isusyMass1 =  440
            isusyMass2 =  500
        elif isusyMass>1000:
            isusyMass1 =  900
            isusyMass2 = 1000

        if str(isusyMass1) in SUSYCrossSections[susyProcess]['massPoints'].keys() and str(isusyMass2) in SUSYCrossSections[susyProcess]['massPoints'].keys() :

            susyXsec1 = float(SUSYCrossSections[susyProcess]['massPoints'][str(isusyMass1)]['value'])
            susyXsec2 = float(SUSYCrossSections[susyProcess]['massPoints'][str(isusyMass2)]['value'])

            slope = -math.log(susyXsec2/susyXsec1)/(isusyMass2-isusyMass1)
            return susyXsec1*math.exp(-slope*(isusyMass-isusyMass1))

    print 'getCrossSection ERROR: cross section not available for', susyProcess, 'at mass =', susyMass, ', exiting'
    exit()

for mSlep in range( 100, 1301, 25):
    datasetName = 'TSlepSlep'
    lspStep = 10
    if mSlep>450:
        if mSlep%50!=0:
            continue
        datasetName = 'TSlepSlep_mSlep-500to1300'
        lspStep = 25
    mNeutralinoList = [ ] 
    mNeutralinoList.extend(range( 0,  min(mSlep-40+1, 651), lspStep))
    for dm in [1,5,10,20,30,40]:
        if mSlep-dm<=650 and (dm<40 or mSlep>=500):
            mNeutralinoList.append(mSlep-dm)
    for mNeutralino in mNeutralinoList:

        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
            
        massPointName = '_mS-' + str(mSlep) + '_mX-' + str(mLSP)
        massPointCut = 'susyMSlepton>=' + str(mSlep) + '-4 && susyMSlepton<=' + str(mSlep) + '+4 && susyMLSP>=' + str(mLSP) + '-2 && susyMLSP<=' + str(mLSP) + '+2'

        xSecSlepLH = str(getTSlepSlepCrossSection('TSelectronSelectronLH', str(mSlep)))
        xSecSlepRH = str(getTSlepSlepCrossSection('TSelectronSelectronRH', str(mSlep)))
        xSecCorrection = '(('+xSecSlepLH+'*(susyIDprompt<=1000016)+'+xSecSlepRH+'*(susyIDprompt>=2000000))/Xsec)'

        for sleptonModel in [ 'TSlepSlep', 'TSlepSlepLH', 'TSeleSeleLH', 'TSmuoSmuoLH', 'TSlepSlepRH', 'TSeleSeleRH', 'TSmuoSmuoRH' ]:
            signalMassPoints[sleptonModel][sleptonModel+massPointName] = { }
            signalMassPoints[sleptonModel][sleptonModel+massPointName]['massPointDataset'] = datasetName
            signalMassPoints[sleptonModel][sleptonModel+massPointName]['massPointCut'] = xSecCorrection+'*(' + massPointCut
                
        signalMassPoints['TSlepSlep']  ['TSlepSlep'+massPointName]  ['massPointCut'] += ')'
        signalMassPoints['TSlepSlepLH']['TSlepSlepLH'+massPointName]['massPointCut'] += ' && susyIDprompt<=1000016)'
        signalMassPoints['TSeleSeleLH']['TSeleSeleLH'+massPointName]['massPointCut'] += ' && susyIDprompt==1000011)'
        signalMassPoints['TSmuoSmuoLH']['TSmuoSmuoLH'+massPointName]['massPointCut'] += ' && susyIDprompt==1000013)'
        signalMassPoints['TSlepSlepRH']['TSlepSlepRH'+massPointName]['massPointCut'] += ' && susyIDprompt>=2000000)'
        signalMassPoints['TSeleSeleRH']['TSeleSeleRH'+massPointName]['massPointCut'] += ' && susyIDprompt==2000011)'
        signalMassPoints['TSmuoSmuoRH']['TSmuoSmuoRH'+massPointName]['massPointCut'] += ' && susyIDprompt==2000013)'


