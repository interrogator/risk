#!/usr/bin/ipython

#   Building parsed corpora for discourse analysis
#   Author: Daniel McDonald

# tool list:
# get text from file
# structure text by integer
# spelling normalisation
# parse files

def correctspelling(path, newpath):
    import enchant
    import codecs
    import os
    """Feed this function an unstructured corpus and get a version with corrected spelling"""
    subdirs = [d for d in os.listdir(path) if os.path.isdir(d)]
    for subdir in subdirs:
        txtFiles = [f for f in os.listdir(os.path.join(path,subdir)) if f.endswith(".txt")]
        print 'Doing ' + subdir + ' ...'
        for txtFile in txtFiles: 
            d = enchant.Dict("en_UK")
            try:
                f = codecs.open(os.path.join(path,subdir,txtFile), "r", "utf-8")
            except IOError:
                print "Error reading the file, right filepath?"
                return
            textdata = f.read()
            textdata = unicode(textdata, 'utf-8')
            mispelled = [] # empty list. Gonna put mispelled words in here
            words = textdata.split()
            for word in words:
                # if spell check failed and the word is also not in
                # our mis-spelled list already, then add the word
                if d.check(word) == False and word not in mispelled:
                    mispelled.append(word)
            # print mispelled
            for mspellword in mispelled:
                mspellword_withboundaries = '\b' + str(mspellword) + '\b'
                #get suggestions
                suggestions=d.suggest(mspellword)
                #make sure we actually got some
                if len(suggestions) > 0:
                    # pick the first one
                    picksuggestion=suggestions[0]
                    picksuggestion_withboundaries = '\b' + str(picksuggestion) + '\b'

                textdata = textdata.replace(mspellword_withboundaries,picksuggestion_withboundaries)
            try:
                if not os.path.exists(fraser_corpus_corrected):
                    os.makedirs(fraser_corpus_corrected)
                fo=open(os.path.join(newpath, txtFile), "w")
            except IOError:
                print "Error"
                return 
            fo.write(textdata.encode("UTF-8"))
            fo.close()
    return
