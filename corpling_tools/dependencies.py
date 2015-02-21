#!/usr/local/bin/ipython

#   Interrogating parsed corpora and plotting the results: dependencies
#   for ResBaz NLTK stream
#   Author: Daniel McDonald

def dependencies(path, options, query, lemmatise = False, test = False, 
    titlefilter = False, lemmatag = False, deps = False):
    """Uses Tregex to make list of frequency counts in corpora.
    
    Interrogator investigates sets of Stanford dependencies for complex frequency information. 

    path: path to corpus as string
    options:
    query: regex to match
    Lemmatise: lemmatise results
    test: for development, go through only three subcorpora
    titlefilter: strip 'mr, mrs, dr' etc from proper noun strings

    Note: subcorpora directory names must be numbers only.
    """
    import os
    from bs4 import BeautifulSoup, SoupStrainer
    import collections
    import time
    from time import localtime, strftime
    import re
    import sys
    import string
    import codecs
    from string import digits
    import operator
    import glob
    # define option regexes
    if lemmatise:
        import nltk
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr=WordNetLemmatizer() # initialise lemmatiser only once, for speed
    time = strftime("%H:%M:%S", localtime())

    # welcome message based on kind of interrogation
    # this could probably be made simpler...
    if options == 'depnum':
        print time + ": Beginning corpus interrogation: " + path + "\n          Query: " + str(query) + ". \n           Number only.\n"
    elif options == 'rship':
         print time + ": Beginning corpus interrogation: " + path + "\n          Query: " + str(query) + ". \n          Role only.\n"
    elif options == 'govrole':
        print time + ": Beginning corpus interrogation: " + path + "\n          Query: " + str(query) + ". \n          Role and governor.\n"
    # make this into a function
    # get POS from Tregex query
    # TO DO: add a feature where if tag and terminal option is selected, lemmatiser gets the tag from the tag portion...
    if lemmatise is True:
        if lemmatag is False:
            # attempt to find tag from tregex query
            # currently this will fail with a query like r'/\bthis/'
            tagfinder = re.compile(r'^[^A-Za-z]*([A-Za-z]*)') 
            tagchecker = re.compile(r'^[A-Z]{2,4}$')
            tagfinder = re.compile(r'^[^A-Za-z]*([A-Za-z]*)')
            treebank_tag = re.findall(tagfinder, query)
            if re.match(tagchecker, treebank_tag[0]):
                if treebank_tag[0].startswith('J'):
                    tag = 'a'
                elif treebank_tag[0].startswith('V'):
                    tag = 'v'
                elif treebank_tag[0].startswith('N'):
                    tag = 'n'
                elif treebank_tag[0].startswith('R'):
                    tag = 'r'
            else:
                tag = 'n' # default to noun tag---same as lemmatiser does with no tag
        if lemmatag:
            tag = lemmatag
            tagchecker = re.compile(r'^[avrn]$')
            if not re.match(tagchecker, lemmatag):
                raise ValueError("WordNet POS tag not recognised. Must be 'a', 'v', 'r' or 'n'.")
    # get subdirectories in corpus folder
    sorted_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    sorted_dirs.sort(key=int)
    if test is True: # allow shorter testing
        sorted_dirs = sorted_dirs[:5]
    number_of_subcorpora = len(sorted_dirs) # move earlier
    results = []
    exclude = set(string.punctuation)
    annual_totals = [u'Totals']
    # search the corpus    


    def dep_search():
        """Searching via dependencies"""
        regex = re.compile(query)

        def govrole(soup):
            """print rship:gov"""
            result = []
            for dep_elem in soup.find_all('dependencies'):
                deptype = dep_elem.attrs.get('type')
            # get just collapsed
                if deptype == 'collapsed-ccprocessed-dependencies':
                    for dep in dep_elem.find_all('dep'):
                        for dependent in dep.find_all('dependent'):
                            word = dependent.get_text()
                            if re.match(regex, word):
                                role = dep.attrs.get('type')
                                # the below is a redundant loop
                                for gov in dep.find_all('governor'):
                                    govword = gov.get_text()
                                colsep = role + ':' + govword
                                result.append(colsep)
            return result

        def rship(soup):
            """"print functional role"""
            result = []
            for dep in soup.find_all('dep'):
                for dependent in dep.find_all('dependent'):
                    word = dependent.get_text()
                    if re.match(regex, word):
                        result.append(dep.attrs.get('type'))
            return result

        def depnum(soup):
            """print dependency number"""
            result = []
            for dep in soup.find_all('dep'):
                for dependent in dep.find_all('dependent'):
                    word = dependent.get_text()
                    if re.match(regex, word):
                        # get just the number
                        result.append(dependent.attrs.get('idx'))
            return result
        coll_dep_regex = re.compile('collapsed-ccprocessed-dependencies')
        for d in sorted_dirs:
            yearfinder = re.findall(r'[0-9]+', d)
            time = strftime("%H:%M:%S", localtime())
            print time + ": Doing " + yearfinder[0] + " ... "
            files = os.listdir(os.path.join(path, d))
            time = strftime("%H:%M:%S", localtime())
            print time + ': Concatenating ... '
            read_files = glob.glob(os.path.join(path, d, "*.xml"))
            result = []
            for f in read_files:
                with open(f, "rb") as text:
                    data = text.read()
                    just_good_deps = SoupStrainer('dependencies', type=coll_dep_regex) # was originally re.compile...
                    soup = BeautifulSoup(data, parse_only=just_good_deps)
                    if options == 'govrole':
                        result_from_file = govrole(soup)
                    if options == 'rship':
                       result_from_file = rship(soup)
                    if options == 'depnum':
                      result_from_file = depnum(soup)
                for entry in result_from_file:
                    result.append(entry)
            # back to the old interrogator now:
            # get total:
            totalcount = [int(d), len(result)]
            annual_totals.append(totalcount)
            # process results
            lowercase_result = []
            for word in result: # will have to make lemmatiser work for govrole...
                try:
                    word = unicode(word, 'utf-8')
                except TypeError:
                    raise ValueError("Some kind of encoding problem.")
                if lemmatise is True:
                    # some post-hoc fixing of tokens for lemmatiser ...
                    if word == u'\'s':
                        word = u'is'
                    if word == u'\'re':
                        word = u'are'
                    if word == u'\'m':
                        word = u'am'
                    #if word == u'\'d':
                        #word = u'is'
                    #if word == u'\'ll':
                        #word = u'is'
                    if word == u'n\'t':
                        word = u'not'
                    word = lmtzr.lemmatize(word, tag)
                word = re.sub(r"^[^A-Za-z\(\']*", "", word) # this might be too strict
                lowered = word.lower()
                if titlefilter is True:
                    lowered = re.sub(r"^(admiral|archbishop|alan|merrill|sarah|queen|king|sen|chancellor|prime minister|cardinal|bishop|father|hon|rev|reverend|pope|the|sir|doctor|professor|president|senator|congressman|congresswoman|mr|ms|mrs|miss|dr|bill|hillary|hillary rodham|saddam|osama|ayatollah|george|george w|mitt|malcolm|barack|ronald|john|john f|william|al|bob)\b\.* *", "", lowered)
                #lowered = lowered.translate(None, digits) # not a good way to go about it.
                lowercase_result.append(lowered)
            results.append(lowercase_result)
        return results

    def sort(results):
        time = strftime("%H:%M:%S", localtime())
        print time + ": Sorting results ..."
        unique_results = []
        for subcorpus in results:
            yearfinder = re.findall(r'[0-9]+', sorted_dirs[results.index(subcorpus)])
            year = yearfinder[0]
            uniques = set(sorted(results[results.index(subcorpus)]))
            unique_words = []
            for word in uniques:
                if word is not '':
                    count = subcorpus.count(word)
                    year_lemma_and_count = [year, word, count]
                #########print year_lemma_and_count
                    unique_results.append(year_lemma_and_count)
            #unique_results.append(unique_words)
        # now we've got the year, word and count from every subcorpus.
        unique_results.sort(lambda x,y: cmp(x[1],y[1]))
        return unique_results

    def table(unique_results):
        allwords = []
        tally = []
        # make a list of all words in corpus
        for item in unique_results: 
            allwords.append(item[1])
        uniquewords = set(sorted(allwords))
        count = len(uniquewords)
        # print updates on tabling process because it's slow
        time = strftime("%H:%M:%S", localtime())
        print time + ': Processing ' + str(count) + ' entries ... \r',
        c = 1
        m = 1000
        for wordlist_entry in uniquewords:
            c += 1
            if c == m:
                perc = c * 100 / count
                time = strftime("%H:%M:%S", localtime())
                print time + ': ' + str(perc) + ' per cent done ... '
                m += 1000
            lines = [line for line in unique_results if wordlist_entry == line[1]] # this is the slow part...
            counts = [wordlist_entry]
            for l in lines:
                unique_results.remove(l) # this speeds the tabling up by removing completed entries
                year_and_count = [l[0], l[2]]
                counts.append(year_and_count)
            tally.append(counts)
        sorting = []
        final = []
        tally = sorted(tally)

        # final formatting --- elaborate, but fast.

        for entry in tally:
            if entry[0] == u'': # catch and remove empty entries
                tally.remove(entry)
            #if type(entry[0]) != unicode:
                #tally.remove(entry)
            if type(entry[0]) == unicode:
                word = unicode(entry[0])
            else:
                word = False
            listofyears = []
            toadd = []
            data = []
            for part in entry[1:]: # get year, word, and count
                if type(part) == list:
                    int_year = int(part[0])
                    listofyears.append(part[0]) # get years with results
                    toadd.append(part[1])
                    int_year_and_count = [int_year, part[1]]
                    data.append(int_year_and_count)
                equals = sum(int(l) for l in toadd)
            # adding zero counts for matplotlib
            for d in sorted_dirs: # get year as string
                yearfinder = re.findall(r'[0-9]+', d)
                year = yearfinder[0] 
                if year not in listofyears: 
                    data.append([int(year), 0])
                data = sorted(data)
            if word is not False:
                total_data = [equals] + [word] + data # total, word, year and count ...
            #else:
                #print 'A word was not found  ... '
                sorting.append(total_data)
        sorting = sorted(sorting, reverse = True) # could improve with generator expr
        for entry in sorting:
            if entry[1] != u'':
                final.append(entry[1:]) # this and the line below are ways to remove total from final
            #sorting.remove(entry[0])
        time = strftime("%H:%M:%S", localtime())
        print time + ': ' + path + ' interrogation done.'
        return final


# actually do the functions

    results = dep_search()
    unique_results = sort(results)
    final = table(unique_results)
    outputnames = collections.namedtuple('interrogation', ['query', 'results', 'totals'])
    query_options = [query, options] 
    output = outputnames(query_options, final, annual_totals)
    return output
