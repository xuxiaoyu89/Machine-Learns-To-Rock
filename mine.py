def generateNotes(filename):
    result = []
    for line in open(filename):
        line = line.strip("\n").split()
        result.append(line[0]+line[1])
    return result

print generateNotes("mozart-k331-1.txt")



