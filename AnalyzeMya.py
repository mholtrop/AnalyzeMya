#!/usr/bin/python
#
import sys
import argparse
import ROOT
import numpy as np
import datetime


def main(argv=None):
    if argv is None:
        argv=sys.argv

    parser = argparse.ArgumentParser(description="""A MYA to ROOT converter.""",
    epilog="""For more information, or errors, please email: maurik@physics.unh.edu """)
    parser.add_argument('-f','--file',type=str,help='Get the data from the specified file',default=None)
    parser.add_argument('-o','--outfile',type=str,help='Name of the output root file.',default=None)
    parser.add_argument('-b','--begin',type=str,help='Begin time, passed on to MYA. Can be relative time as in -12h',default=None)
    parser.add_argument('-e','--end'  ,type=str,help='End time, passed on to MYA. Can be relative time as in -12h',default=None)    
    parser.add_argument('-i','--interactive',action='store_true',help='Show the graph for each channel and pause until <enter>.')
    parser.add_argument('-d','--debug',action='count',help='Increase debugging verbosity ')
    args = parser.parse_args(argv[1:]) # Drop the program name.

    Channels = ('IPM2C21A.VAL','IPM2C21A.XPOS','IPM2C21A.YPOS',
                'IPM2C24A.VAL','IPM2C24A.XPOS','IPM2C24A.YPOS',
                'IPM2H01.VAL' ,'IPM2H01.XPOS' ,'IPM2H01.YPOS',
                'IPM2H00.XPOS','IPM2H00.YPOS',
                'IPM2H02.XPOS','IPM2H02.YPOS',
                'scalerS12b.VAL','scalerS13b.VAL','scalerS14b.VAL','scalerS15b.VAL')
                
    if args.interactive:
        canv = ROOT.TCanvas("canv","Canvas",800,600);

    outfile="epics.root"
    if args.file:
        ff=open(args.file)        
        
        if args.outfile:
            outfile = args.outfile
        else:
            outfile = args.file +".root"

    else:
        pass
        ######### TO DO: Pipe the myData command. ##############


    root_file = ROOT.TFile(outfile,"RECREATE")
    root_tree = ROOT.TTree("Epics","Tree with Epics data.")

    ll=ff.readline()  # First line is the headers.
    ll = ll.replace(".","_") # ROOT is not cool about var names with .
    headers = ll.split()[1:] # First is "Date"
    
    ll=ff.readline()         # Values, first 2 are Date Time
    (date,time) = ll.split()[0:2]
    
    ff.seek(0)    # rewind
    ff.readline() # headers again

    Zero_time = datetime.datetime.strptime(date+" "+time,"%Y-%m-%d %H:%M:%S") #[ int(x) for x in date.split('-') + time.split(':') ]
    axis_start = ROOT.TDatime(Zero_time.year,Zero_time.month,Zero_time.day,Zero_time.hour,Zero_time.minute,Zero_time.second)
    ROOT.gStyle.SetTimeOffset(axis_start.Convert())
    
    tstamp=[]
    graph_data=[ []  for i in range(len(headers)) ]   # Create an empty array of arrays to store the results. We want column-wise storage!

    ######## Setup the ROOT Tree ##############################

    tree_delta_time = np.zeros(1,dtype="float64")
    tree_data=[ np.zeros(1,dtype="float64")  for i in range(len(headers)) ]   # Create an array of size 1 arrays of doubles

    root_tree.Branch("time",tree_delta_time,"time/D")

    #    for name,dat in zip(headers,tree_data):
    #        print "Booking ",name
    #        root_tree.Branch(name,dat,name+"/D")

    for i in range(len(headers)):
        if args.debug: print "Tree Booking ",headers[i]
        root_tree.Branch(headers[i],tree_data[i],headers[i]+"/D")

    #
    # We will now read the file line by line and process the data.
    # One complication is that the myData program will give multiple lines with the same time stamp, where only
    # one (or two) of the values change for each of those lines. In such cases the LAST line has all the changed
    # values, and that would be the one we want.
    #
    # We can handle this by storing the last line. If the current line is a newer time then we process the last line.

    repeat_time_counter=0
    last_line = ff.readline()
    (date,time) = last_line.split()[0:2]
    last_time = datetime.datetime.strptime(date+" "+time,"%Y-%m-%d %H:%M:%S")

    for ll in ff:
        (date,time) = ll.split()[0:2]
        this_time = datetime.datetime.strptime(date+" "+time,"%Y-%m-%d %H:%M:%S")

        if ( (this_time - last_time).total_seconds() < 1.0 ):
            repeat_time_counter += 1
            last_time = this_time
            last_line = ll
            if args.debug > 1: print "Skip time: ",date,time
            continue                     # Get the next line, don't process.

        # We are at a new time then

        if args.debug > 1: print "Proc time: ",date,time

        repeat_time_counter=0

        values =  last_line.split()[2:]   # We process the LAST LINE. 
        if len(values) != len(headers):
            print "Incorrect data length in line: (",len(values)," != ",len(headers),") \n",ll
            sys.exit(9)
     
        for i in range(len(values)):
            tree_data[i][0] = values[i]


        delta_time = (last_time - Zero_time).total_seconds() 
        tree_delta_time[0] = delta_time
        last_time = this_time

        tstamp.append(delta_time)

        if args.debug >0:
            print "F: ",tree_delta_time[0],tree_data[0][0],tree_data[1][0],tree_data[6][0]
        root_tree.Fill()
        for i in range(len(values)):
            graph_data[i].append(values[i])    # Store column wise.            
        
    
    # END of file read. Now process the data into the graphs.

    gr_x = np.array(tstamp,dtype='float64')
        
    print "Data contained ",len(tstamp)," timestamp lines."

    graphs=[]

    for i in range(len(headers)):
        gr_y = np.array(graph_data[i],dtype="float64")
        print "Creating graph ",i+1," for ",headers[i]
        gr = ROOT.TGraph(len(gr_x),gr_x,gr_y)
        gr.SetTitle(headers[i])
        gr.GetXaxis().SetTimeDisplay(1)
        gr.GetXaxis().SetTimeFormat("%d %H:%M:%S")
        gr.GetXaxis().SetTimeOffset(axis_start.Convert())

        

        if args.interactive:
            gr.Draw("AL")
            canv.Update()
            sys.stdin.readline()
        
        gr.Write(headers[i])  # Write to the file with proper name.

    root_file.Write()
    root_file.Close()

    ####################### Plotting Section ############################

    
    
    

if __name__ == "__main__":
    sys.exit(main())
