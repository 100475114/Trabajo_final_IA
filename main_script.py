
from MFIS_Classes import *
from MFIS_Read_Functions import *


def main():
    # read files
    inputFuzzySets = readFuzzySetsFile('InputVarSets.txt')
    outputFuzzySets = readFuzzySetsFile('Risks.txt')
    rules = readRulesFile()
    applications = readApplicationsFile()
    # process all the applications and write Rests file
    outputFile = open ('Results. txt', "w")
    for application in applications:
        centroid = processApplication(application, inputFuzzySets, outputFuzzySets, rules)
        outputFile.write(application.appId + " " + str(centroid)+ "\n")
    outputFile.close()