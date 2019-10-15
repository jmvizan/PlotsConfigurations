signalMassPoints = {}

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
        massPointCut = '(susyMstop==' + str(mStop) + ' && susyMLSP==' + str(mLSP) + ')'

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
        massPointCut = '(susyMstop==' + str(mStop) + ' && susyMLSP==' + str(mLSP) + ')'

        massPoint = {}
        massPoint['massPointDataset'] = datasetName
        massPoint['massPointCut'] = massPointCut

        signalMassPoints['T2bW'][massPointName] = massPoint

signalMassPoints['TChipmSlepSnu'] = {}

for mChipm in range( 100,  1501, 25):
    datasetName = 'TChipmSlepSnu'
    if mChipm>800:
        datasetName += '__mC1_825_1500'
    for mNeutralino in range( 0,  min(mChipm-49, 901), 25):
            
        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
            
        massPointName = 'TChipmSlepSnu' + '_mC-' + str(mChipm) + '_mX-' + str(mLSP)
        massPointCut = '(susyMstop==' + str(mChipm) + ' && susyMLSP==' + str(mLSP) + ')'

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
            massPointCut = '(susyMstop==' + str(mChipm) + ' && susyMLSP==' + str(mLSP) + ')'

            massPoint = {}
            massPoint['massPointDataset'] = datasetName
            massPoint['massPointCut'] = massPointCut

            signalMassPoints['TChipmWW'][massPointName] = massPoint

