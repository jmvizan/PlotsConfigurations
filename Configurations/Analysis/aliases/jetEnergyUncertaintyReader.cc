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

class JetEnergyUncertaintyReader : public multidraw::TTreeFunction {
public:
  JetEnergyUncertaintyReader(char const* jeuFileName, char const* jeuVar);

  char const* getName() const override { return "JetEnergyUncertaintyReader"; }
  TTreeFunction* clone() const override { return new JetEnergyUncertaintyReader(jeuFileName_.Data(), jeuVar_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return jetEnergyUncertaintyReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
 
  IntArrayReader*  nJet{}; 
  FloatArrayReader* Jet_pT{};
  FloatArrayReader* Jet_eta{};

  std::vector<double> jetEnergyUncertaintyReader{};
  void setValues();

  TString jeuFileName_{};
  TString jeuVar_{};

  int nJEUEtaBin, nJEUPtPoint;

  static const int nJEUEtaBins = 100, nJEUPtPoints = 100;
  float JEUEtaEdge[nJEUEtaBins][2];
  float JEUPtPoint[nJEUPtPoints];
  float Jet_JEU[nJEUEtaBins][nJEUPtPoints][2];
  int BhoFactor = 150;

};

void JetEnergyUncertaintyReader::beginEvent(long long _iEntry) {
  setValues();
}

JetEnergyUncertaintyReader::JetEnergyUncertaintyReader(char const* jeuFileName, char const* jeuVar) :
  TTreeFunction(),
  jeuFileName_{jeuFileName},
  jeuVar_{jeuVar}
{
  ifstream jeuFile; jeuFile.open(jeuFileName_);
  if (!jeuFile) throw std::invalid_argument("JEU file not found!");

  nJEUEtaBin = 0;

  std::string delimiter = " ";

  std::string line;

  while (std::getline(jeuFile, line)) {

    if (line.find("{")!=std::string::npos) continue;

    nJEUPtPoint = 0;

    int ntoken = 0;
    size_t pos = 0;
    std::string token;

    while ((pos = line.find(delimiter)) != std::string::npos) {
      token = line.substr(0, pos);
      if (ntoken==0) JEUEtaEdge[nJEUEtaBin][0] = atof(token.c_str());
      else if (ntoken==1) JEUEtaEdge[nJEUEtaBin][1] = atof(token.c_str());
      else if (ntoken==2) {
        if (atoi(token.c_str())!=150) throw std::invalid_argument("Bad bho value reading JEU file"); 
      } else {
        if (ntoken%3==0) {
          JEUPtPoint[nJEUPtPoint] = atof(token.c_str());
        } else if (ntoken%3==1) {
          Jet_JEU[nJEUEtaBin][nJEUPtPoint][0] = atof(token.c_str()); 
        } else if (ntoken%3==2) {
          Jet_JEU[nJEUEtaBin][nJEUPtPoint][1] = atof(token.c_str());
          if (Jet_JEU[nJEUEtaBin][nJEUPtPoint][0]!=Jet_JEU[nJEUEtaBin][nJEUPtPoint][1]) throw std::invalid_argument("Asymmetric uncertainties reading JEU file");
          nJEUPtPoint++;
        } 
      }
      line.erase(0, pos + delimiter.length());
      ntoken++;
    }

    nJEUEtaBin++;

  }

}

double
JetEnergyUncertaintyReader::evaluate(unsigned iJ) {
  return jetEnergyUncertaintyReader[iJ];
}

void JetEnergyUncertaintyReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nJet,    "nJet");
  _library.bindBranch(Jet_pT,  "Jet_pT");
  _library.bindBranch(Jet_eta, "Jet_eta");
}

void JetEnergyUncertaintyReader::setValues() {

  jetEnergyUncertaintyReader.clear();

  for (int ijet = 0; ijet<nJet->At(0); ijet++) { 

    double JetPt{Jet_pT->At(ijet)};
    double JetEta{Jet_eta->At(ijet)};

    double jetEnergyUncertaintyValue = -1.;

    for (int ib = 0; ib<nJEUEtaBin; ib++)
      if (JetEta>=JEUEtaEdge[ib][0] && JetEta<JEUEtaEdge[ib][1])
        for (int ipt = 0; ipt<nJEUPtPoint; ipt++)
          if (JetPt>=JEUPtPoint[ipt]) jetEnergyUncertaintyValue = Jet_JEU[ib][ipt][0];

    if (jetEnergyUncertaintyValue<=0.) 
      std::cout << "JetEnergyUncertaintyReader Error for " << jeuFileName_ << " " << JetPt << " " << JetEta << " " << jetEnergyUncertaintyValue << std::endl;

    if (jeuVar_=="down") jetEnergyUncertaintyReader.push_back(JetPt*(1.-jetEnergyUncertaintyValue));
    else if (jeuVar_=="up") jetEnergyUncertaintyReader.push_back(JetPt*(1.+jetEnergyUncertaintyValue));

  }

}

 
