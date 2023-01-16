#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

#include <vector>
#include <map>

#include "TVector2.h"
#include "TLorentzVector.h"
#include "TString.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "Math/Vector4Dfwd.h"
//#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

class DecayAngleCME : public multidraw::TTreeFunction {
public:
  DecayAngleCME();

  char const* getName() const override { return "DecayAngleCME"; }
  TTreeFunction* clone() const override { return new DecayAngleCME(); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return decayAngleCME.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  UIntArrayReader*  nGenPart{};
  FloatArrayReader* GenPart_pt{};
  FloatArrayReader* GenPart_eta{};
  FloatArrayReader* GenPart_phi{};
  FloatArrayReader* GenPart_mass{};
  IntArrayReader*   GenPart_pdgId{};
  IntArrayReader*   GenPart_genPartIdxMother{};

  int nEvt;
  int plusB;
  int minusB;

  std::vector<double> decayAngleCME{};
  void setValues();
  
};

void DecayAngleCME::beginEvent(long long _iEntry) {
  setValues();
}

DecayAngleCME::DecayAngleCME() :
  TTreeFunction(),
  nEvt{0},
  plusB{0},
  minusB{0}
{
}

double
DecayAngleCME::evaluate(unsigned iJ) {
  return decayAngleCME[iJ];
}

void DecayAngleCME::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nGenPart, "nGenPart");
  _library.bindBranch(GenPart_pt, "GenPart_pt");
  _library.bindBranch(GenPart_eta, "GenPart_eta");
  _library.bindBranch(GenPart_phi, "GenPart_phi");
  _library.bindBranch(GenPart_mass, "GenPart_mass");
  _library.bindBranch(GenPart_pdgId, "GenPart_pdgId");
  _library.bindBranch(GenPart_genPartIdxMother, "GenPart_genPartIdxMother");
}

void DecayAngleCME::setValues() {

  decayAngleCME.clear();

  double decayAnglePlusSusy  = -999.;
  double decayAnglePlusSM    = -999.;
  double decayAngleMinusSusy = -999.; 
  double decayAngleMinusSM   = -999.;

  double boostedDecayAnglePlusSusy  = -999.;
  double boostedDecayAnglePlusSM    = -999.;
  double boostedDecayAngleMinusSusy = -999.;
  double boostedDecayAngleMinusSM   = -999.;
 
  double promptPlusPt   = -999.;
  double promptPlusEta  = -999.;
  double promptPlusPhi  = -999.;
  double promptPlusMass = -999.;

  double promptMinusPt   = -999.;
  double promptMinusEta  = -999.;
  double promptMinusPhi  = -999.;
  double promptMinusMass = -999.;

  double lastPromptPlusPt   = -999.;
  double lastPromptPlusEta  = -999.;
  double lastPromptPlusPhi  = -999.;
  double lastPromptPlusMass = -999.;
  
  double lastPromptMinusPt   = -999.;
  double lastPromptMinusEta  = -999.;
  double lastPromptMinusPhi  = -999.;
  double lastPromptMinusMass = -999.;

  double plusSusyPt   = -999.;
  double plusSMPt     = -999.;
  double minusSusyPt  = -999.;
  double minusSMPt    = -999.;

  double plusSusyMass   = -999.;
  double plusSMMass     = -999.;
  double minusSusyMass  = -999.;
  double minusSMMass    = -999.;

  double cmePlusSusyPt   = -999.;
  double cmePlusSMPt     = -999.;
  double cmeMinusSusyPt  = -999.;
  double cmeMinusSMPt    = -999.;

  double cmePlusSusyMass   = -999.;
  double cmePlusSMMass     = -999.;
  double cmeMinusSusyMass  = -999.;
  double cmeMinusSMMass    = -999.;

  double cmePlusSusyP     = -999.;
  double cmeMinusSusyP    = -999.;
  double cmePlusSMP       = -999.;
  double cmeMinusSMP      = -999.;

  double lspPlusMass  = -999.;
  double lspMinusMass = -999.;

  TLorentzVector plusResidualP;     plusResidualP.SetPtEtaPhiM(0., 0., 0., 0.);
  TLorentzVector minusResidualP;    minusResidualP.SetPtEtaPhiM(0., 0., 0., 0.);
  TLorentzVector cmePlusResidualP;  cmePlusResidualP.SetPtEtaPhiM(0., 0., 0., 0.);
  TLorentzVector cmeMinusResidualP; cmeMinusResidualP.SetPtEtaPhiM(0., 0., 0., 0.);

  int nPlusDaus    =  0;
  int idxPlusSusy  = -1;
  int idxPlusSM    = -1;
  int nMinusDaus   =  0;
  int idxMinusSusy = -1;
  int idxMinusSM   = -1;

  int idxMotherPlusSusy  = -1;
  int idxMotherPlusSM    = -1;
  int idxMotherMinusSusy = -1;
  int idxMotherMinusSM   = -1;

  for (unsigned int part = 0; part<nGenPart->At(0); part++) {
    
    int partMother{GenPart_genPartIdxMother->At(part)};
    if (partMother>=0) {

      int partID{GenPart_pdgId->At(part)};
      int partMotherID{GenPart_pdgId->At(partMother)};

      if (fabs(partID)>=1000000 && fabs(partID)<=2001000) {
        if (fabs(partMotherID)<1000000) { 

          if (partID>0) {
            promptPlusPt   = GenPart_pt->At(part);
            promptPlusEta  = GenPart_eta->At(part);
            promptPlusPhi  = GenPart_phi->At(part);
            promptPlusMass = GenPart_mass->At(part);
          } else {
            promptMinusPt   = GenPart_pt->At(part);
            promptMinusEta  = GenPart_eta->At(part);
            promptMinusPhi  = GenPart_phi->At(part);
            promptMinusMass = GenPart_mass->At(part);
          }

          int promptFilled = 0;
          int cmePromptFilled = 0;
 
          for (unsigned int dau = 0; dau<nGenPart->At(0); dau++) {

            int dauID{GenPart_pdgId->At(dau)};
            int dauMother{GenPart_genPartIdxMother->At(dau)};
            int dauMotherID{GenPart_pdgId->At(dauMother)};

            if (dauID!=partID && dauMotherID==partID) {

              for (unsigned int lspp = 0; lspp<nGenPart->At(0); lspp++) {
                if (abs(GenPart_pdgId->At(lspp))==1000022) {
                  int lspMother{GenPart_genPartIdxMother->At(lspp)};
                  int lspMotherID{GenPart_pdgId->At(lspMother)};
                  if (lspMotherID==dauID) {
                    if (dauMotherID>0) lspPlusMass = GenPart_mass->At(lspp);
                    else lspMinusMass = GenPart_mass->At(lspp);
                  }
                }
              }
              
              double motherEta{GenPart_eta->At(dauMother)};
              double motherPt{GenPart_pt->At(dauMother)};
              double motherPhi{GenPart_phi->At(dauMother)};
              double motherMass{GenPart_mass->At(dauMother)};

              if (partID>0) {
                lastPromptPlusPt   = motherPt;
                lastPromptPlusEta  = motherEta;
                lastPromptPlusPhi  = motherPhi;
                lastPromptPlusMass = motherMass;
              } else {
                lastPromptMinusPt   = motherPt;
                lastPromptMinusEta  = motherEta;
                lastPromptMinusPhi  = motherPhi;
                lastPromptMinusMass = motherMass;
              } 

              TLorentzVector prompt;
              prompt.SetPtEtaPhiM(motherPt, motherEta, motherPhi, motherMass);
              if (partID>0.) {
                  if (promptFilled==0) {
                      plusResidualP.SetPtEtaPhiM(motherPt, motherEta, motherPhi, motherMass);
                      promptFilled = 1;
                  }
              } else if (partID<0.) {
                  if (promptFilled==0) {
                      minusResidualP.SetPtEtaPhiM(motherPt, motherEta, motherPhi, motherMass);
                      promptFilled = 1;
                  }
              }

              TVector3 promptBoost = prompt.BoostVector();
         
              double dauEta{GenPart_eta->At(dau)};
              double dauPt{GenPart_pt->At(dau)};
              double dauPhi{GenPart_phi->At(dau)};
              double dauMass{GenPart_mass->At(dau)};

              TLorentzVector sdau;
              sdau.SetPtEtaPhiM(dauPt, dauEta, dauPhi, dauMass);

              if (dauMotherID>0) plusResidualP -= sdau;
              else minusResidualP -= sdau;

              double boostedDeltaPhi = sdau.DeltaPhi(prompt);

              sdau.Boost(-promptBoost);

              double cmeDauPt   = sdau.Pt();
              double cmeDauP    = sdau.P();
              double cmeDauMass = sdau.M();
              double deltaPhi = sdau.DeltaPhi(prompt);
              
              if (partID>0.) {
                  if (cmePromptFilled==0) {
                      cmePlusResidualP.SetPtEtaPhiM(motherPt, motherEta, motherPhi, motherMass);
                      cmePlusResidualP.Boost(-promptBoost);
                      cmePromptFilled = 1;
                  }
                  cmePlusResidualP -= sdau;
              } else if (partID<0.) {
                  if (cmePromptFilled==0) {
                      cmeMinusResidualP.SetPtEtaPhiM(motherPt, motherEta, motherPhi, motherMass);
                      cmeMinusResidualP.Boost(-promptBoost);
                      cmePromptFilled = 1;
                  }
                  cmeMinusResidualP -= sdau;
              }

              if (fabs(dauID)>=1000000 && fabs(dauID)<=2001000) {
                if (dauMotherID>0) {
                  nPlusDaus += 1;
                  idxPlusSusy = dau;
                  idxMotherPlusSusy = dauMother;
                  plusSusyPt      = dauPt;
                  plusSusyMass    = dauMass;
                  cmePlusSusyPt   = cmeDauPt;
                  cmePlusSusyMass = cmeDauMass;
                  cmePlusSusyP    = cmeDauP;
                  boostedDecayAnglePlusSusy = boostedDeltaPhi;
                  decayAnglePlusSusy = deltaPhi;
                } else {
                  nMinusDaus += 1;
                  idxMinusSusy = dau;
                  idxMotherMinusSusy = dauMother;
                  minusSusyPt      = dauPt;
                  minusSusyMass    = dauMass;
                  cmeMinusSusyPt   = cmeDauPt;
                  cmeMinusSusyMass = cmeDauMass;
                  cmeMinusSusyP    = cmeDauP;
                  boostedDecayAngleMinusSusy = boostedDeltaPhi;
                  decayAngleMinusSusy = deltaPhi; 
                }
              } else {
                if (dauMotherID>0) {
                  nPlusDaus += 1;
                  idxPlusSM = dau;
                  idxMotherPlusSM  = dauMother;
                  plusSMPt      = dauPt;
                  plusSMMass    = dauMass;
                  cmePlusSMPt   = cmeDauPt;
                  cmePlusSMMass = cmeDauMass;
                  cmePlusSMP    = cmeDauP;
                  boostedDecayAnglePlusSM = boostedDeltaPhi;
                  decayAnglePlusSM = deltaPhi;
                } else {
                  nMinusDaus += 1;
                  idxMinusSM = dau;
                  idxMotherMinusSM  = dauMother;
                  minusSMPt      = dauPt;
                  minusSMMass    = dauMass;
                  cmeMinusSMPt   = cmeDauPt;
                  cmeMinusSMMass = cmeDauMass;
                  cmeMinusSMP    = cmeDauP;
                  boostedDecayAngleMinusSM = boostedDeltaPhi;
                  decayAngleMinusSM = deltaPhi;
                }
              }

            }                    

          }

        }
      }

    }

  }

  nEvt += 1;

  bool debug = false;

  if (debug) {

    if (decayAnglePlusSusy<-10. || decayAnglePlusSM<-10. || decayAngleMinusSusy<-10. || decayAngleMinusSM<-10.)
      std::cout << "decayAngleCME Error: missing angle" << std::endl;

    if (cos(fabs(decayAnglePlusSusy-decayAnglePlusSM))>-0.9) {
      plusB += 1;
      std::cout << "decayAngleCME Error: plus angles not opposed: " << decayAnglePlusSusy << " " << decayAnglePlusSM << " " << cos(fabs(decayAnglePlusSusy-decayAnglePlusSM))  << " " << plusB << "/"<< nEvt << std::endl;
      std::cout << "                                              " << idxPlusSusy << " " << idxMotherPlusSusy << " " << idxPlusSM << " " << idxMotherPlusSM << " " << nPlusDaus << std::endl;
      std::cout << "                                              " << GenPart_pdgId->At(idxPlusSusy) << " " << GenPart_pdgId->At(idxMotherPlusSusy) << " " << GenPart_pdgId->At(idxPlusSM) << " " << GenPart_pdgId->At(idxMotherPlusSM) << std::endl;
    }

    if (cos(fabs(decayAngleMinusSusy-decayAngleMinusSM))>-0.9) {
      minusB += 1;
      std::cout << "decayAngleCME Error: minus angles not opposed: " << decayAngleMinusSusy << " " << decayAngleMinusSM << " " << cos(fabs(decayAngleMinusSusy-decayAngleMinusSM)) << " " << minusB << "/"<< nEvt << std::endl;
      std::cout << "                                              " << idxMinusSusy << " " << idxMotherMinusSusy << " " << idxMinusSM << " " << idxMotherMinusSM << " " << nMinusDaus << std::endl;
      std::cout << "                                              " << GenPart_pdgId->At(idxMinusSusy) << " " << GenPart_pdgId->At(idxMotherMinusSusy) << " " << GenPart_pdgId->At(idxMinusSM) << " " << GenPart_pdgId->At(idxMotherMinusSM) << std::endl;
    }

  }

  decayAngleCME.push_back(decayAnglePlusSusy);
  decayAngleCME.push_back(decayAnglePlusSM);
  decayAngleCME.push_back(decayAngleMinusSusy);
  decayAngleCME.push_back(decayAngleMinusSM);

  decayAngleCME.push_back(boostedDecayAnglePlusSusy);
  decayAngleCME.push_back(boostedDecayAnglePlusSM);
  decayAngleCME.push_back(boostedDecayAngleMinusSusy);
  decayAngleCME.push_back(boostedDecayAngleMinusSM);

  decayAngleCME.push_back(promptPlusPt);
  decayAngleCME.push_back(promptPlusEta);
  decayAngleCME.push_back(promptPlusPhi);
  decayAngleCME.push_back(promptPlusMass);
 
  decayAngleCME.push_back(promptMinusPt);
  decayAngleCME.push_back(promptMinusEta);
  decayAngleCME.push_back(promptMinusPhi);
  decayAngleCME.push_back(promptMinusMass);

  decayAngleCME.push_back(lastPromptPlusPt);
  decayAngleCME.push_back(lastPromptPlusEta);
  decayAngleCME.push_back(lastPromptPlusPhi);
  decayAngleCME.push_back(lastPromptPlusMass);

  decayAngleCME.push_back(lastPromptMinusPt);
  decayAngleCME.push_back(lastPromptMinusEta);
  decayAngleCME.push_back(lastPromptMinusPhi);
  decayAngleCME.push_back(lastPromptMinusMass);

  decayAngleCME.push_back(plusSusyPt);
  decayAngleCME.push_back(plusSMPt);
  decayAngleCME.push_back(minusSusyPt);
  decayAngleCME.push_back(minusSMPt);

  decayAngleCME.push_back(plusSusyMass);
  decayAngleCME.push_back(plusSMMass);
  decayAngleCME.push_back(minusSusyMass);
  decayAngleCME.push_back(minusSMMass);

  decayAngleCME.push_back(cmePlusSusyPt);
  decayAngleCME.push_back(cmePlusSMPt);
  decayAngleCME.push_back(cmeMinusSusyPt);
  decayAngleCME.push_back(cmeMinusSMPt);

  decayAngleCME.push_back(cmePlusSusyMass);
  decayAngleCME.push_back(cmePlusSMMass);
  decayAngleCME.push_back(cmeMinusSusyMass);
  decayAngleCME.push_back(cmeMinusSMMass);

  decayAngleCME.push_back(cmePlusSusyP);
  decayAngleCME.push_back(cmePlusSMP);
  decayAngleCME.push_back(cmeMinusSusyP);
  decayAngleCME.push_back(cmeMinusSMP);

  decayAngleCME.push_back(plusResidualP.P());
  decayAngleCME.push_back(plusResidualP.E());
  decayAngleCME.push_back(minusResidualP.P());
  decayAngleCME.push_back(minusResidualP.E());

  decayAngleCME.push_back(cmePlusResidualP.P());
  decayAngleCME.push_back(cmePlusResidualP.E());
  decayAngleCME.push_back(cmeMinusResidualP.P());
  decayAngleCME.push_back(cmeMinusResidualP.E());

  decayAngleCME.push_back(lspPlusMass);
  decayAngleCME.push_back(lspMinusMass);
}
