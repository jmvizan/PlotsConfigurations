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

class KinematicWeightsReader : public multidraw::TTreeFunction {
public:
  KinematicWeightsReader(char const* weightFile, char const* histoName);

  char const* getName() const override { return "KinematicWeightsReader"; }
  TTreeFunction* clone() const override { return new KinematicWeightsReader(weightFile_.Data(), histoName_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return kinematicWeightsReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* muJet_pt{};
  FloatArrayReader* muJet_eta{};

  std::vector<double> kinematicWeightsReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString weightFile_{};
  TString histoName_{};

  TFile* rootFile{};
  TH2F*  kinematicWeightsHisto{};

};

void KinematicWeightsReader::beginEvent(long long _iEntry) {
  setValues();
}

KinematicWeightsReader::KinematicWeightsReader(char const* weightFile, char const* histoName) :
  TTreeFunction(),
  weightFile_{weightFile},
  histoName_{histoName}
{
  rootFile = new TFile(weightFile_);
  kinematicWeightsHisto = (TH2F*)rootFile->Get(histoName_);
}

double
KinematicWeightsReader::evaluate(unsigned iJ) {
  return kinematicWeightsReader[iJ];
}

void KinematicWeightsReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(muJet_pt,  "muJet_pt");
  _library.bindBranch(muJet_eta, "muJet_eta");
}

void KinematicWeightsReader::setValues() {

  kinematicWeightsReader.clear();

  double muJetPt{muJet_pt->At(0)};
  double muJetEta{muJet_eta->At(0)};

  double kinematicWeight = this->GetBinContent4Weight(kinematicWeightsHisto, muJetPt, muJetEta, 0);

  if (kinematicWeight<=0.) 
      std::cout << "KinematicWeightsReader Error for " << weightFile_ << " " << histoName_ << " " << muJetPt << " " << muJetEta << std::endl;

  kinematicWeightsReader.push_back(kinematicWeight);

}

double KinematicWeightsReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){

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
 
