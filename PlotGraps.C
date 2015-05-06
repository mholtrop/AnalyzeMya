{
  TFile f("epics.root");
  TGraph *g1=(TGraph *)f.Get("IPM2H01.VAL");
  TGraph *g2=(TGraph *)f.Get("IPM2H00.YPOS");
  TGraph *g3=(TGraph *)f.Get("IPM2H01.YPOS");
  TGraph *g4=(TGraph *)f.Get("IPM2H02.YPOS");
  TCanvas *cc= new TCanvas("cc","BPMs",1400,500);
  cc->cd();
  TLatex *t1 = new TLatex(0.1,0.93,"2H01.Cur");
  t1->SetTextColor(7);
  t1->Draw();

  TLatex *t2 = new TLatex(0.2,0.93,"2H00.YPOS");
  t2->SetTextColor(kRed);
  t2->Draw();

  TLatex *t3 = new TLatex(0.3,0.93,"2H01.YPOS");
  t3->SetTextColor(kGreen);
  t3->Draw();

  TLatex *t4 = new TLatex(0.4,0.93,"2H02.YPOS");
  t4->SetTextColor(kBlue);
  t4->Draw();

  TPad *p1=new TPad("p1","",0,0,1,1);
  p1->SetFillColor(0);
  p1->SetFillStyle(4000);
  p1->Draw();
  p1->cd();
  g1->SetTitle("");
  g1->SetFillColorAlpha(7,0.3);
  g1->SetLineColorAlpha(0,0.5);
  g1->GetYaxis()->SetLabelColor(7);
  g1->GetYaxis()->SetLabelOffset(0.08);
  g1->GetYaxis()->SetAxisColor(7);
  g1->GetYaxis()->SetTickSize(-0.01);
  g1->Draw("ALF");

  TPad *p2=new TPad("p2","",0,0,1,1);
  p2->SetFillColor(0);
  p2->SetFillStyle(4000);
  p2->SetFrameFillStyle(4000);
  p2->Draw();
  p2->cd();
  g2->SetTitle("");
  g2->SetLineColor(kRed);
  g2->SetLineWidth(2);
  g2->GetYaxis()->SetLabelColor(kRed);
  g2->GetYaxis()->SetLabelOffset(0.055);
  g2->GetYaxis()->SetAxisColor(kRed);
  g2->GetYaxis()->SetTickSize(0.02);
  g2->SetMinimum(-0.5);
  g2->SetMaximum(1.5);
  g2->Draw("AL");

  TPad *p3=new TPad("p3","",0,0,1,1);
  p3->SetFillColor(0);
  p3->SetFillStyle(4000);
  p3->SetFrameFillStyle(4000);
  p3->Draw();
  p3->cd();
  g3->SetTitle("");
  g3->SetLineColor(kGreen);
  g3->SetLineWidth(2);
  g3->GetYaxis()->SetLabelColor(kGreen);
  g3->GetYaxis()->SetLabelOffset(0.03);
  g3->GetYaxis()->SetAxisColor(kGreen);
  g3->GetYaxis()->SetTickSize(0.015);  
  g3->SetMinimum(-3.);
  g3->SetMaximum(-1.0);
  g3->Draw("AL");

  TPad *p4=new TPad("p4","",0,0,1,1);
  p4->SetFillColor(0);
  p4->SetFillStyle(4000);
  p4->SetFrameFillStyle(4000);
  p4->Draw();
  p4->cd();
  g4->SetTitle("");
  g4->SetLineColor(kBlue);
  g4->SetLineWidth(2);
  g4->GetYaxis()->SetLabelColor(kBlue);
  g4->GetYaxis()->SetLabelOffset(0.0);
  g4->GetYaxis()->SetAxisColor(kBlue);
  g4->GetYaxis()->SetTickSize(0.01);  
  g4->SetMinimum(-1.5);
  g4->SetMaximum(0.5);
  g4->Draw("AL");

}
