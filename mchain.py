from re import sub

comfile = './corpora/comedies/Comedies.txt'
trafile = './corpora/tragedies/Tragedies.txt'
histfile = './corpora/historical/Historicals.txt'

coms = ' '.join(open(comfile, mode = 'r').readlines())
tras = ' '.join(open(trafile, mode = 'r').readlines())
hists = ' '.join(open(histfile, mode = 'r').readlines())
corp = coms + tras + hists

corp = sub("<.*>","",corp)
corp = sub("[^a-zA-Z ]","",corp).split()
