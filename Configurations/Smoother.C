int npv, npf;
double xv[500], yv[500];
double xf[500], yf[500];

void GetHardFit(TString Signal, TString GrName) {

  TGraph *ObsV = new TGraph(npv, xv, yv);
  
  float xMin = 9999., xMax = -999.;
  for  (int iv = 0; iv<npv; iv++) {
    if (xv[iv]<xMin) xMin = xv[iv];
    if (xv[iv]>xMax) xMax = xv[iv];
  }

  TF1 *fun = new TF1("fun", "pol1", xMin, xMax);
  ObsV->Fit("fun", "", "", xMin, xMax);

  TCanvas *CV = new TCanvas("CV", "", 600, 400);
  CV->cd();

  ObsV->Draw();

  float offY = (yv[0]+yv[npv-1])/2.;
  float pend = fun->GetParameter(1);
  float cosA = cos(atan(pend));
  float sinA = sin(atan(pend));
  for (int iv = 0; iv<npv; iv++) {
    float xr =  cosA*xv[iv] + sinA*(yv[iv]-offY);
    float yr = -sinA*xv[iv] + cosA*(yv[iv]-offY);
    xv[iv] = xr;
    yv[iv] = yr;
  }

  TGraph *ObsR = new TGraph(npv, xv, yv);
  TF1 *funf = new TF1("funf", "pol5", xv[0], xv[npv-1]);
  ObsR->Fit("funf", "", "", xv[0], xv[npv-1]);
  ObsR->Draw();

  for (int iv = 0; iv<npv; iv++) {
    float xr =  cosA*xv[iv] - sinA*(funf->Eval(xv[iv]));
    float yr =  sinA*xv[iv] + cosA*(funf->Eval(xv[iv]));
    xf[npf] = xr;
    yf[npf] = yr + offY;
    npf++;
  }
  
}

void GetHardFitT2tt(TString Signal, TString GrName, TString pol) {

  float offY = (yv[0]+yv[npv-1])/2.;
  float pend = (Signal.Contains("T2tt")) ? -1. : -0.5;
  float cosA = cos(atan(pend));
  float sinA = sin(atan(pend));
  for (int iv = 0; iv<npv; iv++) {
    float xr =  cosA*xv[iv] + sinA*(yv[iv]-offY);
    float yr = -sinA*xv[iv] + cosA*(yv[iv]-offY);
    xv[iv] = xr;
    yv[iv] = yr;
  }

  TCanvas *CV = new TCanvas("CV", "", 600, 400);
  CV->cd();

  TGraph *ObsR = new TGraph(npv, xv, yv);
  TF1 *funf = new TF1("funf", pol, xv[0], xv[npv-1]);

  ObsR->Fit("funf", "", "", xv[0], xv[npv-1]);
  ObsR->Draw();

  double lastX = -1;
  for (int iv = 0; iv<npv; iv++) {
    float xr =  cosA*xv[iv] - sinA*(funf->Eval(xv[iv]));
    float yr =  sinA*xv[iv] + cosA*(funf->Eval(xv[iv]));
    if (lastX>=0. && xv[iv]<lastX) continue;
    lastX = xv[iv];
    xf[npf] = xr;
    yf[npf] = yr + offY;
    cout << "F " << npf << " " << xf[npf] << " " << yf[npf] << endl;
    npf++;
  }

}

TGraph *GetSmoothGraph(TString Signal, TString GrName, bool Verbose = false) {
  TFile *_file0 = TFile::Open("./RootFiles/" + Signal + ".root");

  double xx[500], yy[500];

  TGraph *ObsC = (TGraph*)_file0->Get(GrName);
  
  int np = ObsC->GetN();
  
  for (int ip = 0; ip<np; ip++) {

    double xxx, yyy;
    ObsC->GetPoint(ip, xxx, yyy);
    if (Signal.Contains("T2tt") && GrName.Contains("gr_Obs")) {
      xx[np-1-ip] = xxx;
      yy[np-1-ip] = yyy;
    } else {
      xx[ip] = xxx;
      yy[ip] = yyy;
    }

  }
   
  if (Verbose) 
    for (int ip = 0; ip<np; ip++)
      cout << ip << " " << xx[ip] << " " << yy[ip] << endl;
 
  int nMidPoints = 0; int MidPointI[1000], MidPointF[1000];

  if  (Signal.Contains("TChiSlep")) {
    MidPointI[0] = 0;
    MidPointF[0] = np-1;
    nMidPoints = 1;
  } else if  (Signal.Contains("T2bW")) {
    if (GrName=="gr_Exp") {
      /*MidPointI[0] = 0;
      MidPointF[0] = 59;
      MidPointI[1] = 69;
      MidPointF[1] = np-1;
      nMidPoints = 2;*/
      MidPointI[0] = 0;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } else if (GrName=="gr_ExpP") {
      /*MidPointI[0] = 0;
      MidPointF[0] = 71;
      MidPointI[1] = 73;
      MidPointF[1] = np-1;
      nMidPoints = 2;*/
      MidPointI[0] = 0;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } else if (GrName=="gr_ExpM") {
      /*MidPointI[0] = 5;
      MidPointF[0] = 51;
      MidPointI[1] = 52;
      MidPointF[1] = 58;
      nMidPoints = 2;*/
      MidPointI[0] = 5;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } else if (GrName=="gr_Obs") {
      /*MidPointI[0] = 7;
      MidPointF[0] = 67;
      MidPointI[1] = 68;
      MidPointF[1] = np-1;
      nMidPoints = 2;*/
      MidPointI[0] = 7;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } else if (GrName=="gr_ObsM") {
      /*MidPointI[0] = 7;
      MidPointF[0] = 72;
      MidPointI[1] = 73;
      MidPointF[1] = np-1;
      nMidPoints = 2;*/
      MidPointI[0] = 7;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } else if (GrName=="gr_ObsP") {
      /*MidPointI[0] = 7;
      MidPointF[0] = 63;
      MidPointI[1] = 68;
      MidPointF[1] = np-1;
      nMidPoints = 2;*/
      MidPointI[0] = 7;
      MidPointF[0] = np-1;
      nMidPoints = 1;
    } 
  } else if  (Signal.Contains("T2tt")) {
    if (GrName=="gr_ExpP") {
      MidPointI[0] = 0;
      MidPointF[0] = 100;
      MidPointI[1] = 101;
      MidPointF[1] = 112;/*
      MidPointI[2] = 116;
      MidPointF[2] = 136;
      MidPointI[3] = 138;
      MidPointF[3] = 183;
      MidPointI[4] = 184;
      MidPointF[4] = 211;
      MidPointI[5] = 212;
      MidPointF[5] = 285;
      nMidPoints = 6;*/
      MidPointI[2] = 116;//101;
      MidPointF[2] = 158;//285;
      MidPointI[3] = 158;//101;
      MidPointF[3] = 287;//285;
      nMidPoints = 4;
    } else if (GrName=="gr_Exp") {
      MidPointI[0] = 0;
      MidPointF[0] = 77;
      MidPointI[1] = 79;
      MidPointF[1] = 93;/*
      MidPointI[2] = 94;
      MidPointF[2] = 119;
      MidPointI[3] = 120;
      MidPointF[3] = 183;
      MidPointI[4] = 184;
      MidPointF[4] = 257;
      nMidPoints = 5;*/
      MidPointI[2] = 97;
      MidPointF[2] = 144;
      MidPointI[3] = 157;
      MidPointF[3] = 257;
      nMidPoints = 4;
    } else if (GrName=="gr_ExpM") {
      MidPointI[0] = 0;
      MidPointF[0] = 65;
      MidPointI[1] = 67;
      MidPointF[1] = 74;/*
      MidPointI[2] = 79;
      MidPointF[2] = 125;
      MidPointI[3] = 126;
      MidPointF[3] = 205;
      MidPointI[4] = 206;
      MidPointF[4] = 271;
      nMidPoints = 5;*/
      MidPointI[2] = 80;
      MidPointF[2] = 114;
      MidPointI[3] = 115;
      MidPointF[3] = 135;
      MidPointI[4] = 136;
      MidPointF[4] = 272;
      nMidPoints = 5;
    } else if (GrName=="gr_ObsP") {
      MidPointI[0] = 0;
      MidPointF[0] = 92;
      MidPointI[1] = 94;
      MidPointF[1] = 109;/*
      MidPointI[2] = 111;
      MidPointF[2] = 132;
      MidPointI[3] = 133;
      MidPointF[3] = 183;
      MidPointI[4] = 184;
      MidPointF[4] = 268;
      MidPointI[5] = 349;
      MidPointF[5] = 357;
      MidPointI[6] = 358;
      MidPointF[6] = 372;
      nMidPoints = 7;*/
      MidPointI[2] = 118;
      MidPointF[2] = 157;
      MidPointI[3] = 168;
      MidPointF[3] = 268;
      MidPointI[4] = 346;
      MidPointF[4] = 357;
      MidPointI[5] = 358;
      MidPointF[5] = 372;
      nMidPoints = 6;
    } else if (GrName=="gr_Obs") {
      MidPointI[0] = 0;
      MidPointF[0] = 82;
      MidPointI[1] = 84;
      MidPointF[1] = 100;
      MidPointI[2] = 102;
      MidPointF[2] = 112;
      MidPointI[3] = 120;
      MidPointF[3] = 130;
      MidPointI[4] = 157;
      MidPointF[4] = 269;
      MidPointI[5] = 348;
      MidPointF[5] = 368;
      MidPointI[6] = 369;
      MidPointF[6] = 396;
      nMidPoints = 7;
    } else if (GrName=="gr_ObsM") {
      MidPointI[0] = 0;
      MidPointF[0] = 78;
      MidPointI[1] = 81;
      MidPointF[1] = 91;
      MidPointI[2] = 124;
      MidPointF[2] = 126;
      MidPointI[3] = 127;
      MidPointF[3] = 160;
      MidPointI[4] = 160;
      MidPointF[4] = 275;
      MidPointI[5] = 348;
      MidPointF[5] = 385;
      MidPointI[6] = 386;
      MidPointF[6] = 426;
      nMidPoints = 7;
    }
  }
  
  npf = 0;

  if (MidPointI[0]!=0) {
    for (int jf = 0; jf<MidPointI[0]; jf++) {
      xf[npf] = xx[jf];
      yf[npf] = yy[jf];
      npf++;
    }
  }

  for (int md = 0; md<nMidPoints; md++) {

    npv = 0;
    for (int ip = MidPointI[md]; ip<=MidPointF[md]; ip++) {
      
      if (Signal.Contains("T2bWa")) {
	if (GrName=="gr_Exp") {
	  if (ip>=51 && ip<=55) continue;
	  if (ip>=60 && ip<=65) continue;
	}
	if (GrName=="gr_ExpP") {
	  if (ip>=61 && ip<=66) continue;
	}
      } else if (Signal.Contains("T2tt")) {
	if (GrName=="gr_ObsP") {
	  if (ip>=253 && ip<=267) continue;
	}
      }
      xv[npv] = xx[ip];//xv[ip-1] + dx;
      yv[npv] = yy[ip];// - yy[ip-1];  
      if (Verbose)
	cout << "V " << npv << " " << xv[npv] << " " << yv[npv] << endl;
      npv++;

    }

    TString fun = "pol9";
    if (Signal.Contains("T2bW")) {
      //fun = "pol8";
      //if (GrName.Contains("gr_") && md==1) fun = "pol2";
      fun = "retT2tt";
    } else if (Signal.Contains("T2tt")) {
      fun = "pol2";
      if (md==2 || md==3 || 
	  (md==4 && (GrName=="gr_ExpM" || GrName=="gr_Obs" || GrName=="gr_ObsM"))) fun = "retT2tt";
    }

    TF1 *FF;

    if (!fun.Contains("ret")) {

      TGraph *ObsV = new TGraph(npv, xv, yv);

      TCanvas *CV = new TCanvas("CV", "", 600, 400);
      CV->cd();

      FF = new TF1("FF", fun, xv[0], xv[npv-1]);   
      ObsV->Fit("FF", "", "", xv[0], xv[npv-1]); 
      ObsV->Draw();  
      
      for (int ip = 0; ip<npv; ip++) {
	
	if (Signal.Contains("T2bW")) {
	  if (GrName=="gr_ExpP" && md==0) 
	    if (ip>63) continue;
	  //if (GrName=="gr_ExpP" && md==1) 
	  //if (ip>=71) continue;
	  if (GrName.Contains("gr_") && md==0) 
	    if (ip>0 && xv[ip]<xf[npf-1]) continue;
	  if (GrName.Contains("gr_") && md==1) 
	    if (ip>0 && xv[ip]>xf[npf-1]) continue;
	} else if (Signal.Contains("T2tt")) {
	  if (md==4)
	    if (ip>0 && xv[ip]<xf[npf-1]) continue;
	} else if (Signal.Contains("TChiSlep")) {
	  if (ip>0 && xv[ip]<xf[npf-1]) continue;
	}
	
	xf[npf] = xv[ip];
	yf[npf] = FF->Eval(xv[ip]);
	if (Verbose) cout << "F " << ip << " " << npf << " " << xf[npf] << " " << yf[npf] << endl;
	npf++;
      
      }

      if (Signal.Contains("TChiSlep")) {
	while (yf[npf-1]>1.) {
	  xf[npf] = xf[npf-1] + 10.;
	  yf[npf] = FF->Eval(xf[npf]);
	  npf++;
	}
      }

    } else if (fun=="ret") {

      GetHardFit(Signal, GrName);

    } else if (fun=="retT2tt") {

      TString pol = "pol2";
      if (Signal.Contains("T2tt")) {
	if ((GrName=="gr_Exp" || GrName=="gr_ExpP") && md==3) pol = "pol9";
	if (GrName=="gr_ExpM" && md==4) pol = "pol6";  
	if (GrName=="gr_ObsP" && md==3) pol = "pol6";  
	if (GrName=="gr_Obs" && md==4) pol = "pol6";   
	if (GrName=="gr_ObsM" && md==4) pol = "pol6";  
      } else if (Signal.Contains("T2bW")) {
	//if ((GrName=="gr_Exp" || GrName=="gr_ExpP" || GrName=="gr_ExpM") && md==0) pol = "pol6";
	pol = "pol9";
      }   
      GetHardFitT2tt(Signal, GrName, pol);
      
    } 

    if  (Signal.Contains("T2tt")) {
      if (GrName.Contains("gr_")) {
	if (md==1) {
	  int fpa = MidPointI[md+1];
	  if (GrName.Contains("gr_ObsM")) fpa = 97;
	  for (int jf = MidPointF[md]; jf<fpa; jf++) {
	    xf[npf] = xx[jf];
	    yf[npf] = yy[jf];
	    npf++;
	  } 
	}
	if (GrName.Contains("gr_ObsP") && md==3) {
	  xf[213] = 698.;
	  yf[213] =  60.;
	  xf[214] = 700.;
	  yf[214] =  40.;
	  xf[215] = 710.;
	  yf[215] =  -1.;
	  npf = 216;
	}
	if (GrName.Contains("gr_ExpP") && md==3) {
	  cout << "S"<<endl;
	  xf[243] = 760.;
	  yf[243] = -1.;
	  npf = 244;
	}
	if (GrName.Contains("gr_Obs") && md==nMidPoints-3) {
	  xf[npf] = xx[MidPointF[nMidPoints-3]];
	  yf[npf] = -10.;
	  npf++;
	  xf[npf] = xx[MidPointI[nMidPoints-2]];
	  yf[npf] = -10.;
	  npf++;
	} 
      }
    }

    /*
    if  (Signal.Contains("TChiSlep")) {
      if (md==nMidPoints-1 && yf[npf-1]>10.) {
	xf[npf] = xf[npf-1];
	yf[npf] = -10.;
	npf++;
      }  
    }
    */

    if (Signal.Contains("T2bW")) {
      if (GrName=="gr_Obs" || GrName=="gr_ExpM") {
	xf[npf] = xx[np-1];
	yf[npf] = yy[np-1];
	npf++;
      }
    }

    // Final part
    if (md==nMidPoints-1+100) {
      bool more = yf[npf-1]>5. ? true : false;
      while (yf[npf-1]>5. && more) {
	float dx = 10.;
	if (Signal.Contains("T2bW")) dx = -10.;
	double xxx = xf[npf-1] + dx;
	if (FF->Eval(xxx)<yf[npf-1]) {
	  xf[npf] = xxx;
	  yf[npf] = FF->Eval(xxx); 
	  npf++;
	} else more = false;
      }
      if (yf[npf-1]>5.) {
	xf[npf] = xx[np-1];
	yf[npf] = yy[np-1];
	npf++;
      }
    }

  }

  TGraph *ObsF = new TGraph(npf, xf, yf);
    
  TCanvas *CF = new TCanvas("CF", "", 600, 400);
  CF->cd();
  
  ObsC->Draw();  
  ObsF->SetLineColor(2);
  ObsF->Draw("same"); 

  _file0->Close();

  //if (GrName.Contains("Exp")) ObsF->SetLineColor(1);

  return ObsF;

}

TH2F *Get2dHisto(TString Signal, TString HistoName) {

  TFile *_file0 = TFile::Open("./RootFiles/" + Signal + ".root");

  TH2F *H2D = (TH2F*) _file0->Get(HistoName);

  return H2D;


}

void Smoother(TString Signal) {

  TFile *_file1 = new TFile("./RootFiles/" + Signal + "_Smooth.root", "recreate");

  int const ngr = 6;
  TString GrName[ngr] = {"gr_Exp", "gr_ExpM", "gr_ExpP", "gr_ObsP", "gr_Obs", "gr_ObsM"};
  
  for (int igr = 0; igr<ngr; igr++) {

    TGraph *gr = GetSmoothGraph(Signal, GrName[igr]);
    
    _file1->cd();

    gr->SetName(GrName[igr]);
    gr->Write();

  }
  
  TH2F *hXsec_exp = Get2dHisto(Signal, "hXsec_exp");
  TH2F *hXsec_obs = Get2dHisto(Signal, "hXsec_obs");

  _file1->cd();
  
  hXsec_exp->Write();
  hXsec_obs->Write();

  _file1->Close();

}


void CompareGraph(TString Signal1, TString Signal2, TString GrName) {

  TFile *_file1 = TFile::Open("./RootFiles/" + Signal1 + ".root");
  TFile *_file2 = TFile::Open("./RootFiles/" + Signal2 + ".root");

  TGraph *Obs1 = (TGraph*)_file1->Get(GrName);
  TGraph *Obs2 = (TGraph*)_file2->Get(GrName);
  
  int np1 = Obs1->GetN();
  int np2 = Obs2->GetN();
  
  int np = np1>np2 ? np1 : np2;

  for (int ip = 0; ip<np; ip++) {

    int ip1 = (np1-1)-ip;
    int ip2 = (np2-1)-ip;

    double xx1 = -999., yy1 = -999., xx2 = -999., yy2 = -999.;
    if (ip1<np1) Obs1->GetPoint(ip1, xx1, yy1);
    if (ip2<np2) Obs2->GetPoint(ip2, xx2, yy2);

    cout << ip << " " << xx1 << " " << xx2 << "   " << yy1 << " " << yy2 << endl;
    
  }
  
}
