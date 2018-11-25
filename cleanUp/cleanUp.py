def clean(inputLocation, outputLocation, dirtyWords=[]):
    with open(inputLocation, 'r') as inputFile:
        with open(outputLocation, 'a') as outputFile:
            lineCount = 0
            
            for line in inputFile:
                lineCount += 1

                if lineCount%50000 == 0:
                    print(lineCount)

                lineClean = True
                
                for dirtyWord in dirtyWords:
                    if dirtyWord in line:
                        lineClean = False
                        break

                if lineClean == True:
                    outputFile.write(line)
