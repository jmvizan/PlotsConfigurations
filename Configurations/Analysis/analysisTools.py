import os
import ROOT
import commonTools
from array import array

### Loops on analysis years and tags

### Analysis specific weights, efficiencies, scale factors, etc.

def kinematicWeights(opt):

    if 'mujetpteta' in opt.option.lower():
        print 'kinematicWeights in 2D not supported yet'
        exit()

    for year in opt.year.split('-'):

        outputDir = '/'.join([ opt.datadir, year, 'Kinematics' ])
        os.system('mkdir -p '+outputDir)

        samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, opt.sigset, 'variables')

        data, backgrounds = '', [ ]
        for sample in samples:
            if samples[sample]['isDATA']: data = sample
            else: backgrounds.append(sample)

        if 'mujetpt' in opt.option.lower() or 'mujeteta' in opt.option.lower():

            minMuJetPt, maxMuJetPt, maxMuJetEta, muJetPtEdges, cutLowerPtEdge = 999999., -999999., -10., [], {}

            for cut in cuts:

                cutList =  cuts[cut]['expr'].split(' ')
                cutLowerPt = 999999.
                nJetPtCuts, nJetEtaCuts = 0, 0
                for subcut in cutList:
                    if 'muJet_eta' in subcut and 'muJet_phi' not in subcut and nJetEtaCuts==0:
                        etaCut = float(subcut.split('<')[1].replace('=','').replace(')',''))
                        maxMuJetEta = max(maxMuJetEta, etaCut)
                        nJetEtaCuts += 1
                    elif 'muJet_pt' in subcut and ')' not in subcut and nJetPtCuts<2:
                        ptCut = float(subcut.replace('>','<').split('<')[1].replace('=','').replace(')',''))
                        minMuJetPt = min(minMuJetPt, ptCut)
                        maxMuJetPt = max(maxMuJetPt, ptCut)
                        cutLowerPt = min(cutLowerPt, ptCut)
                        if ptCut not in muJetPtEdges:
                            muJetPtEdges.append(ptCut)
                        nJetPtCuts += 1

                cutLowerPtEdge[cut] = cutLowerPt              

            minMuJetEta = -maxMuJetEta
            muJetPtEdges.sort()

            weightsHisto = { }

            if 'mujetpt' in opt.option.lower():
                for back in backgrounds:
                    weightsHisto[back] = ROOT.TH2F(back+'-mujetpt',  '', int(maxMuJetPt-minMuJetPt), minMuJetPt, maxMuJetPt, 1, minMuJetEta, maxMuJetEta)

            elif 'mujeteta' in opt.option.lower():
                nEtaBins = int((maxMuJetEta-minMuJetEta)/0.1)
                for back in backgrounds:
                    weightsHisto[back] = ROOT.TH2F(back+'-mujeteta', '', len(muJetPtEdges)-1, array('d',muJetPtEdges), nEtaBins, minMuJetEta, maxMuJetEta)

        inputFile = commonTools.openShapeFile(opt.shapedir, opt.year, opt.tag, opt.sigset, opt.fileset)


        for variable in variables:

            if variable.split('_')[0] not in opt.option.lower(): continue

            outputname = opt.tag.split('Prod')[0].replace('Kinematics','') + ':' + variable.split('_')[0]
            outputFile = ROOT.TFile(outputDir+'/'+outputname+'.root', 'recreate')

            for back in backgrounds:

                for cut in cuts: 
                    if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:
 
                        dataHisto = inputFile.Get('/'.join([ cut, variable, 'histo_'+data ])) ; dataHisto.SetDirectory(0)
                        backHisto = inputFile.Get('/'.join([ cut, variable, 'histo_'+back ])) ; backHisto.SetDirectory(0)

                        if 'skipfixspikes' not in opt.option:

                            spikeList = [ ]
                            for ib in range(1, backHisto.GetNbinsX()+1):
                                isSpike = True
                                for shift in [ ib-1, ib+1 ]:
                                    if backHisto.GetBinContent(shift)>0.:
                                        if backHisto.GetBinContent(ib)/backHisto.GetBinContent(shift)<1.1:
                                            isSpike = False
                                if isSpike: spikeList.append(ib)

                            for spike in spikeList:
                                spikeContent, spikeShifts = 0., 0
                                for shift in [ spike-1, spike+1 ]:
                                    if backHisto.GetBinContent(shift)>0.:
                                        spikeContent += backHisto.GetBinContent(shift)
                                        spikeShifts += 1
                                spikeContent /= spikeShifts
                                backHisto.SetBinContent(spike, spikeContent)

                        if 'mujetpt' in opt.option.lower() or 'mujeteta' in opt.option.lower():

                            dataHisto.Divide(backHisto) 

                            if 'mujetpt' in opt.option.lower():
                        
                                minPtFit, maxPtFit = dataHisto.GetBinLowEdge(1), dataHisto.GetBinLowEdge(dataHisto.GetNbinsX()+1)
                                ptfit = ROOT.TF1('ptfit', 'pol3', minPtFit, maxPtFit)
                                dataHisto.Fit('ptfit')

                            binx, biny, binz = ROOT.Long(), ROOT.Long(), ROOT.Long()

                            ptval  = cutLowerPtEdge[cut] + 0.1
                            etaval = weightsHisto[back].GetYaxis().GetBinCenter(1)

                            for ib in range(dataHisto.GetNbinsX()):

                                if 'mujetpt' in opt.option.lower():
                                    ptval  = dataHisto.GetBinCenter(ib+1)
                                    weight = ptfit.Eval(dataHisto.GetBinCenter(ib+1))

                                elif 'mujeteta' in opt.option.lower():
                                    etaval = dataHisto.GetBinCenter(ib+1)
                                    weight = dataHisto.GetBinContent(ib+1)

                                bin2D = weightsHisto[back].FindBin(ptval, etaval)
                                weightsHisto[back].GetBinXYZ(bin2D, binx, biny, binz)
                                weightsHisto[back].SetBinContent(binx, biny, weight)

                                if 'verbose' in opt.option:
                                    print back, cut, ptval, etaval, weight

                weightsHisto[back].Write()                        

            outputFile.Close()

