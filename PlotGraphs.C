void PlotGraphs(const char * file){
  // Open file.

  TString fnam(file);
  TFile *f=new TFile(fnam+".root");

  int kBrown=45;
  TGraph *g_fc=(TGraph *)f->Get("FCUP");
  TGraph *g1=new TGraph(*g_fc);    // Make a copy, since we'll scale it.
  TGraph *g2=(TGraph *)f->Get("Delta_IPM2H00_YPOS");
  TGraph *g3=(TGraph *)f->Get("Delta_IPM2H01_YPOS");
  TGraph *g4=(TGraph *)f->Get("Delta_IPM2H02_YPOS");
  TGraph *g_t=(TGraph *)f->Get("HPS_T");
  TGraph *g5 = new TGraph(*g_t);
  TGraph *g_sc=(TGraph *)f->Get("HPS_SC");
  TGraph *g6 = new TGraph(*g_sc);
  TGraph *g7=(TGraph *)f->Get("Delta_IPM2C21A_YPOS");
  TGraph *g8=(TGraph *)f->Get("Delta_IPM2C24A_YPOS");

  TGraph *g2_x=(TGraph *)f->Get("Delta_IPM2H00_XPOS");
  TGraph *g3_x=(TGraph *)f->Get("Delta_IPM2H01_XPOS");
  TGraph *g4_x=(TGraph *)f->Get("Delta_IPM2H02_XPOS");
  TGraph *g7_x=(TGraph *)f->Get("Delta_IPM2C21A_XPOS");
  TGraph *g8_x=(TGraph *)f->Get("Delta_IPM2C24A_XPOS");

  f->Close();
  delete f;

  double fcup_scale = 2E-1;
  char fcup_scale_txt[] = "FCUP*2*10^{-1}";

  double hps_t_scale = 1.e-5;
  char hps_t_scale_txt[] = "HPS_T*1.*10^{-5}";

  double hps_sc_scale = 0.16e-5;
  char hps_sc_scale_txt[] = "HPS_SC*0.16*10^{-5}";

  TCanvas *cc_y= new TCanvas("cc_y",fnam+"_Y",1400,500);
  cc_y->cd();

  TLatex *t1 = new TLatex(0.05,0.93,fnam+"_Y");
  t1->SetTextColor(kBlack);
  t1->Draw();

  TLatex *t2 = new TLatex(0.3,0.93,"#Delta_2H00.YPOS");
  t2->SetTextColor(kRed);
  t2->Draw();

  TLatex *t4 = new TLatex(0.43,0.93,"#Delta_2H02.YPOS");
  t4->SetTextColor(kBlue);
  t4->Draw();

  TLatex *t5 = new TLatex(0.55,0.93,hps_t_scale_txt);
  t5->SetTextColor(kBlack);
  t5->Draw();

  TLatex *t6 = new TLatex(0.68,0.93,hps_sc_scale_txt);
  t6->SetTextColor(kBrown);
  t6->Draw();

  TLatex *t7 = new TLatex(0.83,0.93,fcup_scale_txt);
  t7->SetTextColor(7);
  t7->Draw();


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

  for (int i=0;i<g1->GetN();i++) g1->GetY()[i] = g_fc->GetY()[i]*fcup_scale;  //  Scale
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


  for (int i=0;i<g5->GetN();i++) g5->GetY()[i] = g_t->GetY()[i]*hps_t_scale;  //  Move Down by 1.5
  g5->SetTitle("");
  g5->SetLineColor(kBlack);
  g5->SetLineWidth(2);
  g5->Draw("L");

  for (int i=0;i<g6->GetN();i++) g6->GetY()[i] = g_sc->GetY()[i]*hps_sc_scale;  //  Move Down by 1.5
  g6->SetTitle("");
  g6->SetLineColor(kBrown);
  g6->SetLineWidth(2);
  g6->Draw("L");

  g7->SetLineColor(kGreen);
  g8->SetLineColor(kYellow);
    
  //  TMultiGraph *mg = new TMultiGraph();
  //mg->Add(g1,"L");
  //mg->Add(g2,"L");
  //mg->Add(g3,"L");
  //mg->Add(g4,"L");
  //mg->Draw()
  
  TCanvas *cc_x= new TCanvas("cc",fnam+"_X",1400,500);
  cc_x->cd();

  TLatex *t1x = new TLatex(0.05,0.93,fnam+"_X");
  t1x->SetTextColor(kBlack);
  t1x->Draw();

  TLatex *t2x = new TLatex(0.3,0.93,"#Delta_2H00.XPOS");
  t2x->SetTextColor(kRed);
  t2x->Draw();

  TLatex *t4x = new TLatex(0.43,0.93,"#Delta_2H02.XPOS");
  t4x->SetTextColor(kBlue);
  t4x->Draw();

  TLatex *t5x = new TLatex(0.55,0.93,hps_t_scale_txt);
  t5x->SetTextColor(kBlack);
  t5x->Draw();

  TLatex *t6x = new TLatex(0.68,0.93,hps_sc_scale_txt);
  t6x->SetTextColor(kBrown);
  t6x->Draw();

  t7->Draw();

  TPad *p1x=new TPad("p1","",0,0,1,1);
  p1x->SetFillColor(0);
  p1x->SetFillStyle(4000);
  p1x->Draw();
  p1x->cd();

  g2_x->SetTitle("");
  g2_x->SetLineColor(kRed);
  g2_x->SetLineWidth(2);
  //  g2_x->GetYaxis()->SetLabelColor(kRed);
  //  g2_x->GetYaxis()->SetLabelOffset(0.055);
  //g2_x->GetYaxis()->SetAxisColor(kRed);
  g2_x->GetYaxis()->SetTickSize(0.02);
  g2_x->SetMinimum(-1.);
  g2_x->SetMaximum(1.);
  g2_x->Draw("AL");

  g1->Draw("L");

  //  for (int i=0;i<g3->GetN();i++) g3->GetY()[i] = g3->GetY()[i]-1.5;  //  Move Down by 1.5
  g3_x->SetTitle("");
  g3_x->SetLineColor(kGreen);
  g3_x->SetLineWidth(2);
  //  g3->Draw("L");

  g4_x->SetTitle("");
  g4_x->SetLineColor(kBlue);
  g4_x->SetLineWidth(2);
  g4_x->Draw("L");

  g5->Draw("L");

  g6->Draw("L");

  g7_x->SetLineColor(kGreen);
  g8_x->SetLineColor(kYellow);

  cc_y->Update();
  TFile *fout= new TFile("cc_plots.root","UPDATE");
  cc_y->Write("cc_y_"+fnam);
  cc_y->SaveAs("cc_y_"+fnam+".pdf");    

  cc_x->Update();
  cc_x->Write("cc_x_"+fnam);
  cc_x->SaveAs("cc_x_"+fnam+".pdf");    

  fout->Close();
  delete fout;
  gSystem->Exit(1);

}
