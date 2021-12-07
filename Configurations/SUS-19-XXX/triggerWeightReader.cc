#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

#include <vector>
#include <map>

#include "TVector2.h"
#include "TString.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

class TriggerWeightReader : public multidraw::TTreeFunction {
public:
  TriggerWeightReader(char const* fileName, char const* binsPt, char const* binsEta, char const* binsBTag);

  char const* getName() const override { return "TriggerWeightReader"; }
  TTreeFunction* clone() const override { return new TriggerWeightReader(fileName_.Data(), binsPt_.Data(), binsEta_.Data(), binsBTag_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return triggerWeightReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* Lepton_pt{};
  FloatArrayReader* Lepton_eta{};
  IntArrayReader*   Lepton_pdgId{};

  std::vector<double> triggerWeightReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString fileName_{};
  TString binsPt_{};
  TString binsEta_{};
  TString binsBTag_{};

  TFile* rootFile{};
  TH2F* histMuoMuoCentralTriggerWeightReader{};
  TH2F* histEleEleCentralTriggerWeightReader{};   
  TH2F* histEleMuoCentralTriggerWeightReader{};
  TH2F* histMuoMuoForwardTriggerWeightReader{};
  TH2F* histEleEleForwardTriggerWeightReader{};
  TH2F* histEleMuoForwardTriggerWeightReader{};

};

void TriggerWeightReader::beginEvent(long long _iEntry) {
  setValues();
}

TriggerWeightReader::TriggerWeightReader(char const* fileName, char const* binsPt, char const* binsEta, char const* binsBTag) :
  TTreeFunction(),
  fileName_{fileName},
  binsPt_{binsPt},
  binsEta_{binsEta},
  binsBTag_{binsBTag}
{
  rootFile = new TFile(fileName_);
  TString centralHisto = "efficiency_MET_full_"+binsBTag_+"_both";
  TString forwardHisto = "efficiency_MET_full_"+binsBTag_+"_both";
  if (binsEta_=="split") {
      centralHisto = "efficiency_MET_cent_"+binsBTag_+"_both";
      forwardHisto = "efficiency_MET_forw_"+binsBTag_+"_both";
  }
  histMuoMuoCentralTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/mm/"+centralHisto);
  histEleEleCentralTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/ee/"+centralHisto);
  histEleMuoCentralTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/em/"+centralHisto);
  histMuoMuoForwardTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/mm/"+forwardHisto);
  histEleEleForwardTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/ee/"+forwardHisto);
  histEleMuoForwardTriggerWeightReader = (TH2F*)rootFile->Get(binsPt_+"/em/"+forwardHisto);
}

double
TriggerWeightReader::evaluate(unsigned iJ) {
  return triggerWeightReader[iJ];
}

void TriggerWeightReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Lepton_pt, "Lepton_pt");
  _library.bindBranch(Lepton_eta, "Lepton_eta");
  _library.bindBranch(Lepton_pdgId, "Lepton_pdgId");
}

void TriggerWeightReader::setValues() {

  triggerWeightReader.clear();

  float triggerWeight = -1.;
  double LeadingLeptonPt{Lepton_pt->At(0)};
  double TrailingLeptonPt{Lepton_pt->At(1)};
  double LeadingLeptonEta{Lepton_eta->At(0)};
  int LeadingLeptonId{Lepton_pdgId->At(0)};
  int TrailingLeptonId{Lepton_pdgId->At(1)};
  int channel = LeadingLeptonId*TrailingLeptonId;

  if (abs(channel)==121) {
      if (fabs(LeadingLeptonEta)<=1.2) {
          triggerWeight = this->GetBinContent4Weight(histEleEleCentralTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      } else {
          triggerWeight = this->GetBinContent4Weight(histEleEleForwardTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      }
  } else if (abs(channel)==169) {
      if (fabs(LeadingLeptonEta)<=1.2) {
          triggerWeight = this->GetBinContent4Weight(histMuoMuoCentralTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      } else {
          triggerWeight = this->GetBinContent4Weight(histMuoMuoForwardTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      }
  } else if (abs(channel)==143) {
      if (fabs(LeadingLeptonEta)<=1.2) {
          triggerWeight = this->GetBinContent4Weight(histEleMuoCentralTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      } else {
          triggerWeight = this->GetBinContent4Weight(histEleMuoForwardTriggerWeightReader, LeadingLeptonPt, TrailingLeptonPt, 0);
      }
  }

  if (triggerWeight<=0.) 
      std::cout << "TriggerWeightReader Error for " << channel << " " << LeadingLeptonPt << " " << TrailingLeptonPt << " " << LeadingLeptonEta << std::endl;

  triggerWeightReader.push_back(triggerWeight);

}

double TriggerWeightReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){

  double xmin=hist->GetXaxis()->GetXmin();
  double xmax=hist->GetXaxis()->GetXmax();
  double ymin=hist->GetYaxis()->GetXmin();
  double ymax=hist->GetYaxis()->GetXmax();
  if(xmin>=0) valx=fabs(valx);
  if(valx<xmin) valx=xmin+0.001;
  if(valx>xmax) valx=xmax-0.001;
  if(ymin>=0) valy=fabs(valy);
  if(valy<ymin) valy=ymin+0.001;
  if(valy>ymax) valy=ymax-0.001;
  float weight = hist->GetBinContent(hist->FindBin(valx,valy));
  if (sys!=0) {
    weight += sys*hist->GetBinError(hist->FindBin(valx,valy));
  }
  return weight;
}
    


