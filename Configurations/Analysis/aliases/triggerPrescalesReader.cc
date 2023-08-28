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
#include <sstream>
#include <fstream>
#include <string>

class TriggerPrescalesReader : public multidraw::TTreeFunction {
public:
  TriggerPrescalesReader(char const* prescaleFileName);

  char const* getName() const override { return "TriggerPrescalesReader"; }
  TTreeFunction* clone() const override { return new TriggerPrescalesReader(prescaleFileName_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return triggerPrescalesReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;

  UIntArrayReader*  Run{};
  UIntArrayReader*  LumiBlock{};

  std::vector<double> triggerPrescalesReader{};
  void setValues();

  TString prescaleFileName_{};
  ifstream prescaleFile{};

  int nPrescales;

  static const int nMaxPrescales = 8000;
  unsigned int triggerPrescaleRunNumber[nMaxPrescales]{};
  unsigned int triggerPrescaleLumiSection[nMaxPrescales]{};
  float triggerPrescaleValue[nMaxPrescales]{};

};

void TriggerPrescalesReader::beginEvent(long long _iEntry) {
  setValues();
}

TriggerPrescalesReader::TriggerPrescalesReader(char const* prescaleFileName) :
  TTreeFunction(),
  prescaleFileName_{prescaleFileName}
{
  prescaleFile.open(prescaleFileName_);
  if (!prescaleFile) throw std::invalid_argument("Prescale weights not found!");

  nPrescales = 0;

  std::string delimiter = ",";

  int runNumber = -1, lumiSection = -1; float triggerPrescale = -1.;

  std::string line;

  while (prescaleFile) {

    prescaleFile >> line;

    if (line.find("#")!=std::string::npos) continue;

    int ntoken = 0;
    size_t pos = 0;
    std::string token;
    while ((pos = line.find(delimiter)) != std::string::npos) {
      token = line.substr(0, pos);
      if (ntoken==0) runNumber = atoi(token.c_str());
      if (ntoken==1) lumiSection = atoi(token.c_str());
      if (ntoken==3) triggerPrescale = atof(token.c_str());
      line.erase(0, pos + delimiter.length());
      ntoken++;
    }

    if (runNumber>0 && lumiSection>0 && triggerPrescale>0.) {

      triggerPrescaleRunNumber[nPrescales] = runNumber;
      triggerPrescaleLumiSection[nPrescales] = lumiSection;
      triggerPrescaleValue[nPrescales] = triggerPrescale;
      nPrescales++;

    }

  }

  if (nPrescales>nMaxPrescales)
    std::cout << "TriggerPrescalesReader: ERROR -> need to increase nMaxPrescales " << std::endl;

}

double
TriggerPrescalesReader::evaluate(unsigned iJ) {
  return triggerPrescalesReader[iJ];
}

void TriggerPrescalesReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Run, "Run");
  _library.bindBranch(LumiBlock, "LumiBlock");
}

void TriggerPrescalesReader::setValues() {

  triggerPrescalesReader.clear();

  unsigned int run{Run->At(0)}; 
  unsigned int lumiblock{LumiBlock->At(0)};

  float triggerPrescale = -1.;

  for (int ps = 0; ps<nPrescales; ps++)
    if (run==triggerPrescaleRunNumber[ps] && lumiblock>=triggerPrescaleLumiSection[ps])  
      triggerPrescale = triggerPrescaleValue[ps];

  if (triggerPrescale<0.)
    std::cout << "TriggerPrescalesReader Error for " << prescaleFileName_ << " " << run << " " << lumiblock << " " << triggerPrescale << std::endl;

  triggerPrescalesReader.push_back(triggerPrescale);

}

