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
            
        #mLSP = mNeutralino*bool(mNeutralino) + 1*bool(!mNeutralino)
        mLSP = mNeutralino
        if mLSP==0: mLSP = 1
        if mStop-mLSP==75: mLSP = mStop - 87 
            
        massPointName = 'T2tt' + '_mS-' + str(mStop) + '_mX-' + str(mLSP)
        massPointCut = '(susyMstop==' + str(mStop) + ' && susyMLSP==' + str(mLSP) + ')'

        massPoint = {}
        massPoint['massPointDataset'] = datasetName
        massPoint['massPointCut'] = massPointCut

        signalMassPoints['T2tt'][massPointName] = massPoint

