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

class PileupWeightsReader : public multidraw::TTreeFunction {
public:
  PileupWeightsReader(char const* weightFileName);

  char const* getName() const override { return "PileupWeightsReader"; }
  TTreeFunction* clone() const override { return new PileupWeightsReader(weightFileName_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return pileupWeightsReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;

  FloatArrayReader* nPUtrue{};

  std::vector<double> pileupWeightsReader{};
  void setValues();
  double GetBinContent4Weight(TH1* hist, double valx);

  TString weightFileName_{};

  TFile* weightFile{};
  TH2F*  pileupWeightsHisto{};
  TH2F*  pileupWeightsUpHisto{};
  TH2F*  pileupWeightsDownHisto{};

};

void PileupWeightsReader::beginEvent(long long _iEntry) {
  setValues();
}

PileupWeightsReader::PileupWeightsReader(char const* weightFileName) :
  TTreeFunction(),
  weightFileName_{weightFileName}
{
  weightFile = new TFile(weightFileName_);
  pileupWeightsHisto     = (TH2F*)weightFile->Get("pileup");
  pileupWeightsUpHisto   = (TH2F*)weightFile->Get("pileup_plus");
  pileupWeightsDownHisto = (TH2F*)weightFile->Get("pileup_minus");
}

double
PileupWeightsReader::evaluate(unsigned iJ) {
  return pileupWeightsReader[iJ];
}

void PileupWeightsReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nPUtrue, "nPUtrue");
}

void PileupWeightsReader::setValues() {

  pileupWeightsReader.clear();

  float nTruePU{nPUtrue->At(0)}; 

  for (int pusyst = -1; pusyst<=1; pusyst++) {

    double pileupWeight = -1.;
    if (pusyst==-1) pileupWeight = this->GetBinContent4Weight(pileupWeightsDownHisto, nTruePU);
    if (pusyst==0)  pileupWeight = this->GetBinContent4Weight(pileupWeightsHisto,     nTruePU);
    if (pusyst==1)  pileupWeight = this->GetBinContent4Weight(pileupWeightsUpHisto,   nTruePU);

    if (pileupWeight<=0.) 
      std::cout << "PileupWeightsReader Error for " << weightFileName_ << " " << nTruePU << std::endl;

    pileupWeightsReader.push_back(pileupWeight);

  }

}

double PileupWeightsReader::GetBinContent4Weight(TH1* hist, double valx){

  double xmin=hist->GetXaxis()->GetXmin();
  double xmax=hist->GetXaxis()->GetXmax();
  if(xmin>=0) valx=fabs(valx);
  if(valx<xmin) valx=xmin+0.001;
  if(valx>xmax) valx=xmax-0.001;
  return hist->GetBinContent(hist->FindBin(valx));

}
 
