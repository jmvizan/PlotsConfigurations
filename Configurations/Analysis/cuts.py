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
                if 'Data' in opt.sigset:
                    lightAwayJetTrg += '*('+'prescale_'+triggerInfos[trigger]['jetTrigger']+')'

                binTriggerCuts.append(jetTriggerCut)
                lightAwayJetTrgSels.append(lightAwayJetTrg)

    return  orCuts(binTriggerCuts), orCuts(binTriggerPrescales, ' + '), orCuts(lightAwayJetTrgSels, ' + ')

def getPtHatSafetySelection(opt):

    if not opt.isShape or 'Data' in opt.tag: return ''

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

else:

    for ptbin in jetPtBins:

        if '_Pt' in opt.tag and ptbin not in opt.tag: continue

        jetPtMin, jetPtMax = jetPtBins[ptbin][0], jetPtBins[ptbin][1]

        binEventCuts = [ goodPV ]
        if 'Light' not in opt.tag: binEventCuts.extend([ muJetEvt, muJetPt+'>='+jetPtMin, muJetPt+'<'+jetPtMax, muJetSel ])
 
        binEventCut = andCuts(binEventCuts)
        binTriggerCut, binTriggerPrescale, lightAwayJetTrgSel = getAwayJetTriggerSelections(opt)

        if 'Light' not in opt.tag:

            cuts[ptbin] = { 'expr' : andCuts([ binEventCut, binTriggerCut, getMuonKinSelection(opt,'Central'), getPtHatSafetySelection(opt) ]) }

            if 'Data' in opt.sigset and opt.method+'Data' not in opt.tag: cuts[ptbin]['weight'] = binTriggerPrescale
            elif 'MC' in opt.sigset and opt.method+'Data' in opt.tag: cuts[ptbin]['weight'] = '0.'

        else: 

            cuts[ptbin] = { 'expr' : andCuts([ binEventCut, binTriggerCut ]) }

            cuts[ptbin]['lightJetWeight']   = orCuts([lightAwayJetTrgSel, getPtHatSafetySelection(opt) ], '*')
            lightTrkJetSel, nLightTrkJetCut = getMuonKinSelection(opt,'Central')
            cuts[ptbin]['cutNLightTrkJet']  = nLightTrkJetCut

            if 'LightTemplates' in opt.tag:

                cuts[ptbin]['cutLightTrkJetSel'] = lightTrkJetSel

                for musyst in [ '_MuPtUp', '_MuPtDown', '_MuDRUp', '_MuDRDown' ]: 

                    lightTrkJetSel, nLightTrkJetCut = getMuonKinSelection(opt,musyst)

                    cuts[ptbin+musyst] = deepcopy(cuts[ptbin])
                    cuts[ptbin+musyst]['cutNLightTrkJet']   = nLightTrkJetCut
                    cuts[ptbin+musyst]['cutLightTrkJetSel'] = lightTrkJetSel

        if 'PtRelTemplates' in opt.tag:

            for btagwp in bTagWorkingPoints:
                for btagselection in [ 'Pass', 'Fail' ]:

                    cutName = '_'.join([ btagwp, ptbin, btagselection ])
                    discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'['+muJetIdx+']>='+bTagWorkingPoints[btagwp]['cut']
                    if btagselection=='Fail': discCut = discCut.replace('>=', '<')

                    cuts[cutName] = deepcopy(cuts[ptbin])
                    cuts[cutName]['expr'] = andCuts([ cuts[ptbin]['expr'], discCut ])

                    if '_NoAwayJetVariations' not in opt.tag:
                        for btagAwayJetVariation in btagAwayJetVariations:
                            if btagAwayJetVariation!='Central':

                                cutAwayJetName = '_'.join([ btagwp, ptbin, btagAwayJetVariation, btagselection ])
                                ptbinAwayJetCut = cuts[ptbin]['expr'].replace(btagAwayJetVariations['Central'], btagAwayJetVariations[btagAwayJetVariation])

                                cuts[cutAwayJetName] = deepcopy(cuts[ptbin])
                                cuts[cutAwayJetName]['expr'] = andCuts([ ptbinAwayJetCut, discCut ])

            del cuts[ptbin]

        elif 'System8Templates' in opt.tag:

            awayTagVariations = { '' : 'None', 'AwayJetTag' : 'Central' }
            if '_NoAwayJetVariations' not in opt.tag:
                for btagAwayJetVariation in btagAwayJetVariations:
                    if btagAwayJetVariation!='Central': awayTagVariations[btagAwayJetVariation] = btagAwayJetVariation

            for awayTagVariation in awayTagVariations:

                if awayTagVariation=='':
                    cutName = ptbin
                else:
                    cutName = '_'.join([ ptbin, awayTagVariation ])
                    cuts[cutName] = deepcopy(cuts[ptbin])
                    cuts[cutName]['expr'] = cuts[ptbin]['expr'].replace('>=-999999.','>='+btagAwayJetVariations[awayTagVariations[awayTagVariation]])

                for btagwp in bTagWorkingPoints:

                    btagCutName = '_'.join([ cutName, btagwp ])
                    discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'['+muJetIdx+']>='+bTagWorkingPoints[btagwp]['cut']

                    cuts[btagCutName] = deepcopy(cuts[cutName])
                    cuts[btagCutName]['expr'] = andCuts([ cuts[cutName]['expr'], discCut ])

        if opt.method+'Templates' in opt.tag and '_NoMuonSelVariations' not in opt.tag:

            cutList = cuts.keys()

            for cutName in cutList:
                if ptbin in cutName:

                    isAwayJetTag = False
                    for btagAwayJetVariation in btagAwayJetVariations:
                        if btagAwayJetVariation in cutName: isAwayJetTag = True

                    if not isAwayJetTag:

                        muonCentralSelection = getMuonKinSelection(opt,'Central') 

                        for musyst in [ 'MuPtUp', 'MuPtDown', 'MuDRUp', 'MuDRDown' ]:

                            musystCutName = cutName.replace(ptbin, '_'.join([ ptbin, musyst ]))
                            cuts[musystCutName] = deepcopy(cuts[cutName])
                            cuts[musystCutName]['expr'] = cuts[cutName]['expr'].replace(muonCentralSelection, getMuonKinSelection(opt,musyst)) 






