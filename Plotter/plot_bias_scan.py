
import os, sys, re
import ROOT
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLabelFont(42,"xyz")
ROOT.gStyle.SetLabelSize(0.05,"xyz")
#ROOT.gStyle.SetTitleFont(42)
ROOT.gStyle.SetTitleFont(42,"xyz")
ROOT.gStyle.SetTitleFont(42,"t")
#ROOT.gStyle.SetTitleSize(0.05)
ROOT.gStyle.SetTitleSize(0.06,"xyz")
ROOT.gStyle.SetTitleSize(0.06,"t")
ROOT.gStyle.SetPadBottomMargin(0.14)
ROOT.gStyle.SetPadLeftMargin(0.14)
ROOT.gStyle.SetTitleOffset(1,'y')
#ROOT.gStyle.SetLegendTextSize(0.05)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridColor(13)

one = ROOT.TColor(2001,0.906,0.153,0.094)
two = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four =ROOT.TColor(2004,0.071,0.694,0.18)
five =ROOT.TColor(2005,0.388,0.098,0.608)
six=ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,2,3,4,6,7,5,1,8,9,29,38,46]

standard_pd_signal = 35. #mV

def plot_single_scan(scan_num,graph,graph_pd,graph_norm,graph_temp,graph_norm_lgadbias,graph_current_lgadbias, name,temp):
	cosmetic_tgraph(graph,3)
	cosmetic_tgraph(graph_pd,2)
	cosmetic_tgraph(graph_norm,4)
	cosmetic_tgraph(graph_temp,1)
	cosmetic_tgraph(graph_norm_lgadbias,5)
	cosmetic_tgraph(graph_current_lgadbias,6)

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()
	mgraph.Add(graph_pd)
	mgraph.Add(graph_temp)
	mgraph.Add(graph_current_lgadbias)
	mgraph.Add(graph)
	mgraph.Add(graph_norm)
	mgraph.Add(graph_norm_lgadbias)

	mgraph.SetTitle("; Bias voltage [V]; Average laser response [mV]")
	# graph.Draw("AELP")
	# graph_pd.Draw("ELP same")
	# graph_norm.Draw("ELP same")
	# graph_temp.Draw("ELP same")
	#mgraph.SetMinimum(-5)
	mgraph.Draw("AELP")
	leg = ROOT.TLegend(0.2,0.7,0.59,0.89)
	leg.SetMargin(0.15)
	leg.AddEntry(graph_pd, "Photodiode","EP")
	leg.AddEntry(graph_temp, "Measured temperature [C]","EP")
	leg.AddEntry(graph_current_lgadbias, "Current [#muA]","EP")
	leg.AddEntry(graph, "%s, %i C" % (name,temp),"EP")
	leg.AddEntry(graph_norm, "%s, %i C, norm."%(name,temp),"EP")
	leg.AddEntry(graph_norm_lgadbias, "%s, corrected LGAD bias"%name,"EP")
	
	leg.Draw()
	c.Print("plots/scan%i.pdf"%scan_num)

def plot_overlay(outfile,names,temps,series_num,plottype):
	if plottype==1: filename = "gr"
	if plottype==2: filename = "grlgad"
	if plottype==3: filename = "griv"

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()

	leg = ROOT.TLegend(0.2,0.7,0.59,0.89)
	leg.SetMargin(0.15)

	for i,scan in enumerate(scan_nums):
		graph = outFile.Get(filename+str(scan))
	 	cosmetic_tgraph(graph,i)
		mgraph.Add(graph)
	 	leg.AddEntry(graph, "%s, %i C" %(names[i],temps[i]),"EP")

	mgraph.SetTitle("; Bias voltage [V]; Average laser response [mV]")
	if plottype==3: mgraph.SetTitle("; Bias voltage [V]; Current [#muA]")
	mgraph.Draw("AELP")
	leg.Draw()
	if plottype==1: c.Print("plots/series%i.pdf"%series_num)
	if plottype==2: c.Print("plots/series%i_corr.pdf"%series_num)
	if plottype==3: c.Print("plots/series%i_IV.pdf"%series_num)



def cosmetic_tgraph(graph,colorindex):
	graph.SetLineColor(colors[colorindex])
	graph.SetMarkerColor(colors[colorindex])
	graph.SetMarkerSize(1)
	graph.SetMarkerStyle(20)
	graph.SetTitle("; Bias voltage [V]; Average laser response [mV]")

def get_mean_response_channel(tree,ch):
	hist = ROOT.TH1F("h","",20,0,1000)
	tree.Project("h","amp[%i]"%ch,"")
	return hist.GetMean(),hist.GetMeanError()

def get_mean_response(tree):
	means_this_run=[]
	errs_this_run=[]
	for i in range(17):
		if i==8: continue #trigger
		mean,err = get_mean_response_channel(tree,i)
		means_this_run.append(mean)
		errs_this_run.append(err)
	
	best_mean =  max(means_this_run)
	best_chan = means_this_run.index(best_mean)	
	err = errs_this_run[best_chan]

	#print best_mean,err,best_chan

	return best_mean,err


def get_scan_results(scan_num):
	runs=[]
	biases=[]
	biases_meas=[]
	lgad_biases=[]
	currents_meas=[]
	temps =[] 
	
	mean_responses=[]
	err_responses=[]

	mean_photodiode=[]
	err_photodiode=[]

	mean_responses_norm=[]
	err_responses_norm=[]

	scan_txt_filename = "/home/daq/BiasScan/LBSF/VoltageScanDataRegistry/scan%i.txt" % scan_num
	with open(scan_txt_filename) as scan_txt_file:
		for line in scan_txt_file:
			if line[:1] == "#": continue
			runs.append(int(line.split("\t")[0]))		
		 	biases.append(abs(float(line.split("\t")[1])))
			biases_meas.append(abs(float(line.split("\t")[2])))
			currents_meas.append(1.e6*abs(float(line.split("\t")[3]))) ## convert to microamps

			lgad_biases.append(biases[-1] - 1.1 * currents_meas[-1]) ## 1.1 MOhm in series with LGAD

			temps.append(float(line.split("\t")[4]))

			if biases[-1]>0 and abs(biases_meas[-1]-biases[-1])/biases[-1] > 0.1:
				print "[WARNING]: Scan %i, run %i set to %.0f V, measured at %.0f V" % (scan_num, runs[-1],biases[-1],biases_meas[-1])


	for i,run in enumerate(runs):
		#open root file/tree
		tree = ROOT.TChain("pulse")
		tree.Add("/home/daq/Data/CMSTiming/RawDataSaver0CMSVMETiming_Run%i_0_Raw.root" % run)
		
		mean,err = get_mean_response(tree)
		##photodiode
		mean_pd,err_pd = get_mean_response_channel(tree,18) 
	
		#print mean_pd
		##normalized results
		if mean_pd > 0:
			mean_responses_norm.append( mean * standard_pd_signal/mean_pd )
			err_responses_norm.append( err * standard_pd_signal/mean_pd )

			mean_photodiode.append(mean_pd)
			err_photodiode.append(err_pd)
			mean_responses.append(mean)
			err_responses.append(err)

		else: 
			print "ERROR: run %i has 0 mean_pd"%run
			del biases[i]
			del biases_meas[i]
			del currents_meas[i]
			del temps[i]


	if(len(mean_responses)!=len(biases)): print "ERROR: length of gains does not match length of biases."


	graph = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",mean_responses),array("d",[1 for i in biases]),array("d",err_responses))
	graph_pd = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",mean_photodiode),array("d",[1 for i in biases]),array("d",err_photodiode))
	graph_norm = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",mean_responses_norm),array("d",[1 for i in biases]),array("d",err_responses_norm))
	graph_norm_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",mean_responses_norm),array("d",[1 for i in biases]),array("d",err_responses_norm))
	graph_current_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",currents_meas),array("d",[1 for i in biases]),array("d",[1 for i in biases]))

	graph_temp = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",temps),array("d",[1 for i in biases]),array("d",[0.1 for i in biases]))
	graph_norm.SetName("gr%i"%scan_num)
	graph_norm_lgadbias.SetName("grlgad%i"%scan_num)
	graph_current_lgadbias.SetName("griv%i"%scan_num)
	#mgraph.Add(graph_norm)
	return graph,graph_pd,graph_norm,graph_temp,graph_norm_lgadbias,graph_current_lgadbias
	


if len(sys.argv) < 2:
    sys.exit('Please provide a series number') 

series_num = int(sys.argv[1])
series_txt_filename="series/series%i.txt" % series_num
scan_nums=[]
names=[]
temps=[]
with open(series_txt_filename) as series_txt_file:
		for line in series_txt_file:
			if len(line.split(","))==0: continue
			if line[:1] == "#": continue
			scan_nums.append(int(line.split(",")[0]))		
			names.append(line.split(",")[1])
			temps.append(int(line.split(",")[2]))


outFile = ROOT.TFile("buffer.root","RECREATE")
for i,scan_num in enumerate(scan_nums):
	graph,graph_pd,graph_norm,graph_temp,graph_norm_lgadbias,graph_current_lgadbias = get_scan_results(scan_num)
	graph_norm.Write()
	graph_norm_lgadbias.Write()
	graph_current_lgadbias.Write()
	plot_single_scan(scan_num,graph,graph_pd,graph_norm,graph_temp,graph_norm_lgadbias,graph_current_lgadbias,names[i],temps[i])


outFile.Save()

plot_overlay(outFile,names,temps,series_num,1)
plot_overlay(outFile,names,temps,series_num,2)
plot_overlay(outFile,names,temps,series_num,3)
