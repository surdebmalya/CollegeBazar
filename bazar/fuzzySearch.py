def levenshteinDistance(s, t):
    
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for i in range(1, rows):
        dist[i][0] = i

    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                dist[row][col-1] + 1,      # insertion
                                dist[row-1][col-1] + cost) # substitution

    return dist[row][col]



def luceneFuzzySearchPercentage(list, text, threshold):    # similarity=(longerLength(x,y) - levenshteinDistance(x,y)) / longerLength(x,y)
    res = []
    for s in list:
        t = []
        
        dist = levenshteinDistance(s[0], text)
        l = float(max(len(s[0]),len(text)))
        score = (l - dist)/l
        score = round(score*100, 2)

        if(score >= threshold):
            t.append(s)
            t.append(score)
            res.append(t)
    
    return res

