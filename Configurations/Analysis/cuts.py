##### cuts = {}

def andCuts(cutList):
    return ' && '.join(cutList)

def orCuts(cutList, operator = ' || '):
    return '(' + operator.join([ '('+x+')' for x in cutList ]) + ')'

for ptbin in jetPtBins:

    if '_Pt' in opt.tag and ptbin not in opt.tag: continue

    jetPtMin, jetPtMax = jetPtBins[ptbin][0], jetPtBins[ptbin][1]

    binMuJetCuts = [ 'muJet_pt>='+jetPtMin, 'muJet_pt<'+jetPtMax, muJetSel ]
    binAwayJetCuts, binTriggerCuts, binTriggerPrescales = [], [], []

    for trigger in triggerInfos:

        jetPtTrgMin, jetPtTrgMax = triggerInfos[trigger]['jetPtRange'][0], triggerInfos[trigger]['jetPtRange'][1] 

        if float(jetPtMin)<float(jetPtTrgMax) and float(jetPtTrgMin)<float(jetPtMax):

           triggerAwayJetCut = awayJetCut.replace('AWAYJETPTCUT', triggerInfos[trigger]['ptAwayJet'])
           ptInTriggerBinCut = andCuts([ 'muJet_pt>='+jetPtTrgMin, 'muJet_pt<'+jetPtTrgMax ])

           binAwayJetCuts.append(andCuts([ ptInTriggerBinCut, triggerAwayJetCut ]))
           binTriggerCuts.append(andCuts([ ptInTriggerBinCut, 'HLT_'+trigger ]))
           binTriggerPrescales.append(orCuts([ 'muJet_pt>='+jetPtTrgMin, 'muJet_pt<'+jetPtTrgMax, 'prescale_'+trigger ], '*'))

    binMuJetCut        = andCuts(binMuJetCuts)       
    binAwayJetCut      = orCuts(binAwayJetCuts)
    binTriggerCut      = orCuts(binTriggerCuts)
    binTriggerPrescale = orCuts(binTriggerPrescales, ' + ')

    cuts[ptbin] = { }

    if 'Data' in opt.sigset:
        cuts[ptbin]['expr'] = andCuts([ binMuJetCut, binAwayJetCut, binTriggerPrescale+'>=1.' ])
        if opt.method+'Data' not in opt.tag: cuts[ptbin]['weight'] = binTriggerPrescale

    else:
        cuts[ptbin]['expr'] = andCuts([ binMuJetCut, binAwayJetCut, binTriggerCut ])
        if opt.method+'Data' in opt.tag: cuts[ptbin]['weight'] = '0.'

if '_btag' in opt.tag:

   btagWPToRemove = []
   btagWPSelection = opt.tag.split('_btag')[1].split('_')[0]

   for btagwp in bTagWorkingPoints:
       if btagWPSelection not in btagwp: 
           btagWPToRemove.append(btagwp)
           
   for btagwp in btagWPToRemove:
       del bTagWorkingPoints[btagwp]

if 'PtRelTemplates' in opt.tag:

    for ptbin in jetPtBins:
        if ptbin not in cuts: continue
        for btagwp in bTagWorkingPoints:
            for btagselection in [ 'Pass', 'Fail' ]:

                cutName = '_'.join([ btagwp, ptbin, btagselection ])
                discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'[muJet_idx]>='+bTagWorkingPoints[btagwp]['cut'] 
                if btagselection=='Fail': discCut = discCut.replace('>=', '<')

                cuts[cutName] = {}
                cuts[cutName]['expr'] = andCuts([ cuts[ptbin]['expr'], discCut ])
                if 'weight' in cuts[ptbin]: cuts[cutName]['weight'] = cuts[ptbin]['weight']

                if '_NoAwayJetVariations' not in opt.tag: 
                    for btagAwayJetVariation in btagAwayJetVariations:
                        if btagAwayJetVariation!='Central':
 
                            cutAwayJetName = '_'.join([ btagwp, ptbin, btagAwayJetVariation, btagselection ])
                            ptbinAwayJetCut = cuts[ptbin]['expr'].replace(btagAwayJetVariations['Central'], btagAwayJetVariations[btagAwayJetVariation])                     

                            cuts[cutAwayJetName] = {}
                            cuts[cutAwayJetName]['expr'] = andCuts([ ptbinAwayJetCut, discCut ])
                            if 'weight' in cuts[ptbin]: cuts[cutAwayJetName]['weight'] = cuts[ptbin]['weight']

        del cuts[ptbin]

elif 'System8Templates' in opt.tag:

     for ptbin in jetPtBins:

         if ptbin not in cuts: continue 
         
         cutName = ptbin+'_AwayJetTag'
         cuts[cutName] = {}
         cuts[cutName]['expr'] = cuts[ptbin]['expr'].replace('>-999999.','>'+btagAwayJetVariations['Central'])
         if 'weight' in cuts[ptbin]: cuts[cutName]['weight'] = cuts[ptbin]['weight']

         for awayJetSelection in [ '', '_AwayJetTag' ]:
             for btagwp in bTagWorkingPoints: 

                 refCut = ptbin+awayJetSelection
                 cutName = '_'.join([ refCut, btagwp ])
                 discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'[muJet_idx]>='+bTagWorkingPoints[btagwp]['cut']

                 cuts[cutName] = {}
                 cuts[cutName]['expr'] = andCuts([ cuts[refCut]['expr'], discCut ])
                 if 'weight' in cuts[refCut]: cuts[cutName]['weight'] = cuts[refCut]['weight']
             
