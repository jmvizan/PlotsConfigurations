void CheckNoJetRateFit(TString Process) {

  TFile *_file0 = TFile::Open("./DatacardsTest/MassPointChiSlep_Xm525_Xm125/mlfit_prefit.root");
  TFile *_file1 = TFile::Open("./DatacardsTest/MassPointChiSlep_Xm525_Xm125/mlfit_nosyst.root");

  for (int ich = 0; ich<2; ich++) {

    TString ch = ich==0 ? "em" : "sf";

    float PJ = ((TH1D*)_file0->Get("shapes_prefit/" + ch + "_NoJet/" + Process))->Integral();
    float PT = ((TH1D*)_file0->Get("shapes_prefit/" + ch + "_NoTag/" + Process))->Integral();
    
    float FJ = ((TH1D*)_file1->Get("shapes_fit_b/"  + ch + "_NoJet/" + Process))->Integral();
    float FT = ((TH1D*)_file1->Get("shapes_fit_b/"  + ch + "_NoTag/" + Process))->Integral();

    cout << "Yields in the " + ch + " channel: " << endl 
	 << "              before fit: " << PJ << " " << PT << " " << PJ+PT << endl
	 << "              after  fit: " << FJ << " " << FT << " " << FJ+FT << " " << (FJ+FT)/(PJ+PT) << endl
	 << "               rateParam: " << FJ/PJ << " " << FT/PT << " " << 1.+PJ/PT*(1.-FJ/PJ) << endl
	 << endl;
      
  }

}
