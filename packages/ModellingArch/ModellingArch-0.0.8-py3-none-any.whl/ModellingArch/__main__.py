import argparse
import ast
import sympy as sp
import numpy as np
import json
from ModellingArch.Model import Model

parser = argparse.ArgumentParser(
                                 description="A pre-made tool to solve the problem of fitting data to a coninuus markov procces with a given model.\n\n"+
                                            "Pick either an input file or insert the model using the arguments, for larger models it is recommended to mannually make an input file",
                                 allow_abbrev=False)
#Model
parser.add_argument('-Matrix',dest="M", required=False, help ="The square matrix describing the markov chain state diagram where each row will give the diffential equation for the population of that state")
parser.add_argument('-Fs','-FluorescentState',dest="Fs", required=False, help="A list containing tuples with a fluorescent state as the first value and the identifier for the type of light which it depends on")
parser.add_argument('-Lt','-LightDependentTransitions', dest="Lt",required=False, help="A list with for each type of light the transitions which are dependent on it in the same order as light intensities")

#Data
parser.add_argument('-Li','-LightIntensities',dest="Li", required=False, help="A List containing for each type of light dependancy the intensity at which the measurments were taken")
parser.add_argument('-Data', required=False, dest="Data",help= "A 2-dimensional list containing a set of measured apparent rates for each light intensity")

#FixedTransitions
parser.add_argument('-Ft -FixedTransitions', required=False, dest="Ft", help="A list of ordered pairs containing the name of the transition and its value for each fixed transition", default="[]")

#Transition finding settings
parser.add_argument("-Ig","-InitialGuessInterval", dest="Ig", required=False, help="A tuple containing the interval from which the initial guesses will be taken, default is (0,10)",default="(0,10)")
parser.add_argument("-L","-TransitionsLowerBound", dest="Lb", required=False, help="A float which determines the lowest accepted transition rate, default is 1e-10" , default="1e-10")
parser.add_argument("-Mt","-MaxTries", dest="Mt", required=False, help="An integer detemining how many times we want to try and find the transition rates if it has failed with current intial values, default is 50", default="50")

#Solution finding settings
parser.add_argument("-Si","-SolutionInterval", dest="Si", required=False, help="A tuple containing the interval for which the populations will be calculated, default is (0,10)",default="(0,10)")
parser.add_argument("-Ip","-InitialPopulation", dest="Ip", required=False, help="A list containing the initial populations of the system, default is everything in ground state", default="None")
parser.add_argument("-Fss","-FirstStepSize", dest="Fss", required=False, help="The size of the first step taken while numerically solving the system the next step will be dynamically determined, default is 1e-4", default="1e-4")
parser.add_argument("-Ms","-MaxStepSize", dest="Ms", required=False, help="The maximum stepsize that will be taken to calculate the populations determines the resolution of the solution, default is 1e-1", default="1e-1")

#Loading And Saving
parser.add_argument("-In","-InputFilePath",dest="In", required=False, help="The path of the json file containing the model to load")
parser.add_argument("-Out","-OutputFilePath",dest="Out", required=False, help="The path of the json file which will contain the model generated")
parser.add_argument("-DataIn", dest="DIn", required=False,help="Path to a JSON file containing Measurements data")
parser.add_argument("-SkipCalculateTransitions", dest="Ct", required=False,action="store_false",default=True, help="Use this flag if we can skip calculating the transitions")
parser.add_argument("-SkipCalculatePopulations", dest="Pt", required=False,action="store_false",default=True, help="Use this flag if we can skip calculating the populations")

#Temporal Pattern
parser.add_argument("-Tp", "-TemporalPattern", dest="Tp", required=False, help="A list with for each light type its temporal pattern as a sympy function default is all 1", default="[1,1]")

args = parser.parse_args()

#Check if the model is given using the command line or a file
if (not(args.M is None or args.Lt is None or args.Fs is None)):
    M = sp.Matrix(sp.sympify(args.M))

    k = sorted(list(M.free_symbols), key=lambda x : x.name)

    Ldt = sp.sympify(args.Lt)
    Fs = sp.sympify(args.Fs)

    model = Model(M, Ldt, Fs)
#If not given in the command like check if an inputfile was given and load it
elif not args.In is None:
    with open(args.In,'r') as In:
        model = Model.fromJSON(In.read())

#else Throw an error since we dont have a (Full) Model
else:
    raise IOError("Please input all of MATRIX ,FS AND LT  Or give IN")

#Check if all data is filled in and extract it or a file was given
if not (args.Li is None or args.Data is None ):
    LightIntensities = ast.literal_eval(args.Li)
    LightData = ast.literal_eval(args.Data)

    if len(LightData) != len(LightIntensities):
        raise Exception("Length of LightIntensities and Data must be the same")
    else:
        Data = dict(zip(map(tuple,LightIntensities), np.array(LightData) * -1))
elif not (args.DIn is None):
    with open(args.DIn,'r') as In:
        DataFile = json.loads(In.read())
        Data = dict(zip(map(tuple, DataFile['LightIntensities']), np.array(DataFile['LightData']) * -1))

#If there was no data but we need to calculate transitions throw an error
elif args.Ct:
    raise RuntimeError("DATA and LT flag is required if transitions need to be calculated")

#Import the fixed transitions
FixedT = dict(sp.sympify(args.Ft))

#Import the options for the calculating of transitions
InitialGuess = ast.literal_eval(args.Ig)
LowerBound = ast.literal_eval(args.Lb)
MaxTries = ast.literal_eval(args.Mt)

#Interpret the options for calculating the populations
SolutionInterval = ast.literal_eval(args.Si)
InitialValue = ast.literal_eval(args.Ip)
FirstStep = ast.literal_eval(args.Fss)
MaxStep = ast.literal_eval(args.Ms)

#Interpret the temporal patterns
Tp = sp.sympify(args.Tp)

#Run the model
if args.Ct:
    model.calculate_transitions(data=Data,FixedTransitions=FixedT, InitialGuessInterval=InitialGuess,LowerBoundTransitionRates=LowerBound, MaxTries=MaxTries)
if args.Pt:
    model.find_population(SolutionInterval=SolutionInterval,InitialCondition=InitialValue,FirstStepSize=FirstStep,MaxStepSize=MaxStep,TemporalPattern=Tp)

#Plot the Solutions
model.plotSolution()

#Save the model
if not args.Out is None:
    with open(args.Out, 'w') as out:
        out.write(model.toJSON())