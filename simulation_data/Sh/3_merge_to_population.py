import os

################# You need to change this location based on your own path ##############
inLoc = '/dwgsim/simulated_data_with_evolutionary_relationship/data/simulated_raw/'
resLoc = '/dwgsim/simulated_data_with_evolutionary_relationship/data/simulated_fastq/'


genomeNames = ['NC_009515.1','NC_014932.1','NC_020995.1']
insertionLength = 400

def merge_group(group,groupName):
    #make dir
    resGroupDir = resLoc+groupName
    if not os.path.exists(resGroupDir):
        os.mkdir(resGroupDir)

    for genome in genomeNames:
        numHaplotype = group[0][0]
        allCoverageList = group[1]
        populationTotalCoverages = group[5]
        mutateList = group[2]
        readList = group[3]
        errorRateList = group[4]
        similarityList = group[6]
        hapTypeList = group[7]


        # for hapID in range(1, numHaplotype + 1):
        for coverage in populationTotalCoverages:
            for coverageCouple in allCoverageList:
                individualCoverageList =  [coverage * c * 1.0 / sum(coverageCouple)
                                           for c in coverageCouple]
                #oneCoverage = individualCoverageList[hapID-1]
                for mutatePercentage in mutateList:
                    for readLen in readList:
                        for errorRate in errorRateList:
                            for similarity in similarityList:
                                for hapType in hapTypeList:
                                    groupForward = []
                                    groupReverse = []
                                    for hapID in range(1,numHaplotype+1):
                                        oneCoverage = individualCoverageList[hapID - 1]
                                        tmpName = '_'.join([genome,str(mutatePercentage),
                                                            str(hapID), str(readLen),
                                                            str(insertionLength),
                                                            str(oneCoverage), str(errorRate),
                                                            str(similarity),hapType])
                                        fileName_forward = tmpName + '.bwa.read1.fastq'
                                        fileName_reverse = tmpName + '.bwa.read2.fastq'
                                        groupForward.append(fileName_forward)
                                        groupReverse.append(fileName_reverse)



                                coverageInfo = 'a'.join([str(one)
                                                         for one in individualCoverageList])
                                resName = resLoc+groupName+'/' + \
                                          '_'.join([genome,str(mutatePercentage),
                                                    str(readLen),str(insertionLength),
                                                    str(coverageInfo), str(errorRate),
                                                    str(similarity),hapType])
                                command1 = 'cat '
                                for fileName in groupForward:
                                    command1 += inLoc + groupName+'/' + fileName + ' '
                                command2 = 'cat '
                                for fileName in groupReverse:
                                    command2 += inLoc + groupName+'/' + fileName + ' '

                                command1 += '> '+resName+'.read1.fastq'
                                command2 += '> '+resName+'.read2.fastq'
                                print resName
                                os.system(command1)
                                os.system(command2)


#1.number of haplotype: 2
#2.proportions: 30/70
#3.mutation rate:   0.01%
#4.read length: 100bp
#5.error rate:  1%
#6.coverage:    50

Sh_1 = [[3],[(10,30,60), (5,25,70)],[0.01],[100],[0.001],[200,300,400,500],
          [0.3],['t1']]
merge_group(Sh_1, 'Sh_1')

Sh_2 = [[4],[(5,15,25,55), (5,10,35,50)],[0.01],[100],[0.001],
          [200,300,400,500],[0.3],['t2']]
merge_group(Sh_2, 'Sh_2')

Sh_3 = [[4],[(5,15,25,55), (5,10,35,50)],[0.01],[100],[0.001],
          [200,300,400,500],[0.3],['t3']]
merge_group(Sh_3, 'Sh_3')

print 'done'
