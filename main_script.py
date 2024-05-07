
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


def fuzzify(app, inputFuzzySets):
    for var, value in app.data:
        for setid in inputFuzzySets:
            if inputFuzzySets[setid].var == var:
                inputFuzzySets[setid].memDegree = skf.interp_membership(inputFuzzySets[setid].x, inputFuzzySets[setid].y, value)

def evaluateAntecedent(rule, inputFuzzySets):
    rule.strength = 1
    for setid in rule.antecedent:
        rule.strength = min(rule.strength, inputFuzzySets[setid].memDegree)

def evaluateConsequent(rule, outputFuzzySets):
    rule.consequentX = outputFuzzySets[rule.consequent].x
    rule.consequentY = outputFuzzySets[rule.consequent].y
    rule.consequentY = np.minimum(rule.consequentY, rule.strength)

def composition(rule, appOutY):
    return np.maximum(rule.consequentY, appOutY)

def processApplication(app, inputFuzzySets, outputFuzzySets, rules):
    appOutX = outputFuzzySets[list(outputFuzzySets.keys())[0]].x  # Assuming all output fuzzy sets share the same universe
    appOutY = np.zeros_like(appOutX)
    # step 1: fuzzification
    fuzzify(app, inputFuzzySets)
    # step 2: inference
    for r in rules:
        # step 2.1: compute strength of the antecedent
        evaluateAntecedent(r, inputFuzzySets)
        # step 2.2: clip the consequent
        evaluateConsequent(r, outputFuzzySets)
        # step 2.3: accumulate the output
        appOutY = composition(r, appOutY)
    # step 3: defuzzification
    centroid = skf.centroid(appOutX, appOutY)
    return (centroid)


main()
