#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"
#include <vector>
#include <map>

#include "TVector2.h"
#include "TString.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "TGraph.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

class BFragmentationWeightsReader : public multidraw::TTreeFunction {
public:
  BFragmentationWeightsReader(char const* bfragWeightFile, char const* histoName, char const* bdecayWeightFile);

  char const* getName() const override { return "BFragmentationWeightsReader"; }
  TTreeFunction* clone() const override { return new BFragmentationWeightsReader(bfragWeightFile_.Data(), histoName_.Data(), bdecayWeightFile_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return bFragmentationWeightsReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
 
  IntArrayReader*    nPFMuon{};
  DoubleArrayReader* PFMuon_pt{};
  DoubleArrayReader* PFMuon_eta{};
  LongArrayReader*   PFMuon_GoodQuality{};
  LongArrayReader*   PFMuon_IdxJet{};
  IntArrayReader*    nJet{}; 
  FloatArrayReader*  Jet_pT{};
  FloatArrayReader*  Jet_eta{};
  FloatArrayReader*  Jet_phi{};
  DoubleArrayReader* Jet_genpt{};
  UCharArrayReader*  Jet_hadronFlavour;
  IntArrayReader*    nBHadron{};
  FloatArrayReader*  BHadron_pT{};
  FloatArrayReader*  BHadron_eta{};
  FloatArrayReader*  BHadron_phi{};
  DoubleArrayReader* BHadron_mass{};
  IntArrayReader*    BHadron_pdgID{};
  LongArrayReader*   BHadron_hasBdaughter{};

  std::vector<double> bFragmentationWeightsReader{};
  void setValues();
  double GetBFragWeight(TH2* hist, double valx, double valy);
  double GetBRWeight(TGraph* graph, int valx);

  TString bfragWeightFile_{};
  TString histoName_{};
  TString bdecayWeightFile_{};

  TFile* bfragRootFile{};
  TH2F*  bFragmentationWeightsHisto{};
  TH2F*  bFragmentationWeightsUpHisto{};
  TH2F*  bFragmentationWeightsDownHisto{};

  TFile*  bdecayRootFile{};
  TGraph* bdecayWeightsUpGraph{};
  TGraph* bdecayWeightsDownGraph{};

};

void BFragmentationWeightsReader::beginEvent(long long _iEntry) {
  setValues();
}

BFragmentationWeightsReader::BFragmentationWeightsReader(char const* bfragWeightFile, char const* histoName, char const* bdecayWeightFile) :
  TTreeFunction(),
  bfragWeightFile_{bfragWeightFile},
  histoName_{histoName},
  bdecayWeightFile_{bdecayWeightFile}
{
  bfragRootFile = new TFile(bfragWeightFile_);
  bFragmentationWeightsHisto     = (TH2F*)bfragRootFile->Get(histoName_);
  bFragmentationWeightsUpHisto   = (TH2F*)bfragRootFile->Get(histoName_+"up");
  bFragmentationWeightsDownHisto = (TH2F*)bfragRootFile->Get(histoName_+"down");
  bdecayRootFile = new TFile(bdecayWeightFile_);
  bdecayWeightsUpGraph   = (TGraph*)bdecayRootFile->Get("semilepbrup");
  bdecayWeightsDownGraph = (TGraph*)bdecayRootFile->Get("semilepbrdown");
}

double
BFragmentationWeightsReader::evaluate(unsigned iJ) {
  return bFragmentationWeightsReader[iJ];
}

void BFragmentationWeightsReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nPFMuon,              "nPFMuon");
  _library.bindBranch(PFMuon_pt,            "PFMuon_pt");
  _library.bindBranch(PFMuon_eta,           "PFMuon_eta");
  _library.bindBranch(PFMuon_GoodQuality,   "PFMuon_GoodQuality");
  _library.bindBranch(PFMuon_IdxJet,        "PFMuon_IdxJet");
  _library.bindBranch(nJet,                 "nJet");
  _library.bindBranch(Jet_pT,               "Jet_pT");
  _library.bindBranch(Jet_eta,              "Jet_eta");
  _library.bindBranch(Jet_phi,              "Jet_phi");
  _library.bindBranch(Jet_genpt,            "Jet_genpt");
  _library.bindBranch(Jet_hadronFlavour,    "Jet_hadronFlavour");
  _library.bindBranch(nBHadron,             "nBHadron");
  _library.bindBranch(BHadron_pT,           "BHadron_pT");
  _library.bindBranch(BHadron_eta,          "BHadron_eta");
  _library.bindBranch(BHadron_phi,          "BHadron_phi");
  _library.bindBranch(BHadron_mass,         "BHadron_mass");
  _library.bindBranch(BHadron_pdgID,        "BHadron_pdgID");
  _library.bindBranch(BHadron_hasBdaughter, "BHadron_hasBdaughter");
}

void BFragmentationWeightsReader::setValues() {

  bFragmentationWeightsReader.clear();

  int muJetIsB = 0;
  double xB = -1., genJetPt = -1.;
  int bHadronId = -1;

  for (int imu = 0; imu<nPFMuon->At(0); imu++) {

    double    muPt{PFMuon_pt->At(imu)};
    double    muEta{PFMuon_eta->At(imu)}; 
    long long muQuality{PFMuon_GoodQuality->At(imu)};
    long long muJet{PFMuon_IdxJet->At(imu)};

    if (muQuality>=2 && muPt>5. && muEta>-2.4 && muEta<2.4 && muJet>=0) {

      double jetPt{Jet_pT->At(muJet)};
      double jetEta{Jet_eta->At(muJet)};
      int jetFlavour{Jet_hadronFlavour->At(muJet)};
      if (jetPt>=20. && jetEta>-2.5 && jetEta<2.5 && jetFlavour==5) {

        double maxBHadronMass = -1.;
        double jetPhi{Jet_phi->At(muJet)};
        muJetIsB = 1;

        for (int ibh = 0; ibh<nBHadron->At(0); ibh++) {

          float bHadronEta{BHadron_eta->At(ibh)};
          float bHadronPhi{BHadron_phi->At(ibh)};
         
          double DeltaPhi = acos(cos(bHadronPhi-jetPhi));
          double DeltaEta = bHadronEta-jetEta;
          if (sqrt(DeltaPhi*DeltaPhi+DeltaEta*DeltaEta)<0.5) {

            double    bHadronMass{BHadron_mass->At(ibh)};
            float     bHadronPt{BHadron_pT->At(ibh)};     
            long long bHadronHasDaughter{BHadron_hasBdaughter->At(ibh)};            

            if (bHadronMass>maxBHadronMass) {
              genJetPt       = Jet_genpt->At(muJet);
              xB             = bHadronPt/fabs(genJetPt);
              maxBHadronMass = bHadronMass;
            }

            if (bHadronHasDaughter==0) bHadronId = abs(BHadron_pdgID->At(ibh));

          }

        }
  
      }

    }

  }

  

  for (int bfsyst = 0; bfsyst<=4; bfsyst++) {

    double bFragmentationWeight = -1.;

    if (muJetIsB==0) {
      bFragmentationWeight = 1.; // Jusr for safety. It will not be used!
    } else if (muJetIsB==1) {

      bFragmentationWeight = -1.;
      if (bfsyst==0) bFragmentationWeight = this->GetBFragWeight(bFragmentationWeightsDownHisto, xB, genJetPt);
      if (bfsyst==1) bFragmentationWeight = this->GetBFragWeight(bFragmentationWeightsHisto,     xB, genJetPt);
      if (bfsyst==2) bFragmentationWeight = this->GetBFragWeight(bFragmentationWeightsUpHisto,   xB, genJetPt);
      if (bfsyst==3) bFragmentationWeight = this->GetBRWeight(bdecayWeightsDownGraph,             bHadronId);
      if (bfsyst==4) bFragmentationWeight = this->GetBRWeight(bdecayWeightsUpGraph,               bHadronId);

      if (bFragmentationWeight<=0.) { 
        if (bfsyst>=2) { std::cout << "BFragmentationWeightsReader Error for " << bfragWeightFile_ << " " << xB << " " << genJetPt << std::endl; }
        else { std::cout << "BFragmentationWeightsReader Error for " << bdecayWeightFile_ << " " << bHadronId << std::endl; }
      }

    }

    bFragmentationWeightsReader.push_back(bFragmentationWeight);

  }

}

double BFragmentationWeightsReader::GetBFragWeight(TH2* hist, double xB, double genJetPt) {

  if (xB<1 && genJetPt>=30) {
    size_t xb_bin = hist->GetXaxis()->FindBin(xB);
    size_t pt_bin = hist->GetYaxis()->FindBin(genJetPt);
    return hist->GetBinContent(xb_bin, pt_bin);
  } else {
    return 1.;
  }

}
 
double BFragmentationWeightsReader::GetBRWeight(TGraph* graph, int bHadronId) {

  if (bHadronId == 511 ||  bHadronId == 521 ||  bHadronId == 531 ||  bHadronId == 5122) {
    //int bid(jinfo.hasSemiLepDecay ? absBid : -absBid);
    return graph->Eval(bHadronId);
  } else {
    return 1.;
  }

}

