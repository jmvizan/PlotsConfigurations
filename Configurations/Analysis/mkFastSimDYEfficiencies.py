#!/usr/bin/env python
import os
import sys
import ROOT
import math
import optparse
from array import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

Zmass = 91.1876

yearset=sys.argv[1]
prodset=sys.argv[2]
maxentries=int(sys.argv[3])

campaign = 'UL'
#treeLevel = 'DY'
treeLevel = ''

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
        treeDir = 'XXX_102X_nAODv6_Full201Yv6loose/SFSusy201Y'+treeLevel+'v6loose/'

        years = { '2016' : { 'fastsim' : eosusr+treeDir.replace('XXX', 'Summer16FS').replace('201Y', '2016'), 
       	                     'fullsim' : eosusr+treeDir.replace('XXX', 'Summer16').replace('201Y', '2016')    } ,  
                  '2017' : { 'fastsim' : eosusr+treeDir.replace('XXX', 'Fall2017FS').replace('201Y', '2017'), 
                             'fullsim' : eoscaf+treeDir.replace('XXX', 'Fall2017').replace('201Y', '2017')    } ,  
                  '2018' : { 'fastsim' : eoscaf+treeDir.replace('XXX', 'Autumn18FS').replace('201Y', '2018'),  
                             'fullsim' : eoscaf+treeDir.replace('XXX', 'Autumn18').replace('201Y', '2018')    } }
    elif campaign=='UL':

        eosusr = '/eos/home-p/pmatorra/SUS_SF/'
        eoscaf = '/eos/home-p/pmatorra/SUS_SF/'
        #eosusr = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
        #eoscaf = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'

        treeName = 'nanoLatino_DYJetsToLL_M-50-LO__part*root'

        years = { '2016HIPM'   : { 'fastsim' : eosusr+'Spring21UL16FS_106X_nAODv9_Full2016v8/SFSusyDY/',
                                   'fullsim' : eosusr+'Summer20UL16_106X_nAODv9_HIPM_Full2016v8/SFSusyDY/',    } ,
                  '2016noHIPM' : { 'fastsim' : eosusr+'Spring21UL16FS_106X_nAODv9_Full2016v8/SFSusyDY/',
                                   'fullsim' : eosusr+'Summer20UL16_106X_nAODv9_noHIPM_Full2016v8/SFSusyDY/',    } ,
                  '2017'       : { 'fastsim' : eosusr+'Spring21UL17FS_106X_nAODv9_Full2017v8/SFSusyDY/',
                                   'fullsim' : eosusr+'Summer20UL17_106X_nAODv9_Full2017v8/SFSusyDY/',    } ,
                  '2018'       : { 'fastsim' : eosusr+'Spring21UL18FS_106X_nAODv9_Full2018v8/SFSusyDY/',
                                   'fullsim' : eosusr+'Summer20UL18_106X_nAODv9_Full2018v8/SFSusyDY/',    } , }
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
              'Ele' : [ -2.400, -1.444, -0.800,  0.000, 0.800, 1.444, 2.400 ] }
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

        for sim in prodset.split('-'):

            events = ROOT.TChain('Events') 
            events.Add(years[year][sim]+treeName)

            histos[sim] = { }
            for lepton in [ 'Ele', 'Muo' ]:
  
                histos[sim][lepton] = { }
                for level in levels: 
                    histos[sim][lepton][level] = ROOT.TH2F(lepton+'_'+level+'_'+sim, '', len(binsx[lepton])-1, array('d',binsx[lepton]), len(binsy[lepton])-1, array('d',binsy[lepton]))                                                                                            
            nentries = events.GetEntries()            
            print maxentries, nentries
            if maxentries>0. and maxentries<nentries:
                nentries = maxentries

            print year, sim, nentries 
            for entry in range(nentries):

                events.GetEntry(entry)

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
                            if abs(lepMotherPdgId)!=23: continue

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
                        if abs(genLepPdgId[0])==abs(genLepPdgId[1]):
                            if (genLepPdgId[0]*genLepPdgId[1])<0.: 
                                if abs((genVec[0] + genVec[1]).M() - Zmass)<30.:
               
                                    #lepton = 'Ele' if abs(genleptons[genLep[0]].pdgId)==11 else 'Muo'
                                    lepton = 'Ele' if abs(genLepPdgId[0])==11 else 'Muo'
                                    isLeptonTight = []
                                    for glep in range(len(genLep)):
                                        if genLepReco[glep]>=0:
                                            if lepton=='Ele': isLeptonTight.append(isTightElectron(electrons[genLepReco[glep]]))
                                            if lepton=='Muo': isLeptonTight.append(isTightMuon(muons[genLepReco[glep]]))
                                        else: isLeptonTight.append(False)

                                    for glep in range(len(genLep)):
                                        #if genLepTight[1-glep]>=0:
                                        #if (lepton=='Ele' and isTightElectron(electrons[])) or (lepton=='Muo' and ):
                                        if isLeptonTight[1-glep]:

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

                            #tidx = -1
                            
                            #for tlep in range(events.nLepton): 
                            #    if recoleptons[tlep].muonIdx==muo:  
                            #        tidx = tlep 
         
                            #recoMuoTight.append(tidx)

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

                            #tidx = -1
 
                            #for tlep in range(events.nLepton): 
                            #    if recoleptons[tlep].electronIdx==ele:
                            #        tidx = tlep

                            #recoEleTight.append(tidx)

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

            f = ROOT.TFile.Open(outputDir+'/HistoLeptons_'+campaign+'_'+sim+'.root','recreate')

            for lepton in [ 'Ele', 'Muo' ]:
                for level in levels:
                    histos[sim][lepton][level].Write()
            
            f.Close()


