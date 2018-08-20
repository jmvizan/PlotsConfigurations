
void CheckContour(TString Signal) {

  TFile *_file0 = TFile::Open("./RootFiles/" + Signal + ".root");

  TGraph *ExpC = (TGraph*)_file0->Get("gr_Exp");
  TGraph *ExpP = (TGraph*)_file0->Get("gr_ExpP");
  TGraph *ExpM = (TGraph*)_file0->Get("gr_ExpM");

  TGraph *ObsC = (TGraph*)_file0->Get("gr_Obs");
  TGraph *ObsP = (TGraph*)_file0->Get("gr_ObsP");
  TGraph *ObsM = (TGraph*)_file0->Get("gr_ObsM");

  ExpP->SetLineStyle(2);
  ExpM->SetLineStyle(2);

  ObsP->SetLineStyle(2);
  ObsM->SetLineStyle(2);

  ExpC->SetLineColor(1);
  ExpP->SetLineColor(1);
  ExpM->SetLineColor(1);

  ObsC->SetLineColor(2);
  ObsP->SetLineColor(2);
  ObsM->SetLineColor(2);

  ExpP->Draw("");
  ExpC->Draw("same");
  ExpM->Draw("same");
  ObsP->Draw("same");
  ObsC->Draw("same");
  ObsM->Draw("same");

}
