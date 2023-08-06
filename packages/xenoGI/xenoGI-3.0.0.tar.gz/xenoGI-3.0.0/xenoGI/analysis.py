import sys,statistics
from .Family import *
from .Island import *
from . import trees
from . import scores
from . import islands

#### Analysis functions

## general

def printTable(L,indent=0,fileF=sys.stdout):
    '''Given tabular data in a list of lists (where sublists are rows)
print nicely so columns line up. Indent is an optional number of blank spaces to put in front of each row.'''
    # get max width for each column
    colMax=[]
    for col in range(len(L[0])):
        mx=0
        for row in L:
            if len(row[col]) > mx:
                mx = len(row[col])
        colMax.append(mx)
    
    # print
    for row in L:
        for col in range(len(row)):
            row[col]=row[col]+' ' * (colMax[col]-len(row[col]))
            
    for row in L:
        printStr = " "*indent + " | ".join(row)
        print(printStr.rstrip(),file=fileF)

def matchFamilyIsland(genesO,gene2FamIslandD,searchStr):
    '''Return the island number, family number, and gene name(s)
associated with searchStr in genesO.geneInfoD. Searches for a match in all
fields of geneInfoD.'''
    # find matching gene names
    geneMatchL=[]
    for geneNum in gene2FamIslandD:
        # use keys of gene2FamIslandD rather than genesO.geneInfoD
        # because they are from scaffold only.
        valueT=genesO.numToGeneInfo(geneNum)
        for value in valueT:
            if type(value)==str:
                if searchStr in value:
                    descrip = valueT[4]
                    geneMatchL.append((geneNum,descrip))
                    break

    # get family numbers and island numbers
    outL=[]
    for geneNum,descrip in geneMatchL:
        geneName = genesO.numToName(geneNum)
        (locusIslandNum,ifamNum,ofamNum,locusFamNum) = gene2FamIslandD[geneNum]
        outL.append((geneName,locusIslandNum,ifamNum,ofamNum,locusFamNum,descrip))
    return outL
        
## Print scores associated with a family

def printScoreMatrix(familyNum,familiesO,genesO,scoresO,scoreType,fileF):
    '''Print a matrix of scores between all the genes in a family given by
familyNum. Scores are provided by scoresO, and we're extracting the
values associated with scoreType in the edges of this graph.
    '''

    familyGeneNumsL = []
    for lfO in familiesO.getFamily(familyNum).getLocusFamilies():
        familyGeneNumsL.extend(lfO.iterGenes())
    
    rowsL = []
    geneNamesL = [genesO.numToName(gn) for gn in familyGeneNumsL]
    rowsL.append([''] + geneNamesL)
    
    for rowi,gn1 in enumerate(familyGeneNumsL):
        row = [genesO.numToName(familyGeneNumsL[rowi])]
        for gn2 in familyGeneNumsL:
            if scoresO.isEdgePresentByEndNodes(gn1,gn2):
                row.append(format(scoresO.getScoreByEndNodes(gn1,gn2,scoreType),".3f"))
            else:
                row.append('-')
        rowsL.append(row)

    printTable(rowsL,indent=2,fileF=fileF)

def printOutsideFamilyScores(familyNum,familiesO,genesO,scoresO,fileF):
    '''Given a family, print scores for all non-family members with a
connection to genes in family. Scores are provided in the network
scoresO.
    '''

    family = familiesO.getFamily(familyNum)
    outsideGeneNumsS = family.getOutsideConnections(scoresO)
    
    rowL = []
    for familyGeneNum in family.iterGenes():
        familyGeneName = genesO.numToName(familyGeneNum)
        for outsideGeneNum in outsideGeneNumsS:
            if scoresO.isEdgePresentByEndNodes(familyGeneNum,outsideGeneNum):
                outsideGeneName = genesO.numToName(outsideGeneNum)
                rawSc=scoresO.getScoreByEndNodes(familyGeneNum,outsideGeneNum,'rawSc')
                synSc=scoresO.getScoreByEndNodes(familyGeneNum,outsideGeneNum,'synSc')
                coreSynSc=scoresO.getScoreByEndNodes(familyGeneNum,outsideGeneNum,'coreSynSc')
                rowL.append([familyGeneName,outsideGeneName,format(rawSc,".3f"),format(synSc,".3f"),format(coreSynSc,".3f")])

    rowL.sort(key=lambda x: x[2],reverse=True) # sort by score
    rowL.insert(0,['----------','-----------','---','---','-------'])
    rowL.insert(0,['Inside fam','Outside fam','Raw','Syn','CoreSyn'])
                
    print("Printing all scores with non-family members",file=fileF)
    printTable(rowL,indent=2,fileF=fileF)

def getEventCountD(originFamiliesO,eventType):
    '''Produce a dict keyed by species node with value a list of counts of
eventType for every locus family at that node.

    '''
    eventCountD = {node:[] for node in originFamiliesO.speciesRtreeO.preorder()}
    for lfO in originFamiliesO.iterLocusFamilies():
        ct = lfO.countEvents(originFamiliesO,eventType)
        if ct != None:
            eventCountD[lfO.lfMrca].append(ct)
    return eventCountD

def getDtlorScoreSummaryD(originFamiliesO,paramD):
    '''Produce a dict keyed by species node with value a list of dtlor
scores for every locus family at that node.

    '''
    dtlorSummaryD = {node:[] for node in originFamiliesO.speciesRtreeO.preorder()}
    for lfO in originFamiliesO.iterLocusFamilies():
        dtlorScore = lfO.dtlorScore(originFamiliesO,paramD)
        if dtlorScore != None and lfO.aabrhHardCore != []:
            dtlorSummaryD[lfO.lfMrca].append(dtlorScore)
    return dtlorSummaryD 
        
def printSummaryD(speciesRtreeO,summaryD):
    '''Print summary stats of values of entries in summaryD (which is
keyed by species node).'''
    for node in speciesRtreeO.preorder():
        L = summaryD[node]
        if L == []:
            print(node,None,None)
        elif len(L) == 1:
            print(node,L[0],None)
        else:
            print(node,round(statistics.mean(L),3),round(statistics.stdev(L),3))
    
## Print all islands at node

def printIslandLSummary(islandL,fileF):
    '''Given a list of locus islands in islandL (ie a list from a single node),
print a simple tabular summary indicating how many locus families they
have.
    '''
    lenL = []
    for isl in islandL:
        lenL.append(len(isl)) # len of island is num families

    # count how many times each length occurs
    lnCtD = {}
    for ln in lenL:
        if ln in lnCtD:
            lnCtD[ln] += 1
        else:
            lnCtD[ln] = 1

    # print out
    printL = []
    row = ['Num LocusFamilies in LocusIsland','Number of occurrences']
    printL.append(row)
    
    for ln,occurrences in sorted(lnCtD.items()):
        printL.append([str(ln), str(occurrences)])

    printTable(printL,indent=8,fileF=fileF)

def vPrintLocusIsland(island,rootFocalClade,subtreeD,familiesO,genesO,fileF):
    '''Verbose print of a locus island.'''

    print("  LocusIsland",island.id,file=fileF)

    # get species nodes subtended by this mrca
    speciesNodesT = subtreeD[island.mrca].leaves()
    
    # put everything in lists.
    printL=[]
    printL.append(['LocusFamily','lfOrig','Family'])
    for node in speciesNodesT:
        printL[0].append(node)

    # print table of family (row) by gene (col)
    for locusFamO in island.iterLocusFamilies(familiesO):
        newRow=[]
        newRow.append(str(locusFamO.locusFamNum))
        newRow.append(locusFamO.origin(familiesO,rootFocalClade))
        newRow.append(str(locusFamO.famNum))
        for node in speciesNodesT:
            entryL = []
            for geneNum in locusFamO.iterGenesByStrain(node):
                infoT=genesO.numToGeneInfo(geneNum)
                geneName,commonName,locusTag,proteinId,descrip,chrom,start,end,strand=infoT
                commonGeneName = "("+commonName+")" if commonName != '' else ''
                entryL.append(geneName + commonGeneName)
                
            if entryL == []:
                entry = ''
            else:
                entry = ",".join(entryL)

            newRow.append(entry)
        printL.append(newRow)
       
    printTable(printL,indent=4,fileF=fileF)

    # print genes and descriptions
    print(file=fileF)
    for locusFamO in island.iterLocusFamilies(familiesO):
        print("    Locus Family",locusFamO.locusFamNum,file=fileF)
        printL = []
        for geneNum in locusFamO.iterGenes():
            infoT=genesO.numToGeneInfo(geneNum)
            geneName,commonName,locusTag,proteinId,descrip,chrom,start,end,strand=infoT
            printL.append([geneName,descrip])

        printTable(printL,indent=4,fileF=fileF)
        print(file=fileF)

    return
    
def vPrintLocusIslandsAtNode(islandL,rootFocalClade,subtreeD,familiesO,genesO,fileF):
    '''Print a list of islands at a single node.'''
    print("  Summary",file=fileF)
    printIslandLSummary(islandL,fileF)
    print("  -------",file=fileF)
    for island in islandL:
        vPrintLocusIsland(island,rootFocalClade,subtreeD,familiesO,genesO,fileF)
        print('  ------',file=fileF)

def vPrintAllLocusIslands(islandByNodeD,speciesRtreeO,rootFocalClade,subtreeD,familiesO,genesO,fileF):
    '''Loop over all nodes in speciesRtreeO, printing islands at each. '''
    focalRtreeO = speciesRtreeO.subtree(rootFocalClade)
    for node in focalRtreeO.preorder():
        print('########################### ',"Locus Islands at node",node,file=fileF)
        print('',file=fileF)
        vPrintLocusIslandsAtNode(islandByNodeD[node],rootFocalClade,subtreeD,familiesO,genesO,fileF)

def printAllLocusIslandsTsv(islandByNodeD,speciesRtreeO,rootFocalClade,familiesO,genesO,fileF):
    '''Loop over all nodes in speciesRtreeO, printing locus islands at each in tsv form. '''

    # header
    headerTxt = """# Format: locusIslandNum <tab> mrca <tab> locusFamilyOriginStr <tab> [Locus Families and genes in locusIsland]
# The remaining part of each line is organized by locus family
# locusFamilyNum,geneA,geneB <tab> locusFamilyNum,geneC,geneD etc.
# for however many locusFamilies there are."""
    print(headerTxt,file=fileF)
    # print locusIslands
    focalRtreeO = speciesRtreeO.subtree(rootFocalClade)
    for node in focalRtreeO.preorder():
        for island in islandByNodeD[node]:
            oStr = island.getLocusFamilyOriginStr(familiesO,rootFocalClade)
            printL=[str(island.id),str(island.mrca),oStr]
            for locusFamO in island.iterLocusFamilies(familiesO):
                lfamGeneL=[str(locusFamO.locusFamNum)]
                for geneNum in locusFamO.iterGenes():
                    infoT=genesO.numToGeneInfo(geneNum)
                    geneName,commonName,locusTag,proteinId,descrip,chrom,start,end,strand=infoT
                    lfamGeneL.append(geneName)
                printL.append(",".join(lfamGeneL))
            print("\t".join(printL),file=fileF)
    return
    
def createGene2FamIslandD(islandByNodeD,originFamiliesO):
    '''Creates a dictionary keyed by gene number which has the
LocusIsland, Family and LocusFamily for each gene.'''
    D = {}
    for islandsAtNodeL in islandByNodeD.values():
        for locusIslandO in islandsAtNodeL:
            for locusFamO in locusIslandO.iterLocusFamilies(originFamiliesO):
                for gene in locusFamO.iterGenes():
                    ofamNum = locusFamO.famNum
                    ifamNum = originFamiliesO.getFamily(ofamNum).sourceFam
                    D[gene] = (locusIslandO.id,ifamNum,ofamNum,locusFamO.locusFamNum)

    return D

## Print species files with all the genes, grouped by contig

def printSpeciesContigs(geneOrderD,fileStemStr,fileExtensionStr,genesO,gene2FamIslandD,originFamiliesO,rootFocalClade,strainNamesT):
    '''This function produces a set of species specific genome
files. These contain all the genes in a strain laid out in the order
they occur on the contigs. Each gene entry includes LocusIsland and
LocusFamily information, as well as a brief description of the gene's
function.
    '''
    for strainName in strainNamesT:
        if strainName in geneOrderD:
            contigT = geneOrderD[strainName]
            with open(fileStemStr+'-'+strainName+fileExtensionStr,'w') as fileF:
                headerStr = """# Lines not beginning with # have the following format: Gene name <tab> family origin <tab> gene history string <tab> locusIsland <tab> initialFamily <tab> originFamily <tab> locusFamily <tab> locFamMRCA <tab> gene description."""
                print(headerStr,file=fileF)
                for contig in contigT:
                    print("########### Begin contig",file=fileF)
                    printGenes(contig,genesO,gene2FamIslandD,originFamiliesO,rootFocalClade,fileF=fileF)
    return
    
## Print neighborhood of an island

def printLocusIslandNeighb(islandNum,synWSize,subtreeD,islandByNodeD,originFamiliesO,geneOrderD,gene2FamIslandD,genesO,rootFocalClade,fileF):
    '''Print the neighborhood of an island. We include the genes in the island and synWSize/2 genes in either direction.'''

    def printCoordinates(labelText,genesO,firstGene,lastGene,fileF):
        chrom = genesO.numToGeneInfo(firstGene)[5]
        startPos = genesO.numToGeneInfo(firstGene)[6]
        endPos = genesO.numToGeneInfo(lastGene)[7]
        print("    "+labelText,chrom+":"+str(startPos)+"-"+str(endPos),file=fileF)


    print("  LocusIsland:",islandNum,file=fileF)
    
    genesInEitherDirec = int(synWSize/2)

    # get the island object for this islandNum
    for listOfIslands in islandByNodeD.values():
        _,island = islands.searchLocIslandsByID(listOfIslands,islandNum)
        if island != None: break

    if island == None:
        raise ValueError("LocusIsland "+str(islandNum)+" not found.")
        
    mrca = island.mrca
    print("  mrca:",mrca,file=fileF)

    for strainName in subtreeD[mrca].leaves():

        print("  In",strainName,file=fileF)

        islandGenesInStrainL = getIslandGenesInStrain(island,strainName,originFamiliesO)

        if islandGenesInStrainL == []:
            print("the island is not found.",file=fileF)
        else:

            neighbGenesL,firstIslandGene,lastIslandGene=getNeighborhoodGenes(strainName,geneOrderD,islandGenesInStrainL,genesInEitherDirec)

            printCoordinates("Coordinates of locus island",genesO,firstIslandGene,lastIslandGene,fileF)
            printCoordinates("Coordinates of region shown",genesO,neighbGenesL[0],neighbGenesL[-1],fileF)

            printGenes(neighbGenesL,genesO,gene2FamIslandD,originFamiliesO,rootFocalClade,islandGenesInStrainL,fileF)

            
            
def getIslandGenesInStrain(island,strainName,familiesO):
    '''Given an island, a strain number, and our families object, return
all the genes in the island for that strain.'''
    genesL=[]
    for locFam in island.iterLocusFamilies(familiesO):
        genesL.extend(locFam.iterGenesByStrain(strainName))
    return genesL

def getNeighborhoodGenes(strainName,geneOrderD,islandGenesInStrainL,genesInEitherDirec):
    '''Find and return genes in the neighborhood of those given in
islandGenesInStrainL. firstGene and lastGene are the first and last
genes in the island itself.'''
    neighbGenesL=[]
    for contig in geneOrderD[strainName]:
        try:
            # get index of all of these. We're assuming they're on
            # the same contig and in the same area.
            indL=[contig.index(gene) for gene in islandGenesInStrainL]
            maxInd = max(indL)
            minInd = min(indL)
            end = maxInd + genesInEitherDirec +1
            st = minInd-genesInEitherDirec if minInd-genesInEitherDirec>0 else 0 # st can't be less than 0
            neighbGenesL=contig[st:end]

            # get gene numbers of first and last genes in island
            firstGene = contig[minInd]
            lastGene = contig[maxInd]
            
            return neighbGenesL,firstGene,lastGene
        except ValueError:
            continue

def printGenesInteractive(neighbGenesL,genesO,gene2FamIslandD,islandGenesInStrainL,familiesO,fileF):
    '''Given a list of contiguous genes, print them out nicely with
information on locus family and locus island etc.'''

    # now print the neighbors
    rowsL=[]
    for geneNum in neighbGenesL:

        infoT=genesO.numToGeneInfo(geneNum)
        geneName,commonName,locusTag,proteinId,descrip,chrom,start,end,strand=infoT

        
        locIslNum,famNum,locFamNum = gene2FamIslandD[geneNum]
        lfMrca = familiesO.getLocusFamily(locFamNum).lfMrca

        # mark genes in the island with a *
        if geneNum in islandGenesInStrainL:
            geneName = '* '+geneName
        else:
            geneName = '  '+geneName

        infoL = [geneName,"locIsl:"+str(locIslNum),"ofam:"+str(famNum),"locFam:"+str(locFamNum),"lfMrca:"+lfMrca,descrip]

        rowsL.append(infoL)

    printTable(rowsL,indent=4,fileF=fileF)

def printGenes(neighbGenesL,genesO,gene2FamIslandD,originFamiliesO,rootFocalClade,islandGenesInStrainL=[],fileF=sys.stdout):
    '''Given a list of contiguous genes, print them out including

       Gene name,geneOrigin,geneHisStr,locusIsland,ifamNum,ofamNum,locFamNum,locFamMRCA,geneDescription.

       If islandGenesInStrainL is passed in, we assume we're in
       interactive mode, and print in a tabular way. In this case we
       also put * next to any genes in that are in
       islandGenesInStrainL. If this list is empty, we we're in print
       analysis, and print tab delimited.
    '''
    # get strains in focal clade
    focalSubRtreeO = originFamiliesO.speciesRtreeO.subtree(rootFocalClade)
    focalCladeStrainsS = set(focalSubRtreeO.leaves())
    rowsL=[]

    if islandGenesInStrainL != []:
        rowsL.append(['geneName','orig','geneHist','locIsl','ifam','ofam','locFam','lfMrca','descrip'])
        
    for geneNum in neighbGenesL:
        strainName = genesO.numToStrainName(geneNum)
        infoT=genesO.numToGeneInfo(geneNum)
        geneName,commonName,locusTag,proteinId,descrip,chrom,start,end,strand=infoT

        # mark off genes in island (if interactive mode)
        if geneNum in islandGenesInStrainL:
            geneName = '* '+geneName
        else:
            geneName = '  '+geneName

        # family info
        locIslNum,ifamNum,ofamNum,locFamNum = gene2FamIslandD[geneNum]
        famO = originFamiliesO.getFamily(ofamNum)
        
        # only print geneHistory,orign if gene is in focal clade
        if strainName in focalCladeStrainsS:
            geneHisStr = famO.getGeneHistoryStr(str(geneNum)) # geneHistoryD has string keys
            geneOrigin = famO.origin(originFamiliesO.speciesRtreeO,rootFocalClade)
        else:
            geneHisStr = ""
            geneOrigin = ""
            
        lfMrca = originFamiliesO.getLocusFamily(locFamNum).lfMrca

        infoL = [geneName,geneOrigin,geneHisStr,str(locIslNum),str(ifamNum),str(ofamNum),str(locFamNum),lfMrca,descrip]

        rowsL.append(infoL)
        

    # now print
    if islandGenesInStrainL != []:
        # interactive
        printTable(rowsL,indent=4,fileF=fileF)
    else:
        for infoL in rowsL:
            print("\t".join(infoL),file=fileF)
        
    return
