"""
This program allows pgn files(a file containing chess games) to be searched for
a specific type of chess game event and for events of that type to be put into
a new output file. For example, a file could include events such as
"Rated Classical game", "Rated Bullet game", "Rated Blitz tournament", etc.
Stockfish analysis, turn notation, labels and anotation can also be optionaly
removed(by default False).
"""
import re

def remove_clock(line):
    """
    """
    processedLine = re.sub(r'(\{ \[\%clk .\:..\:..] } )|((?<=\]) \[\%clk .\:..\:..\])', '', line)

    return processedLine

def stockfish(line):
    """
    Stockfish analysis evaluated moves are in the format "1. e4 { [%eval 0.22]
    } 1... g6 { [%eval 0.55] } 2. d3 { [%eval 0.14] } 2... Bg7 { [%eval 0.26] }
    ". Non stockfish evaluated moves (default moves) are in the format "1. e4
    g6 2. d3 Bg7" This function uses regex to remove the stockfish analysis.
    """
    stockFish = re.search(r'eval', line)

    if stockFish != None:
        return True    
    else:
        return False

def remove_turn_notation(line):
    """
    Moves are in the format "1. e4 Nc6 2. Nf3 g6". "1." and "2." represent the
    current move in the game. This function removes that notation e.g. "e4 Nc6
    Nf3 g6"
    """
    processedLine = re.sub(r'\d*\. ', '', line)

    return processedLine

def remove_redundant_lines(writingSectionCount, redundantLines, processedLine):
    """
    Removes any lines in a game of chess that are not needed.
    """
    if writingSectionCount in range(redundantLines[0], redundantLines[1]):
        return ''

    else:
        return processedLine

def remove_labels(line):
    """
    Removes and labels and leaves only that data e.g. "[WhiteElo "1639"]" to
    1693
    """
    processedLine = re.sub(r'\[\S* \"', '', line)
    processedLine = re.sub(r'\"\]', '', processedLine)
    return processedLine

def remove_annotation(line):
    """
    Removes move anotations(comments) from moves, i.e. "?", "!"
    """
    processedLine = re.sub(r'\?', '', line)
    processedLine = re.sub(r'\!', '', processedLine)

    return processedLine

def remove_move_extra_info(line):
    """
    """
    processedLine = re.sub(r'x', '', line)
    processedLine = re.sub(r'\+', '', processedLine)
    processedLine = re.sub(r'#', '', processedLine)
    processedLine = re.sub(r'\=.', '', processedLine)
    processedLine = re.sub(r'(?<=[KQRBN])([a-h]|[1-8]|[a-h][1-8])(?=[a-h][1-8])',
                           '', processedLine)
    processedLine = re.sub(r'([a-h]|[1-8]|[a-h][1-8])(?=[a-h][1-8] )', '', processedLine)

    return processedLine
    
def search_pgn(inputLocation, outputLocation, eventType, sectionRange,
               removeClock=False, removeStockfish=False, removeTurnNotation=False,
               removeRedundantLines=False, redundantLines=[None, None],
               removeLabels=False, removeAnnotation=False,
               removeMoveExtraInfo=False):
    """
    This function takes and input file location, a location for an output file,
    the event type to be isolated, the section range and whether to remove
    stockfish analysis and turn notation. the section range corresponds to the
    number of line accosiated with each game in the pgn file. events are then
    searched for and written to the output file if they are of the correct type.
    """
    with open(inputLocation, 'r') as inputFile: 
        with open(outputLocation, 'a') as outputFile:
            lineNum = 0
            writingSection = False
            writingSectionCount = 0
            tempFile = open('temp.txt', 'a')
            
            for line in inputFile:
                lineNum += 1

                if lineNum%50000 == 0:
                    print("Line number:", lineNum)
                
                if eventType in line:
                    endLine = lineNum + sectionRange
                    writingSection = True

                if (removeStockfish and writingSection) == True:
                    if stockfish(line) == True:
                        tempFile.close()
                        with open('temp.txt', 'w') as tempFile:
                            tempFile.write('')

                            writingSection = False
                            writingSectionCount = 0
                            tempFile = open('temp.txt', 'a')

                if writingSection == True:
                    writingSectionCount += 1
                    processedLine = line

                    if removeClock == True:
                        processedLine = remove_clock(processedLine)

                    if removeTurnNotation == True:
                        processedLine = remove_turn_notation(processedLine)

                    if removeRedundantLines == True:
                        processedLine = remove_redundant_lines(
                            writingSectionCount, redundantLines, processedLine)

                    if removeLabels == True:
                        processedLine = remove_labels(processedLine)

                    if removeAnnotation == True:
                        processedLine = remove_annotation(processedLine)

                    if removeMoveExtraInfo == True:
                        processedLine = remove_move_extra_info(processedLine)
                    tempFile.write(processedLine)

                    if writingSectionCount == sectionRange:
                        writingSection = False
                        writingSectionCount = 0
                        tempFile.close()

                        with open('temp.txt','r') as tempFile:
                            for tempLine in tempFile:
                                outputFile.write(tempLine)

                        with open('temp.txt', 'w') as tempFile:
                            tempFile.write('')
                            
                        tempFile = open('temp.txt', 'a')                   
