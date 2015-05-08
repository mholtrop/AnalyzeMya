{
  //  TFile f("epics.root");
  int kBrown=45;
  TGraph *g_fc=(TGraph *)f.Get("FCUP");
  TGraph *g1=new TGraph(*g_fc);    // Make a copy, since we'll scale it.
  TGraph *g2=(TGraph *)f.Get("Delta_IPM2H00_YPOS");
  TGraph *g3=(TGraph *)f.Get("Delta_IPM2H01_YPOS");
  TGraph *g4=(TGraph *)f.Get("Delta_IPM2H02_YPOS");
  TGraph *g_t=(TGraph *)f.Get("HPS_T");
  TGraph *g5 = new TGraph(*g_t);
  TGraph *g_sc=(TGraph *)f.Get("HPS_SC");
  TGraph *g6 = new TGraph(*g_sc);

  TCanvas *cc= new TCanvas("cc","BPMs",1400,500);
  cc->cd();
  TLatex *t1 = new TLatex(0.1,0.93,"FCUP*10^{-2}");
  t1->SetTextColor(7);
  t1->Draw();

  TLatex *t2 = new TLatex(0.2,0.93,"#Delta_2H00.YPOS");
  t2->SetTextColor(kRed);
  t2->Draw();

  TLatex *t4 = new TLatex(0.35,0.93,"#Delta_2H02.YPOS");
  t4->SetTextColor(kBlue);
  t4->Draw();

  TLatex *t5 = new TLatex(0.5,0.93,"HPS_T*0.7*10^{-5}");
  t5->SetTextColor(kBlack);
  t5->Draw();

  TLatex *t6 = new TLatex(0.65,0.93,"HPS_SC*0.2*10^{-5}");
  t6->SetTextColor(kBrown);
  t6->Draw();


  TPad *p1=new TPad("p1","",0,0,1,1);
  p1->SetFillColor(0);
  p1->SetFillStyle(4000);
  p1->Draw();
  p1->cd();

  g2->SetTitle("");
  g2->SetLineColor(kRed);
  g2->SetLineWidth(2);
  //  g2->GetYaxis()->SetLabelColor(kRed);
  //  g2->GetYaxis()->SetLabelOffset(0.055);
  //g2->GetYaxis()->SetAxisColor(kRed);
  g2->GetYaxis()->SetTickSize(0.02);
  g2->SetMinimum(-1.);
  g2->SetMaximum(1.);
  g2->Draw("AL");

  for (int i=0;i<g1->GetN();i++) g1->GetY()[i] = g_fc->GetY()[i]*1E-2;  //  Scale
  g1->SetTitle("");
  g1->SetLineColor(7);
  g1->SetLineWidth(2);
  g1->Draw("L");

  //  for (int i=0;i<g3->GetN();i++) g3->GetY()[i] = g3->GetY()[i]-1.5;  //  Move Down by 1.5
  g3->SetTitle("");
  g3->SetLineColor(kGreen);
  g3->SetLineWidth(2);
  //  g3->Draw("L");

  g4->SetTitle("");
  g4->SetLineColor(kBlue);
  g4->SetLineWidth(2);
  g4->Draw("L");


  for (int i=0;i<g5->GetN();i++) g5->GetY()[i] = g_t->GetY()[i]*0.7E-5;  //  Move Down by 1.5
  g5->SetTitle("");
  g5->SetLineColor(kBlack);
  g5->SetLineWidth(2);
  g5->Draw("L");

  for (int i=0;i<g6->GetN();i++) g6->GetY()[i] = g_sc->GetY()[i]*0.2E-5;  //  Move Down by 1.5
  g6->SetTitle("");
  g6->SetLineColor(kBrown);
  g6->SetLineWidth(2);
  g6->Draw("L");


  //  TMultiGraph *mg = new TMultiGraph();
  //mg->Add(g1,"L");
  //mg->Add(g2,"L");
  //mg->Add(g3,"L");
  //mg->Add(g4,"L");
  //mg->Draw()

}
