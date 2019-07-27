#!/usr/bin/env python
#
import sys
import argparse
import ROOT
import numpy as np
import datetime
import subprocess

def dtime(value):
    """ Special function to parse the -b and -e command line args, which may contain a - """
    return value

def convert_to_float(val):
    """ A more tolerant converter than the float() call, catches some exceptions. """

    try:
        out = float(val)
    except ValueError:
        if val == "<undefined>":
            out = 0
        else:
            print("Unexpected value: ",val)
            out= None

    return out

def main(argv=None):
    if argv is None:
        argv=sys.argv


    Channels = ['IPM2C21A.VAL','IPM2C21A.XPOS','IPM2C21A.YPOS',
                'IPM2C24A.VAL','IPM2C24A.XPOS','IPM2C24A.YPOS',
                'IPM2H01.VAL' ,'IPM2H01.XPOS' ,'IPM2H01.YPOS',
                'IPM2H00.XPOS','IPM2H00.YPOS',
                'IPM2H02.XPOS','IPM2H02.YPOS',
                'scaler_calc1',   # FCUP
                'scalerS12b.VAL', # HPS_L
                'scalerS13b.VAL', # HPS_R
                'scalerS14b.VAL', # HPS_T
                'scalerS15b.VAL'] # HPS_SC
    Trig_Channels = ['B_DAQ_HPS:VTP:rate:00',  # Single-0 Top
                    'B_DAQ_HPS:VTP:rate:01',  # Single-1
                    'B_DAQ_HPS:VTP:rate:02',  # Single-2
                    'B_DAQ_HPS:VTP:rate:03',  # Single-3
                    'B_DAQ_HPS:VTP:rate:04',  # Single-0
                    'B_DAQ_HPS:VTP:rate:05',  # Single-1
                    'B_DAQ_HPS:VTP:rate:06',  # Single-2
                    'B_DAQ_HPS:VTP:rate:07',  # Single-3
                    'B_DAQ_HPS:VTP:rate:08',  # Pair-0
                    'B_DAQ_HPS:VTP:rate:09',  # Pair-1
                    'B_DAQ_HPS:VTP:rate:10',  # Pair-2
                    'B_DAQ_HPS:VTP:rate:11',  # Pair-3
#                    'B_DAQ_HPS:VTP:rate:12',  # LED
#                    'B_DAQ_HPS:VTP:rate:13',  # Cosmic
#                    'B_DAQ_HPS:VTP:rate:14',  # Hodoscope
#                    'B_DAQ_HPS:VTP:rate:15',  # Pulser
                    'B_DAQ_HPS:VTP:rate:16',  # Multiplicity-0 (2Gamma)
                    'B_DAQ_HPS:VTP:rate:17',  # Multiplicity-1 (3Gamma)
                    'B_DAQ_HPS:VTP:rate:18',  # FEE Top
                    'B_DAQ_HPS:VTP:rate:19',  # FEE Bottom
                    'B_DAQ_HPS:TSFP:rate:15',  # FCup
                    'B_DAQ_HPS:TSGTP:sum',    # Trigger Sum
                    ]

    translate = { 'scaler_calc1'  :'FCUP',
                  'scalerS12b.VAL':'HPS_L',
                  'scalerS13b.VAL':'HPS_R',
                  'scalerS14b.VAL':'HPS_T',
                  'scalerS15b.VAL':'HPS_SC',
                  'B_DAQ_HPS:VTP:rate:00':"Single0_Top",
                  'B_DAQ_HPS:VTP:rate:01':"Single1_Top",
                  'B_DAQ_HPS:VTP:rate:02':"Single2_Top",
                  'B_DAQ_HPS:VTP:rate:03':"Single3_Top",
                  'B_DAQ_HPS:VTP:rate:04':"Single0_Bot",
                  'B_DAQ_HPS:VTP:rate:05':"Single1_Bot",
                  'B_DAQ_HPS:VTP:rate:06':"Single2_Bot",
                  'B_DAQ_HPS:VTP:rate:07':"Single3_Bot",
                  'B_DAQ_HPS:VTP:rate:08':"Pair0",
                  'B_DAQ_HPS:VTP:rate:09':"Pair1",
                  'B_DAQ_HPS:VTP:rate:10':"Pair2",
                  'B_DAQ_HPS:VTP:rate:11':"Pair3",
#                  'B_DAQ_HPS:VTP:rate:15':"Pulser",
                  'B_DAQ_HPS:VTP:rate:16':"Mult0",
                  'B_DAQ_HPS:VTP:rate:17':"Mult1",
                  'B_DAQ_HPS:VTP:rate:18':"FEE_Top",
                  'B_DAQ_HPS:VTP:rate:19':"FEE_Bot",
                  'B_DAQ_HPS:TSFP:rate:15':"FCup",
                  'B_DAQ_HPS:TSGTP:sum':"TrigSum"
                   }

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=
"""A MYA to ROOT converter.

Examples:

{} -b -3h -e -1h -c
{} -b "2015-05-04 02:00:54"  -e  "2015-05-04 02:05:17" -c scaler_calc1 IPM2H02.YPOS scalersS14b

If you ommit the list of EPICS variables, a standard HPS list will be used.
The standard list includes the BPMs and the FCUP current, plus the HPS scalers.

Note: If you request a long time span, the myData command will take a long time.""".format(sys.argv[0],sys.argv[0]),

    epilog="""For more information, or errors, please email: maurik@physics.unh.edu """)


    parser.add_argument('-f','--file',type=str,help='Get the data from the specified file',default=None)
    parser.add_argument('-z','--gzip',action='store_true',help='File to be readin is gzipped.')
    parser.add_argument('-o','--outfile',type=str,help='Name of the output root file.',default=None)
    parser.add_argument('-b','--begin',action='store',type=dtime,help='Begin time, passed on to MYA. Can be relative time. To use negative values, precede with an x as in x-12h',default=None)
    parser.add_argument('-e','--end'  ,action='store',type=dtime,help='End time, passed on to MYA. Can be relative time as in x-1h',default=None)
    parser.add_argument('-p','--precision',type=int,help='Number of digits after period for seconds in time. [0]',default=0)
    parser.add_argument('-i','--interactive',action='store_true',help='Show the graph for each channel and pause until <enter>.')
    parser.add_argument('-x','--tryout',action='store_true',help='Show the Mya command but do not excute it, then quit. You can then copy this and pipe it to a file.')
    parser.add_argument('-c','--cutone',type=int,help='Cut the Delta graphs on the current in data item 1 at N nA')
    parser.add_argument('-d','--debug',action='count',help='Increase debugging verbosity ',default=0)
    parser.add_argument('-t','--trigger',action="store_true",help="Add the HPS trigger channels to the list of variables.")
    parser.add_argument('epics_channels',nargs='*',help='List the epics channels. If none given, standard HPS BPM set will be used.',default=Channels)
    args = parser.parse_args(argv[1:]) # Drop the program name.

    if args.trigger:
        args.epics_channels+=Trig_Channels

    ## --begin and --end can have a preceding x. If so, scrub it.

    if args.begin and ( args.begin[0] == 'x' or args.begin[0] == 'X'):  args.begin=args.begin[1:]
    if args.end   and ( args.end[0] == 'x' or args.end[0] == 'X'):  args.end=args.end[1:]

    if args.debug>1:
        print("Arguments parsed:")
        if args.begin: print(" --begin "+str(args.begin))
        if args.end:   print(" --end   "+str(args.end))

    if args.interactive:
        canv = ROOT.TCanvas("canv","Canvas",800,600);

    outfile="epics.root"

    if args.outfile:
        outfile = args.outfile

    if args.file:
        if args.file[-3:] == ".gz": args.gzip = True

        if args.gzip:
            command_line = 'gzcat '+args.file
            pipe = subprocess.Popen(command_line,shell=True, bufsize=1024*1024, stdout=subprocess.PIPE)
            ff = pipe.stdout
        else:
            ff=open(args.file)

        if not args.outfile:
            outfile = args.file[0:args.file.find('.')] +".root"


    else:
        if args.begin is None or args.end is None:
            print("Please specify begin and end on the command line, or specify an input file. ")
            return(9)

        # According to Popen doc, the command line should be split, but this doesn't actually work.
        #        command_line = ["myData",'-b "'+args.begin+'"','-e "'+args.end+'"',"-p "+str(args.precision)] + args.epics_channels

        command_line = " ".join(["myData",'-b "'+args.begin+'"','-e "'+args.end+'"',"-p "+str(args.precision)] + args.epics_channels)
        if args.tryout:
            print("Command: "+command_line)
            return(1)

        if args.debug:
            print("Subprocess line: "+command_line)

        pipe = subprocess.Popen(command_line,shell=True, bufsize=1024*1024, stdout=subprocess.PIPE)
        ff = pipe.stdout


    root_file = ROOT.TFile(outfile,"RECREATE")
    root_tree = ROOT.TTree("Epics","Tree with Epics data.")

    ll=ff.readline()  # First line is the headers.

    if args.debug:
        print("First line:"+str(ll))

    #####  HEADER TRANSLATION #### HPS SPECIFIC  ############

    for old,new in translate.items():
        if args.debug:
            print("Translate: ",old," to ",new)
        ll = ll.replace(old,new)

    ll = ll.replace(".","_") # ROOT is not cool about var names with .

    headers = ll.split()[1:] # First is "Date"

    ####### READ the first line from the data #########

    ll=ff.readline()         # Values, first 2 are Date Time

    if args.debug:
        print("Second line:"+str(ll))

    (date,time) = ll.split()[0:2]

    if args.precision:
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    else:
        datetime_format = "%Y-%m-%d %H:%M:%S"

    Zero_time = datetime.datetime.strptime(date+" "+time,datetime_format)
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
        if args.debug: print("Tree Booking ",headers[i])
        root_tree.Branch(headers[i],tree_data[i],headers[i]+"/D")

    #
    # We will now read the file line by line and process the data.
    # One complication is that the myData program will give multiple lines with the same time stamp, where only
    # one (or two) of the values change for each of those lines. In such cases the LAST line has all the changed
    # values, and that would be the one we want.
    #
    # We can handle this by storing the last line. If the current line is a newer time then we process the last line.

    repeat_time_counter=0
    last_line = ll
    (date,time) = last_line.split()[0:2]

    last_time = datetime.datetime.strptime(date+" "+time,datetime_format)

    time_precision = 0.5*pow(10, -args.precision)

    for ll in ff:
        (date,time) = ll.split()[0:2]
        this_time = datetime.datetime.strptime(date+" "+time,datetime_format)

        if ( (this_time - last_time).total_seconds() < time_precision ):
            repeat_time_counter += 1
            last_time = this_time
            last_line = ll
            if args.debug > 3: print("Skip time: ",date,time)
            continue                     # Get the next line, don't process.

        # We are at a new time then

        if args.debug > 3: print("Proc time: ",date,time)

        repeat_time_counter=0

        values =  last_line.split()[2:]   # We process the LAST LINE. First 2 entries are data and time, so skip.

        if len(values) != len(headers):
            print("Incorrect data length in line: (",len(values)," != ",len(headers),") \n",ll)
            sys.exit(9)

        for i in range(len(values)):     # Needed to get the data into the TTree
            tree_data[i][0] = convert_to_float(values[i])


        delta_time = (last_time - Zero_time).total_seconds()
        tree_delta_time[0] = delta_time
        last_time = this_time           # Set time for next iteration

        tstamp.append(delta_time)
        root_tree.Fill()

        for i in range(len(values)):
            graph_data[i].append(convert_to_float(values[i]))    # Store column wise.


    # END of file read. Now process the data into the graphs.

    gr_x = np.array(tstamp,dtype='float64')

    print("Data contained ",len(tstamp)," timestamp lines.")

    graphs=[]

    for i in range(len(headers)):
        gr_y = np.array(graph_data[i],dtype="float64")
        print("Creating graph ",i+1," for ",headers[i])
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

        ### Graphs of deviation from mean.

        ave1 =  np.average( gr_y ) ## Average
        std1 =  np.std(  gr_y  )   ## Standard dev.

        if args.cutone:
            ### This assumes that the FIRST item in the data is a CURRENT
            ave2 =  np.average( [ x for x,y in zip(gr_y,graph_data[0]) if y > args.cutone ] )  ## Toss out the outlyers (no beam)
            std2 =  np.std    ( [ x for x,y in zip(gr_y,graph_data[0]) if y > args.cutone ] )  ## Toss out the outlyers (no beam)
        else:
            ave2 =  np.average( [ x for x in gr_y if abs( x - ave1 ) < 2*std1 ] )  ## Toss out the outlyers (no beam)
            std2 =  np.std( [ x for x in gr_y if abs( x - ave1 ) < 2*std1 ] )  ## Toss out the outlyers (no beam)


        gr_y_dif = gr_y - ave2

        grm = ROOT.TGraph(len(gr_x),gr_x,gr_y_dif)
        grm.SetTitle("#Delta_"+headers[i])
        grm.GetXaxis().SetTimeDisplay(1)
        grm.GetXaxis().SetTimeFormat("%d %H:%M:%S")
        grm.GetXaxis().SetTimeOffset(axis_start.Convert())

        grm.SetMinimum( -3.*std2)
        grm.SetMaximum( 3.*std2)

        if args.interactive:
            grm.Draw("AL")
            canv.Update()
            sys.stdin.readline()

        grm.Write("Delta_"+headers[i])  # Write to the file with proper name.

    root_file.Write()
    root_file.Close()

    ####################### Plotting Section ############################





if __name__ == "__main__":
    sys.exit(main())
