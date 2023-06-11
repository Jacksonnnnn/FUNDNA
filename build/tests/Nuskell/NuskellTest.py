import nuskell.dsdcompiler
import nuskell.crnverifier


def TestTubeAnalysis(testTube, file, replace):
    DefineTranslation(testTube, file, replace)
    DetermineDotParensPlus(testTube, file, replace)
    ListReactions(testTube, file, replace)


def ListReactions(testTube, f, replace):
    f.write("\n\n")
    f.write('-' * 50)
    f.write("\nReactions:\n")
    f.write('-' * 50)
    f.write("\n")

    i = 0
    for reaction in testTube[1]:
        f.write("\tReaction " + str(i) + " - Involved Complexes:\n")
        for id in reaction:
            complex = reaction[id]
            if replace:
                f.write("\t  - " + complex.name.replace('c', '0.').replace('a', '_0').replace('b', '_1') + "\n")
            else:
                f.write("\t  - " + complex.name + "\n")
        i += 1


def DefineTranslation(testTube, f, replace):
    f.write("\n\n")
    f.write('-' * 50)
    f.write("\nTRANSLATION:\n")
    f.write('-' * 50)
    for id in testTube[0]:
        strand = testTube[0][id]
        if replace:
            f.write("\nComplex: " + str(strand.name).replace('c', '0.').replace('a', '_0').replace('b', '_1'))
        else:
            f.write("\nComplex: " + str(strand.name))
        f.write("\n\tEnclosed Domains:\t" + " ".join(map(str, strand.enclosed_domains)))
        f.write("\n\tExterior Domains:\t" + " ".join(map(str, strand.exterior_domains)))
        if strand.concentration is not None:
            f.write("\n\tConcentration:\t\t" + " ".join(map(str, strand.concentration)))
        else:
            f.write("\n\tConcentration:\t\tUndefined")
        f.write("\n\tKernel String:\t\t" + str(strand.kernel_string))
        f.write("\n\tDot-parens-plus:\t" + "".join(strand.structure))
        pairTable = list(strand.pair_table)
        f.write("\n\tPair Table:\t")
        for set in pairTable:
            f.write("\n\t\t" + str(list(set)))

        strandTable = list(strand.strand_table)
        f.write("\n\tStrand Table:\t")
        f.write("\n\t\tDomain:\tLength:")
        f.write("\n\t\t-------\t-------")

        for strands in strandTable:
            for domain in strands:
                f.write("\n\t\t  " + domain.name + "\t  " + str(domain.length))

        f.write("\n")


def DetermineDotParensPlus(testTube, f, replace):
    f.write("\n\n")
    f.write('-' * 50)
    f.write("\nDOT-PARENS-PLUS NOTATION OF COMPLEXES:\n")
    f.write('-' * 50)
    for id in testTube[0]:
        strand = testTube[0][id]
        if replace:
            f.write("\n" + str(strand.name.replace('c', '0.').replace('a', '_0').replace('b', '_1')) + "\n\t" + "".join(
                strand.structure) + "\n\t" + str(strand.kernel_string))
        else:
            f.write("\n" + str(strand.name) + "\n\t" + "".join(strand.structure) + "\n\t" + str(strand.kernel_string))


# CRN Format:
#       # A list of reactions, optionally with reaction rates:
#       # <- this is a comment!
#       B + B -> C    # [k = 1]
#       C + A <=> D   # [kf = 1, kr = 1]
#       <=> A  [kf = 15, kr = 6]
#
#       # Note that you can write multiple reactions in one line:
#       A + 2C -> E [k = 13.78]; E + F <=> 2A  [kf = 13, kr = 14]

andGateFile = open("!andGate.txt", "w+")
andGate = nuskell.dsdcompiler.translate('A_0 + B_0 -> C_0;'
                                        'A_0 + B_1 -> C_0;'
                                        'A_1 + B_0 -> C_0;'
                                        'A_1 + B_1 -> C_1', 'soloveichik2010.ts', modular=True)
TestTubeAnalysis(andGate, andGateFile, False)
andGateFile.close()

# x^2/10 + x/15 + 4/5

# '0.75_0 + X_0 -> G1_1;'
# '0.75_0 + X_1 -> G1_1;'
# '0.75_1 + X_0 -> G1_1;'
# '0.75_1 + X_1 -> G1_0;'

# 'G1_0 + 0.6667_0 -> G2_1;'
# 'G1_0 + 0.6667_1 -> G2_1;'
# 'G1_1 + 0.6667_0 -> G2_1;'
# 'G1_1 + 0.6667_1 -> G2_0;'

# 'G2_0 + G1_0 -> G3_1;'
# 'G2_0 + G1_1 -> G3_1;'
# 'G2_1 + G1_0 -> G3_1;'
# 'G2_1 + G1_1 -> G3_0;'

# 'G3_0 + 0.2_0 -> G4_1;'
# 'G3_0 + 0.2_1 -> G4_1;'
# 'G3_1 + 0.2_0 -> G4_1;'
# 'G3_1 + 0.2_1 -> G4_0'
polynomialFile = open("!polynomial.txt", "w+")
polynomial = nuskell.dsdcompiler.translate('0.75_0 + X_0 -> G1_1;'
                                           '0.75_0 + X_1 -> G1_1;'
                                           '0.75_1 + X_0 -> G1_1;'
                                           '0.75_1 + X_1 -> G1_0;'

                                           'G1_0 + 0.6667_0 -> G2_1;'
                                           'G1_0 + 0.6667_1 -> G2_1;'
                                           'G1_1 + 0.6667_0 -> G2_1;'
                                           'G1_1 + 0.6667_1 -> G2_0;'

                                           'G2_0 + G1_0 -> G3_1;'
                                           'G2_0 + G1_1 -> G3_1;'
                                           'G2_1 + G1_0 -> G3_1;'
                                           'G2_1 + G1_1 -> G3_0;'

                                           'G3_0 + 0.2_0 -> G4_1;'
                                           'G3_0 + 0.2_1 -> G4_1;'
                                           'G3_1 + 0.2_0 -> G4_1;'
                                           'G3_1 + 0.2_1 -> G4_0'.replace('0.', 'c'),
                                              'soloveichik2010.ts', modular=True)
TestTubeAnalysis(polynomial, polynomialFile, True)
polynomialFile.close()

simpleReactionFile = open("!simple.txt", "w+")
simpleReaction = nuskell.dsdcompiler.translate('A + B -> C', 'soloveichik2010.ts', modular=True)
TestTubeAnalysis(simpleReaction, simpleReactionFile, False)
simpleReactionFile.close()

# this is the formal crn (fcrn) and formal species (fs)
fcrn, fs = nuskell.dsdcompiler.crn_parser.parse_crn_string('A0 + B0 -> C0;'
                                                           'A0 + B1 -> C0;'
                                                           'A1 + B0 -> C0;'
                                                           'A1 + B1 -> C1')

print("-" * 50)
print("CRN:")
print(fcrn)
print("-" * 50)
print("Formal Species:")
print(fs)
print("-" * 50)

# vcrn = [[['A', 'B'], ['C'], 0.3, 0]] # implementation crn (reactants, products, kforward, kreverse)
#
# v = nuskell.crnverifier.verify(fcrn, vcrn, fs, method = 'crn-bisimulation')
#
# if v:
#     print("Input CRN and TestTube-Species are CRN bisimulation equivalent.")
# else:
#     print("Input CRN and TestTube-Species are not CRN bisimulation equivalent.")


# from nuskell import translate, verify
#
# testtube = translate('A+B->C', scheme = 'soloveichik2010.ts')
#
# # Get the enumerated CRN
# testtube.enumerate_reactions()
#
# # Interpret the enumerated CRN, i.e. replace history species
# interpretation = testtube.interpret_species(['A','B','C'], prune=True)
#
# # Formulate reversible reactions as two irreversible reactions.
# fcrn = [[['A','B'],['C']]]
# vcrn = []
# for r in testtube.reactions:
#   rxn = [map(str,r.reactants), map(str,r.products)]
#   vcrn.append(rxn)
#
# v = verify(fcrn, vcrn, fs, method = 'bisimulation')
#
# if v :
#   print("Input CRN and TestTube-Species are CRN bisimulation equivalent.")
# else :
#   print("Input CRN and TestTube-Species are not CRN bisimulation equivalent.")
