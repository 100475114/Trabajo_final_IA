
from MFIS_Classes import *
from MFIS_Read_Functions import *


def main():
    # read files
    inputFuzzySets = readFuzzySetsFile('InputVarSets.txt')
    outputFuzzySets = readFuzzySetsFile('Risks.txt')
    plot_fuzzy_sets_by_category(inputFuzzySets)
    #plot_output_fuzzy_sets(outputFuzzySets)
    rules = readRulesFile()
    applications = readApplicationsFile()
    # process all the applications and write Rests file
    outputFile = open ('Results. txt', "w")
    for application in applications:
        centroid = processApplication(application, inputFuzzySets, outputFuzzySets, rules)
        outputFile.write(application.appId + " " + str(centroid)+ "\n")
    outputFile.close()
    plt.show()


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

import os

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

    # Plot the aggregated function for each application
    plt.figure()
    plt.plot(appOutX, appOutY, label='Aggregated Function')
    plt.title(f'Aggregated Function for Application {app.appId}')
    plt.xlabel('Universe')
    plt.ylabel('Membership Degree')
    plt.legend()
    if not os.path.exists('figuras'):
        os.makedirs('figuras')
    plt.savefig(f'figuras/Aggregated_Function_{app.appId}.png')
    plt.close()
    return (centroid)


def plot_fuzzy_sets_by_category(fuzzy_sets):
    # Encuentra las categorías únicas
    categories = set(fs.var for fs in fuzzy_sets.values())

    # Graficar cada categoría en una figura separada
    for category in categories:
        plt.figure(figsize=(8, 4))
        for setid, fs in fuzzy_sets.items():
            if fs.var == category:
                plt.plot(fs.x, fs.y, label=f'{fs.label}')
        plt.title(f"Fuzzy Sets for {category}")
        plt.xlabel("Universe")
        plt.ylabel("Membership degree")
        plt.legend()
        if not os.path.exists('figuras'):
            os.makedirs('figuras')
        plt.savefig(f'figuras/Fuzzy_Sets_{category}.png')
        plt.close()

main()

