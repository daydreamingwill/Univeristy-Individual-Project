def convert(inputLocation, outputLocation, columnNames=[], spaced=True):
    with open(inputLocation, 'r') as inputFile:
        with open(outputLocation, 'a') as outputFile:
            columns = ''
            print (columnNames)
            numOfColumns = len(columnNames)

            columnCount = 0
            
            for column in columnNames:
                if columnCount < numOfColumns-1:
                    columns = columns + column + ', '
                    
                else:
                    columns = columns + column

                columnCount += 1

            columns = columns + '\n'
            outputFile.write(columns)

            totalLineCount = 0
            lineCount = 0
            row = ''

            for line in inputFile:
                if totalLineCount%50000 == 0:
                    print(totalLineCount)
                
                if lineCount < numOfColumns-1:
                    row = row + line.replace('\n', '') + ', '
                    lineCount += 1

                elif (lineCount == numOfColumns-1) and spaced == True:
                    row = row + line.replace('\n', '')
                    lineCount += 1

                else:
                    row = row + '\n'
                    outputFile.write(row)
                    
                    row = ''
                    lineCount = 0

                totalLineCount += 1
