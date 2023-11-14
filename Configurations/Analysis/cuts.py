##### cuts = {}

from copy import deepcopy

def andCuts(cutList):
    return ' && '.join([ x for x in cutList if x!='' ])

def orCuts(cutList, operator = ' || '):
    return '(' + operator.join([ '('+x+')' for x in cutList if x!='' ]) + ')'

def getAwayJetTriggerSelections(opt):

    if not opt.isShape: return '', '', ''

    binTriggerCuts, binTriggerPrescales, lightAwayJetTrgSels = [], [], []

    for trigger in triggerInfos:

        jetPtTrgMin, jetPtTrgMax = triggerInfos[trigger]['jetPtRange'][0], triggerInfos[trigger]['jetPtRange'][1]

        if float(jetPtMin)<float(jetPtTrgMax) and float(jetPtTrgMin)<float(jetPtMax):

            if 'Light' not in opt.tag:

                ptInTriggerBinCut = andCuts([ muJetPt+'>='+jetPtTrgMin, muJetPt+'<'+jetPtTrgMax ])
                triggerAwayJetCut = awayJetCut.replace('AWAYJETPTCUT', triggerInfos[trigger]['ptAwayJet'])
                btagTriggerCut    = triggerCut.replace('triggerIdx',triggerInfos[trigger]['idx'])
                if opt.method=='PtRel' and float(triggerInfos[trigger]['ptTriggerEmulation'])>0.:
                    btagTriggerCut += ' && '+ triggerEmul.replace('TRGEMULJETPTCUT',triggerInfos[trigger]['ptTriggerEmulation'])

                binTriggerCuts.append(andCuts([ ptInTriggerBinCut, triggerAwayJetCut, btagTriggerCut ]))
                binTriggerPrescales.append(orCuts([ muJetPt+'>='+jetPtTrgMin, muJetPt+'<'+jetPtTrgMax, 'prescale_'+trigger ], '*'))

            else:

                jetTriggerCut    = triggerCut.replace('triggerIdx',triggerInfos[trigger]['idxJetTrigger'])
                lightAwayJetTrg = '(Alt$('+jetPt+'[JETIDX],-1.)>='+triggerInfos[trigger]['jetPtRange'][0]+')*(Alt$('+jetPt+'[JETIDX],999999.)<'+triggerInfos[trigger]['jetPtRange'][1]+')*('+awayJetLightCut.replace('AWAYJETPTCUT',triggerInfos[trigger]['ptAwayJet'])+')*('+jetTriggerCut+')'
                if float(triggerInfos[trigger]['ptTriggerEmulation'])>0.:
                    lightAwayJetTrg += '*('+triggerEmul.replace(muJetIdx,'JETIDX').replace('TRGEMULJETPTCUT',triggerInfos[trigger]['ptTriggerEmulation'])+')'
                if 'Data' in opt.sigset and 'NoPS' not in opt.tag and 'Validation' not in opt.tag:
                    lightAwayJetTrg += '*('+'prescale_'+triggerInfos[trigger]['jetTrigger']+')'

                binTriggerCuts.append(jetTriggerCut)
                lightAwayJetTrgSels.append(lightAwayJetTrg)

    return  orCuts(binTriggerCuts), orCuts(binTriggerPrescales, ' + '), orCuts(lightAwayJetTrgSels, ' + ')

def getPtHatSafetySelection(opt):

    if not opt.isShape or 'Data' in opt.sigset: return ''

    ptHatSafetyVetoes = []

    for pthatthr in sorted(pthatThresholds):
        if float(jetPtMin)>pthatThresholds[pthatthr]:
            ptHatSafetyVetoes = [ 'pthat<'+str(pthatthr) ]
        elif float(jetPtMax)>pthatThresholds[pthatthr]:
            if 'Light' not in opt.tag: ptHatSafetyVetoes.append('pthat<'+str(pthatthr)+' && '+muJetPt+'>'+str(pthatThresholds[pthatthr]))
            else: ptHatSafetyVetoes.append('(pthat<'+str(pthatthr)+')*('+jetPt+'[JETIDX]>'+str(pthatThresholds[pthatthr])+')')

    if len(ptHatSafetyVetoes)==0: return ''
    if 'Light' not in opt.tag: return '!'+orCuts(ptHatSafetyVetoes)
    else: return orCuts(ptHatSafetyVetoes, '+')+'==0'

def getMuonKinSelection(opt, muonsyst):

    if not opt.isShape:
       if 'Light' not in opt.tag: return ''
       else: return '', ''

    muonKinCuts, lightTrkJetSels, nLightTrkJetList = [], [], []

    ptcut = 0 if 'Pt' not in muonsyst else 1 if 'Down' in muonsyst else 2
    drcut = 0 if 'DR' not in muonsyst else 1 if 'Down' in muonsyst else 2

    for mubin in muonKinBins:

        jetPtMuBinMin, jetPtMuBinMax = muonKinBins[mubin]['range'][0], muonKinBins[mubin]['range'][1]

        if float(jetPtMin)<float(jetPtMuBinMax) and float(jetPtMuBinMin)<float(jetPtMax):

            muPtCut, muDRCut = muonKinBins[mubin]['pt'][ptcut], muonKinBins[mubin]['dr'][drcut]

            if 'Light' not in opt.tag:
                    muonKinCuts.append( andCuts([ muJetPt+'>='+jetPtMuBinMin, muJetPt+'<'+jetPtMuBinMax, muJetDR+'<'+muDRCut, muPt+'>'+muPtCut ]) )

            else:
                jetInMuonKinBinCuts = orCuts([ jetPt+'[JETIDX]>='+jetPtMuBinMin, jetPt+'[JETIDX]<'+jetPtMuBinMax ], '*')
                lightTrkJetSels.append(  orCuts([ jetInMuonKinBinCuts, lightTrkSel.replace('TRKPTCUT',muPtCut).replace('TRKDRCUT',muDRCut)  ], '*') )
                nLightTrkJetList.append( orCuts([ jetInMuonKinBinCuts, nLightTrkJet.replace('TRKPTCUT',muPtCut).replace('TRKDRCUT',muDRCut) ], '*') )

    if 'Light' not in opt.tag: return orCuts(muonKinCuts)
    else: return orCuts(lightTrkJetSels, ' + '), orCuts(nLightTrkJetList, ' + ')

if 'WorkingPoints' in opt.tag:

    cuts['QCD'] = { 'expr' : goodPV } 

elif 'PtRelTemplates' in opt.tag and 'ForFit' in opt.tag:

    for ptbin in jetPtBins:
        for btagwp in bTagWorkingPoints:
            for btagselection in [ 'Pass', 'Fail' ]:
                for selection in systematicVariations:
                    if 'JEU' not in selection:
                        cutNameList = [ ptbin, btagwp, btagselection ] if selection=='' else [ ptbin, btagwp, btagselection, selection ]
                        cuts['_'.join(cutNameList)] = { 'expr' : goodPV }

else:

    for ptbin in jetPtBins:

        if '_Pt' in opt.tag and ptbin not in opt.tag: continue

        jetPtMin, jetPtMax = jetPtBins[ptbin][0], jetPtBins[ptbin][1]

        binEventCuts = [ goodPV ]
        if 'Light' not in opt.tag: binEventCuts.extend([ muJetEvt, muJetPt+'>='+jetPtMin, muJetPt+'<'+jetPtMax, muJetSel ])
 
        binEventCut = andCuts(binEventCuts)
        binTriggerCut, binTriggerPrescale, lightAwayJetTrgSel = getAwayJetTriggerSelections(opt)

        if 'Light' not in opt.tag:

            cuts[ptbin] = { 'expr' : andCuts([ binEventCut, binTriggerCut, getMuonKinSelection(opt,muonKinSelection), getPtHatSafetySelection(opt) ]) }

            if 'Data' in opt.sigset and opt.method+'Data' not in opt.tag and 'NoPS' not in opt.tag and 'Validation' not in opt.tag: cuts[ptbin]['weight'] = binTriggerPrescale
            elif 'MC' in opt.sigset and opt.method+'Data' in opt.tag: cuts[ptbin]['weight'] = '0.'

            if 'System8Templates' in opt.tag: 
                cuts[ptbin+'_AwayJetTag'] = deepcopy(cuts[ptbin])
                cuts[ptbin+'_AwayJetTag']['expr'] = cuts[ptbin+'_AwayJetTag']['expr'].replace('>=-999999.', '>='+btagAwayJetVariations[awayJetTagSelection])

        else: 

            cuts[ptbin] = { 'expr' : andCuts([ binEventCut, binTriggerCut ]) }

            cuts[ptbin]['lightJetWeight']   = orCuts([lightAwayJetTrgSel, getPtHatSafetySelection(opt) ], '*')
            lightTrkJetSel, nLightTrkJetCut = getMuonKinSelection(opt,muonKinSelection)
            cuts[ptbin]['cutNLightTrkJet']  = nLightTrkJetCut

            if 'LightTemplates' in opt.tag:

                cuts[ptbin]['cutLightTrkJetSel'] = lightTrkJetSel


