
void CompareContour(TString Signal0, TString Signal1, TString Level, TString Name0 = "", TString Name1 = "") {

  if (Level=="Blind") {
    Signal0 += "_Blind";
    Signal1 += "_Blind";
    Level = "Exp";
  }

  TFile *_file0 = TFile::Open("./RootFiles/" + Signal0 + ".root");
  TFile *_file1 = TFile::Open("./RootFiles/" + Signal1 + ".root");

  TGraph *C0C = (TGraph*)_file0->Get("gr_" + Level);
  TGraph *C0P = (TGraph*)_file0->Get("gr_" + Level + "P");
  TGraph *C0M = (TGraph*)_file0->Get("gr_" + Level + "M");

  TGraph *C1C = (TGraph*)_file1->Get("gr_" + Level);
  TGraph *C1P = (TGraph*)_file1->Get("gr_" + Level + "P");
  TGraph *C1M = (TGraph*)_file1->Get("gr_" + Level + "M");

  C0P->SetLineStyle(2);
  C0M->SetLineStyle(2);

  C1P->SetLineStyle(2);
  C1M->SetLineStyle(2);

  C1C->SetLineColor(2);
  C1P->SetLineColor(2);
  C1M->SetLineColor(2);

  C0C->SetLineColor(1);
  C0P->SetLineColor(1);
  C0M->SetLineColor(1);

  C0P->GetXaxis()->SetTitle("M_{#tilde t} [GeV]");
  C0P->GetYaxis()->SetTitle("M_{#tilde #Chi^{0}_{1}} [GeV]");
  if (Signal1.Contains("TChi")) C0P->GetXaxis()->SetTitle("M_{#tilde #Chi^{#pm}_{1}} [GeV]");

  C0P->SetMinimum(  0.);
  C0P->SetMaximum(500.);

  C0P->Draw("");
  C0C->Draw("same");
  C0M->Draw("same");
  C1P->Draw("same");
  C1C->Draw("same");
  C1M->Draw("same");

  TLegend  *leg = new TLegend(0.13, 0.72, 0.29, 0.88);
  leg->SetFillColor(kWhite); leg->SetBorderSize(0.);
  leg->SetTextColor(1); leg->SetTextSize(0.035);
  leg->SetTextFont(62); 

  if (Name0=="") Name0 = Signal0;
  if (Name1=="") Name1 = Signal1;
  leg->AddEntry(C0C, Name0, "l");
  leg->AddEntry(C1C, Name1, "l");

  leg->Draw();
    
}
