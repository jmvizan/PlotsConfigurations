#!/usr/bin/env python
import os
import sys
import ROOT
import math
import glob
import optparse
from array import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

Zmass = 91.1876

yearset=sys.argv[1]
prodset=sys.argv[2]
sample=sys.argv[3]
maxentries=int(sys.argv[4])

campaign = 'UL'
#treeLevel = 'DY'
treeLevel = ''

SITE=os.uname()[1]

def getLeptonMass(pdgId) :

    if abs(pdgId)==11 :
        return 0.000511
    elif abs(pdgId)==13 :
        return 0.105658
    else:
        print 'mt2llProducer: WARNING: unsupported lepton pdgId'
        return -1

def isTightMuon(muon):
    if muon.mediumId==1 and abs(muon.sip3d)<4. and abs(muon.dxy)<0.05 and abs(muon.dz)<0.10 and muon.pfRelIso04_all<0.15:
        return True
    return False

def isTightElectron(electron): 
    if electron.cutBased>=3 and abs(electron.sip3d)<4. and abs(electron.dxy)<0.05 and abs(electron.dz)<0.10 and electron.lostHits==0:
        return True    
    return False

if __name__ == '__main__':

    if campaign=='EOY':

        eosusr = '/eos/cms/store/user/scodella/SUSY/Nano/'
        eoscaf = '/eos/cms/store/caf/user/scodella/BTV/Nano/' 
        #eosusr = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
        #eoscaf = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/' 

        #treeName = 'nanoLatino_TTJetsDilep__part*root'
        treeName = 'nanoLatino_DYJetsToLL_M-50-LO_*part*root' 
        treeDir = 'XXX_102X_nAODv6_Full201Yv6loose/SFSusy201Y'+treeLevel+'v6loose/'+treeName

        years = { '2016' : { 'fastsim' : eosusr+treeDir.replace('XXX', 'Summer16FS').replace('201Y', '2016'), 
       	                     'fullsim' : eosusr+treeDir.replace('XXX', 'Summer16').replace('201Y', '2016')    } ,  
                  '2017' : { 'fastsim' : eosusr+treeDir.replace('XXX', 'Fall2017FS').replace('201Y', '2017'), 
                             'fullsim' : eoscaf+treeDir.replace('XXX', 'Fall2017').replace('201Y', '2017')    } ,  
                  '2018' : { 'fastsim' : eoscaf+treeDir.replace('XXX', 'Autumn18FS').replace('201Y', '2018'),  
                             'fullsim' : eoscaf+treeDir.replace('XXX', 'Autumn18').replace('201Y', '2018')    } }
    elif campaign=='UL':

        if 'cern' in SITE:
            eosusr = '/eos/home-p/pmatorra/SUS_SF/'
            eoscaf = '/eos/home-p/pmatorra/SUS_SF/'
        else:
            eosusr = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
            eoscaf = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'

        if 'DY' in sample:
            stepName = 'SFSusyDY'
            treeNameFast = 'nanoLatino_DYJetsToLL_M-50-LO__part*root'
            treeNameFull = 'nanoLatino_DYJetsToLL_M-50-LO__part*root'
        elif 'ttbar' in sample:
            stepName = 'SFSusyTT'
            treeNameFast = 'nanoLatino_TTJets_DiLept__part*.root'
            treeNameFull = 'nanoLatino_TTJets_DiLept__part*.root'
        else:
            stepName = 'susyGen__susyW__SFSusySig'
            if 'T2tt_mStop-525_mLSP-350' in sample:
                treeNameFull = 'nanoLatino_T2tt_mStop-525_mLSP-350__part*.root'
                treeNameFast = 'nanoLatino_T2tt_mStop-400to825__part*.root'
            elif 'T2tt_mStop-525_mLSP-438' in sample:
                treeNameFull = 'nanoLatino_T2tt_mStop-525_mLSP-438__part*.root'
                treeNameFast = 'nanoLatino_T2tt_mStop-400to825__part*.root'
            elif 'T2tt_dm-175' in sample:
                treeNameFull = 'nanoLatino_T2tt_mStop-525_mLSP-350__part*.root'
                treeNameFast = 'nanoLatino_T2tt_mStop-*__part*.root'
            elif 'T2tt_dm-87' in sample:
                treeNameFull = 'nanoLatino_T2tt_mStop-525_mLSP-438__part*.root'
                treeNameFast = 'nanoLatino_T2tt_mStop-*__part*.root'
            elif 'TChipmSlepSnu_mC-1150_mX-1' in sample:
                treeNameFull = 'nanoLatino_TChipmSlepSnu_mC-1150_mX-1__part*.root'
                treeNameFast = 'nanoLatino_TChipmSlepSnu_mC1-825to1500__part*.root'
            elif 'TChipmSlepSnu_mC-900_mX-475' in sample:
                treeNameFull = 'nanoLatino_TChipmSlepSnu_mC-900_mX-475__part*.root'
                treeNameFast = 'nanoLatino_TChipmSlepSnu_mC1-825to1500__part*.root'
            elif 'TChipmSlepSnu_mX-1' in sample:
                treeNameFull = 'nanoLatino_TChipmSlepSnu_mC-1150_mX-1__part*.root'
                treeNameFast = 'nanoLatino_TChipmSlepSnu_mC1*__part*.root'
            elif 'TChipmSlepSnu_dm-425' in sample:
                treeNameFull = 'nanoLatino_TChipmSlepSnu_mC-900_mX-475__part*.root'
                treeNameFast = 'nanoLatino_TChipmSlepSnu_mC1-825to1500__part*.root' 
        years = { '2016HIPM'   : { 'fastsim' : eosusr+'Spring21UL16FS_106X_nAODv9_Full2016v8/'+stepName+'/'+treeNameFast,
                                   'fullsim' : eosusr+'Summer20UL16_106X_nAODv9_HIPM_Full2016v8/'+stepName+'/'+treeNameFull,    } ,
                  '2016noHIPM' : { 'fastsim' : eosusr+'Spring21UL16FS_106X_nAODv9_Full2016v8/'+stepName+'/'+treeNameFast,
                                   'fullsim' : eosusr+'Summer20UL16_106X_nAODv9_noHIPM_Full2016v8/'+stepName+'/'+treeNameFull,    } ,
                  '2017'       : { 'fastsim' : eosusr+'Spring21UL17FS_106X_nAODv9_Full2017v8/'+stepName+'/'+treeNameFast,
                                   'fullsim' : eosusr+'Summer20UL17_106X_nAODv9_Full2017v8/'+stepName+'/'+treeNameFull,    } ,
                  '2018'       : { 'fastsim' : eosusr+'Spring21UL18FS_106X_nAODv9_Full2018v8/'+stepName+'/'+treeNameFast,
                                   'fullsim' : eosusr+'Summer20UL18_106X_nAODv9_Full2018v8/'+stepName+'/'+treeNameFull,    } , }
    else:
        print 'Error: campaign', campaign, 'is not supported'
        exit()


    #matchedLepton = '(LeptonGen_isPrompt[abs(Lepton_genIdx)]==1 || LeptonGen_isDirectPromptTauDecayProduct[abs(Lepton_genIdx)]==1)'
    #matchedGenLepton = '(LeptonGen_isPrompt==1 || LeptonGen_isDirectPromptTauDecayProduct==1)'
    #matchedElectron = '((GenPart_statusFlags[abs(Electron_genPartIdx)] & 1) || (GenPart_statusFlags[abs(Electron_genPartIdx)] >> 5 & 1))'
    #matchedMuon = '((GenPart_statusFlags[abs(Muon_genPartIdx)] & 1) || (GenPart_statusFlags[abs(Muon_genPartIdx)] >> 5 & 1))'
    #matchedLepton = '(LeptonGen_isPrompt[abs(Lepton_genIdx)]==1)'
    #matchedGenLepton = '(LeptonGen_isPrompt==1)'
    #matchedElectron = '((GenPart_statusFlags[abs(Electron_genPartIdx)] & 1))'
    #matchedMuon = '((GenPart_statusFlags[abs(Muon_genPartIdx)] & 1))'    
    #matchedParton = '((GenPart_statusFlags & 1))'

    #leptons = { 'Ele' : 'isTightElectron_cutBasedMediumPOG',
    #            #'Ele' : '(Lepton_electronIdx)' 
    #            'Muo' : 'isTightMuon_mediumRelIsoTight'
    #          }

    binsx = { 'Muo' : [ 10., 20., 35., 50., 100., 200., 500. ],
              #'Ele' : [ -2.400, -1.444, -0.800,  0.000, 0.800, 1.444, 2.400 ] }
              'Ele' : [ -2.400, -2.000, -1.566, -1.444, -0.800, 0.000, 0.800, 1.444, 1.566, 2.000, 2.400 ] }
    binsy = { 'Muo' : [ 0., 0.9, 1.2, 2.1, 2.4 ],
              'Ele' : [ 10., 20., 35., 50., 100., 500. ] }

    levels = [ 'reco', 'tight' ]
    if 'DY' not in treeLevel:
        levels.append('gen')
        levels.append('recogen')
        levels.append('tightgen')

    for year in yearset.split('-'):

        outputDir = './Data/'+year+'/'
        os.system('mkdir -p '+outputDir)

        histos = { }
        print prodset
        for sim in prodset.split('-'):
            print years[year][sim]
            events = ROOT.TChain('Events') 
            if maxentries<0 or maxentries>=10:
                jobFlag = ''
                events.Add(years[year][sim])
            else:
                jobFlag = '__part'+str(maxentries)
                nTrees = len(glob.glob(years[year][sim]))
                nParts = math.ceil(nTrees/10)
                for part in range(maxentries*nParts, min(maxentries*(nParts+1), nTrees)):
                    print 'Adding ', years[year][sim].replace('*',part)
                    events.Add(years[year][sim].replace('*',part)) 

            histos[sim] = { }
            for lepton in [ 'Ele', 'Muo' ]:
  
                histos[sim][lepton] = { }
                for level in levels: 
                    histos[sim][lepton][level] = ROOT.TH2F(lepton+'_'+level+'_'+sim, '', len(binsx[lepton])-1, array('d',binsx[lepton]), len(binsy[lepton])-1, array('d',binsy[lepton]))                                                                                            
            mp, mx = -1., -1.
            if '_dm' in sample:
                dm = float(sample.split('_')[1].split('-')[-1])
            elif 'TChipm_mX'in sample:
                mx = float(sample.split('_')[1].split('-')[-1])
            elif 'T2tt_m'in sample or 'TChipm_mC'in sample:
                mp = float(sample.split('_')[1].split('-')[-1])
                mx = float(sample.split('_')[2].split('-')[-1])

            nentries = events.GetEntries()            
            print maxentries, nentries
            if maxentries>=10 and maxentries<nentries:
                nentries = maxentries

            print year, sim, sample, nentries 
            for entry in range(nentries):

                events.GetEntry(entry)

                if 'T2tt_m' in sample:
                    if events.susyMstop<mp-4. or events.susyMstop>mp+4. or events.susyMLSP<mx-2. or events.susyMLSP>mx+2.: continue
                elif 'T2tt_dm' in sample:
                    if events.susyMstop-events.susyMLSP<dm-5. or events.susyMstop-events.susyMLSP>dm+5.: continue
                elif 'TChipm_m' in sample:
                    if events.susyMLSP<mx-2. or events.susyMLSP>mx+2.: continue
                    if 'TChipm_mC'in sample:
                        if events.susyMChargino<mp-4. or events.susyMChargino>mp+4.: continue
                elif 'TChipm_dm' in sample:
                    if events.susyMChargino-events.susyMLSP<dm-5. or events.susyMChargino-events.susyMLSP>dm+5.: continue

                #recoleptons = Collection(events, 'Lepton')      
                #if 'DY' not in treeLevel: 
                #    genleptons = Collection(events, 'LeptonGen') 
                electrons = Collection(events, 'Electron')
                muons = Collection(events, 'Muon')
                genparticles = Collection(events, 'GenPart')

                if 'DY' not in treeLevel:

                    # gen
                    genLep = [ ]
                    genLepPdgId = [ ]
                    genLepReco = [ ]
                    #genLepTight = [ ] 
                    genVec = ROOT.vector('TLorentzVector')()
                    #for glep in range(events.nLeptonGen):
                    #    if genleptons[glep].isPrompt and genleptons[glep].pt>10. and abs(genleptons[glep].eta)<2.4 and (abs(genleptons[glep].pdgId)==11 or abs(genleptons[glep].pdgId)==13):

                    for glep in range(events.nGenPart):
                        if genparticles[glep].pt>10. and abs(genparticles[glep].eta)<2.4 and (abs(genparticles[glep].pdgId)==11 or abs(genparticles[glep].pdgId)==13):
                            lepMotherPdgId, lepMotherIdx = -1, genparticles[glep].genPartIdxMother                        
                            if lepMotherIdx>=0:
                                lepMotherPdgId = genparticles[lepMotherIdx].pdgId
                            if 'DY' in sample and abs(lepMotherPdgId)!=23: continue
                            if 'ttbar' in sample and abs(lepMotherPdgId)!=24: continue
                            if 'T2tt' in sample and abs(lepMotherPdgId)!=24: continue
                            if 'TChipm' in sample and abs(lepMotherPdgId)!=1000024 and (lepMotherPdgId)!=1000011 and (lepMotherPdgId)!=1000013 and (lepMotherPdgId)!=2000011 and (lepMotherPdgId)!=2000013: continue

                            genLep.append(glep)
                            genLepId = genparticles[glep].pdgId # genleptons[glep].pdgId
                            genLepPdgId.append(genLepId)
                            genlepton = ROOT.TLorentzVector()
                            #genlepton.SetPtEtaPhiM(genleptons[glep].pt, genleptons[glep].eta, genleptons[glep].phi, getLeptonMass(genleptons[glep].pdgId))
                            genlepton.SetPtEtaPhiM(genparticles[glep].pt, genparticles[glep].eta, genparticles[glep].phi, getLeptonMass(genparticles[glep].pdgId))
                            genVec.push_back(genlepton)

                            #tidx, ridx = -1, -1
                            ridx = -1
                          
                            ##for tlep in range(events.nLepton):
                            ##    if recoleptons[tlep].genIdx==glep: 
                            ##        tidx = tlep

                            if abs(genLepId)==11:
                                for rlep in range(events.nElectron):
                                    if electrons[rlep].genPartIdx>=0.:
                                        if abs(genparticles[electrons[rlep].genPartIdx].phi-genlepton.Phi())<0.01 and abs(genparticles[electrons[rlep].genPartIdx].eta-genlepton.Eta())<0.01:
                                            ridx = rlep
                                            #for tlep in range(events.nLepton):
                                            #    if recoleptons[tlep].electronIdx==rlep:
                                            #        tidx = tlep 
  
                            elif abs(genLepId)==13:
                                for rlep in range(events.nMuon):
                                    if muons[rlep].genPartIdx>=0.:
                                        if abs(genparticles[muons[rlep].genPartIdx].phi-genlepton.Phi())<0.01 and abs(genparticles[muons[rlep].genPartIdx].eta-genlepton.Eta())<0.01:          
                                            ridx = rlep
                                            #for tlep in range(events.nLepton):
                                            #    if recoleptons[tlep].muonIdx==rlep:
                                            #        tidx = tlep

                            genLepReco.append(ridx)
                            #genLepTight.append(tidx)

                    if len(genLep)==2:
                        #if abs(genleptons[genLep[0]].pdgId)==abs(genleptons[genLep[1]].pdgId):
                        #    if (genleptons[genLep[0]].pdgId*genleptons[genLep[1]].pdgId)<0.:
                        goodDY = abs(genLepPdgId[0])==abs(genLepPdgId[1]) and (genLepPdgId[0]*genLepPdgId[1])<0. and abs((genVec[0] + genVec[1]).M() - Zmass)<30.
                        if goodDY or ('DY' not in sample and (genLepPdgId[0]*genLepPdgId[1])<0.):
               
                            #lepton = 'Ele' if abs(genleptons[genLep[0]].pdgId)==11 else 'Muo'
                            #lepton = 'Ele' if abs(genLepPdgId[0])==11 else 'Muo'
                            isLeptonTight = []
                            for glep in range(len(genLep)):
                                if genLepReco[glep]>=0:
                                    if abs(genLepPdgId[glep])==11: isLeptonTight.append(isTightElectron(electrons[genLepReco[glep]]))
                                    if abs(genLepPdgId[glep])==13: isLeptonTight.append(isTightMuon(muons[genLepReco[glep]]))
                                else: isLeptonTight.append(False)

                            for glep in range(len(genLep)):
                                #if genLepTight[1-glep]>=0:
                                #if (lepton=='Ele' and isTightElectron(electrons[])) or (lepton=='Muo' and ):
                                if isLeptonTight[1-glep]:

                                    lepton = 'Ele' if abs(genLepPdgId[glep])==11 else 'Muo'
                                    if lepton=='Ele':
                                        obsx = genVec[glep].Eta()
                                        obsy = genVec[glep].Pt()
                                    else:
                                        obsx = genVec[glep].Pt()
                                        obsy = abs(genVec[glep].Eta())
                                            
                                    histos[sim][lepton]['gen'].Fill(obsx, obsy)
                        
                                    #if genLepTight[glep]>=0: 
                                    #    if (getattr(recoleptons[genLepTight[glep]], leptons[lepton]))==1:
                                    #        histos[sim][lepton]['tightgen'].Fill(obsx, obsy)

                                    if genLepReco[glep]>=0:
                                        histos[sim][lepton]['recogen'].Fill(obsx, obsy)
                                        if isLeptonTight[glep]:
                                            histos[sim][lepton]['tightgen'].Fill(obsx, obsy)

                # lepton
                recoLepton = [ ]
                recoLeptonID = [ ]
                leptonVec = ROOT.vector('TLorentzVector')()
                
                # muon
                recoMuo = [ ]
                #recoMuoTight = [ ]
                muoVec = ROOT.vector('TLorentzVector')()
                for muo in range(events.nMuon):
                    if muons[muo].genPartIdx>=0.:
                        if (genparticles[muons[muo].genPartIdx].statusFlags & 1) and muons[muo].pt>10. and abs(muons[muo].eta)<2.4:
                            
                            recoMuo.append(muo)
                            recomuon = ROOT.TLorentzVector()
                            recomuon.SetPtEtaPhiM(muons[muo].pt, muons[muo].eta, muons[muo].phi, getLeptonMass(13))
                            muoVec.push_back(recomuon)

                            recoLepton.append(muo)
                            recoLeptonID.append(13)
                            leptonVec.push_back(recomuon)

                            #tidx = -1
                            
                            #for tlep in range(events.nLepton): 
                            #    if recoleptons[tlep].muonIdx==muo:  
                            #        tidx = tlep 
         
                            #recoMuoTight.append(tidx)

                # electron
                recoEle = [ ]
                #recoEleTight = [ ]
                eleVec = ROOT.vector('TLorentzVector')()
                for ele in range(events.nElectron):
                    if electrons[ele].genPartIdx>=0.:
                        if (genparticles[electrons[ele].genPartIdx].statusFlags & 1) and electrons[ele].pt>10. and abs(electrons[ele].eta)<2.4:

                            recoEle.append(ele) 
                            recoelectron = ROOT.TLorentzVector()
                            recoelectron.SetPtEtaPhiM(electrons[ele].pt, electrons[ele].eta, electrons[ele].phi, getLeptonMass(11))
                            eleVec.push_back(recoelectron)

                            recoLepton.append(ele)
                            recoLeptonID.append(11)
                            leptonVec.push_back(recoelectron)

                            #tidx = -1
 
                            #for tlep in range(events.nLepton): 
                            #    if recoleptons[tlep].electronIdx==ele:
                            #        tidx = tlep

                            #recoEleTight.append(tidx)
                  
                if 'DY' in sample:
                 
                    if len(recoMuo)==2:
                        if (muons[recoMuo[0]].charge*muons[recoMuo[1]].charge)<0.:
                            if abs((muoVec[0] + muoVec[1]).M() - Zmass)<30.:

                                for muo in range(len(recoMuo)):
                                    #if recoMuoTight[1-muo]>=0:
                                    if isTightMuon(muons[recoMuo[1-muo]]):

                                        histos[sim]['Muo']['reco'].Fill(muoVec[muo].Pt(), abs(muoVec[muo].Eta()))

                                         #if recoMuoTight[muo]>=0:
                                        if isTightMuon(muons[recoMuo[muo]]):
                                            histos[sim]['Muo']['tight'].Fill(muoVec[muo].Pt(), abs(muoVec[muo].Eta()))

                    if len(recoEle)==2:  
                        if (electrons[recoEle[0]].charge*electrons[recoEle[1]].charge)<0.:                          
                            if abs((eleVec[0] + eleVec[1]).M() - Zmass)<30.:
                                                                                                                                                        
                                for ele in range(len(recoEle)): 
                                    #if recoEleTight[1-ele]>=0:
                                    if isTightElectron(electrons[recoEle[1-ele]]):
                             
                                        etaSC = eleVec[ele].Eta() #+ electrons[recoEle[ele]].deltaEtaSC
                                                                                                                
                                        histos[sim]['Ele']['reco'].Fill(etaSC, eleVec[ele].Pt())
                                                                                           
                                        #if recoEleTight[ele]>=0: 
                                        if isTightElectron(electrons[recoEle[ele]]):
                                            histos[sim]['Ele']['tight'].Fill(etaSC, eleVec[ele].Pt())

                else:

                    if len(recoLepton)==2:
                        if recoLeptonID[0]==13: carge0 = muons[recoLepton[0]].charge
                        else: carge0 = electrons[recoLepton[0]].charge 
                        if recoLeptonID[1]==13: carge1 = muons[recoLepton[1]].charge
                        else: carge1 = electrons[recoLepton[1]].charge 
                        if carge0*carge1<0.:
                            for lep in range(len(recoLepton)):
                                isOtherTight = False
                                if recoLeptonID[1-lep]==11: isOtherTight = isTightElectron(electrons[recoLepton[1-lep]])
                                if recoLeptonID[1-lep]==13: isOtherTight = isTightMuon(muons[recoLepton[1-lep]])
                                if isOtherTight:
                                    if recoLeptonID[lep]==11:
                                        etaSC = leptonVec[lep].Eta() #+ electrons[recoLepton[lep]].deltaEtaSC
                                        histos[sim]['Ele']['reco'].Fill(etaSC, leptonVec[lep].Pt())
                                        if isTightElectron(electrons[recoLepton[lep]]):
                                            histos[sim]['Ele']['tight'].Fill(etaSC, leptonVec[lep].Pt())
                                    else:
                                        histos[sim]['Muo']['reco'].Fill(leptonVec[lep].Pt(), abs(leptonVec[lep].Eta()))
                                        if isTightMuon(muons[recoLepton[lep]]):
                                            histos[sim]['Muo']['tight'].Fill(leptonVec[lep].Pt(), abs(leptonVec[lep].Eta()))
   
            f = ROOT.TFile.Open(outputDir+'/HistoLeptons_'+campaign+'_'+sim+'_'+sample+jobFlag+'.root','recreate')

            for lepton in [ 'Ele', 'Muo' ]:
                for level in levels:
                    histos[sim][lepton][level].Write()
            
            f.Close()


