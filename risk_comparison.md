# Comparison of U.S. newspapers' longitudinal use of *risk words*

### [Daniel McDonald](mailto:mcdonaldd@unimelb.edu.au?Subject=IPython%20NYT%20risk%20project), [Jens Zinn](mailto:jzinn@unimelb.edu.au?Subject=IPython%20NYT%20risk%20project), University of Melbourne

> In this notebook, we build on a preliminary investigation of risk words in
*The New York Times*, looking at five additional mainstream U.S. newspapers. See
our [GitHub repository](https://www.github.com/interrogator/risk), [IPython
Notebook](https://github.com/interrogator/risk/blob/master/risk.ipynb), or
[project report](https://raw.githubusercontent.com/interrogator/risk/master/risk
_report.pdf) for more information. The theoretical underpinnings of our work,
for example, are outlined in detail in the report.

> This Notebook assumes its reader has basic familiarity with **Python** and
**key linguistic concepts**, such as word class, syntax, and lemma.

## Introduction: sociology, linguistics, code

Sociologists such as Ulrich Beck and Anthony Giddens have characterised late
modernity as *a risk society*, where risk plays an increasingly central role in
both institutional structures and everyday life.

Functional linguists are interested in mapping the ways in which words and
wordings come together to both construct and represent particular discourses and
ideologies. Over the past fifty years, linguists working within functional
traditions have mapped out in detail how language is employed by its users as a
resource for negotiating interpersonal relationships and for representing doings
and happenings in the world, or in consciousness.

Assuming that an increasing salience of *risk* in society will at least partly
be reflected in the ways in which risk is discussed, it should therefore be
possible to use real-world communication about risk to empirically examine
sociological claims.

A number of technological developments make it possible to investigate risk
semantics on a large scale:

1. Large, well-organised digital collections of news articles
2. Tools for annotating digital text with linguistic information, such as word
classes and grammatical structure
3. Programming languages, libraries and modules that can extract useful
information from these annotations

That said, the use of corpus linguistics for discourse analysis is a relatively
recent development, with available tools and methods still somewhat behind the
state of the art resources available in computaional linguistics, natural
language processing, etc.

Accordingly, we use [*corpkit*](https://www.github.com/interrogator/corpkit), a
purpose-built Python module for interrogating parsed corpora. The tool is also
available as a graphical application, documented and downloadable
[here](http://interrogator.github.io/corpkit/). Though our investigation could
be performed using the graphical interface, we have instead opted for the
command-line tools, which offer more flexibility, especially when working with
multiple corpora simultaneously.

## Aim of the investigation

Our main interest was in determining **whether findings from our investigation
of the NYT could be generalised to other major U.S. newspapers.**

This investigation makes it possible to describe, and hopefully explain, how
risk words have behaved longitudinally in mainstream U.S. newspapers. Later work
will connect these findings more explicitly to sociological claims.

## Data

Based on readership, location and digital availability, we selected the
following six newspapers.

    1. The New York Times
    2. The Wall Street Journal
    3. The Tampa Bay Times
    4. USA Today
    5. Chicago Tribune
    6. The Washington Post

## Corpus building

To do this, we used ProQuest to grab any articles in these newspapers from
1987-2015 that contained a risk word (defined by regular expression as
`(?i)\brisk` ). This left us with over 500,000 articles!

Paragraphs with risk words were extracted and parsed using *Stanford CoreNLP*.
Given the computationally intensive nature of parsing, we relied on high-
performance computing resources from the University of Melbourne to run an
*embarrassingly parallel* parsing script.

After a lot of parsing, we were left with six folders (one for each newspaper).
Each folder contained annual subcorpora for 1987--2014. In these folders were
XML files containing CoreNLP output annotation for each paragraph containing a
risk word.

## Analytical approach

Once we had the data annotated, the challenges were to:

1. Search the data to find meaningful information about the way risk words
behave
2. Turn raw findings into useful visualisations, descriptions and explanations

Computationally, we used *corpkit* to search the constituency and dependency
parses for lexicogrammatical and discourse-semantic sites of change.
Theoretically, we used concepts from *systemic functional linguistics*, which
articulates the ways in which levels of linguistic abstraction are related, and
the ways in which different kinds of meaning are realised in grammar and
wording.

## Key limitations

There are a number of fairly serious limitations that should be acknowledged
upfront.

First, we are looking only at mainstream U.S. newspaper articles. Our findings
do not reflect society generally, in the USA or otherwise: risk words likely
behave very differently in different text types.

Computationally, we must acknowledge that parser accuracy may be an issue.
Luckily, we're working with a kind of data that generally parses well, given
that default parser models are in fact trained on U.S. news journalism.

In terms of linguistic theory, relevant concepts from systemic functional
linguistics cannot be operationalised fully, given differences between the
systemic-functional grammar and the grammars with which texts were annotated.

Finally, **we're not really investigating the concept of risk, but only risk
words**. Risk as a concept can be construed without the word being present
(*"They had to decide which was safer ... "*). We chose to focus only on risk
words because there is less room for ambiguity about whether or not a risk is
being construed, and to reduce our dataset to a manageable size. The current
dataset, including parses of only paragraphs containing a risk word, is over 44
gigabytes. To parse all text from six newspapers over a 30 year period would
perhaps be the largest amount of data ever parsed for a single academic project,
requiring massive amounts of time and dedicated computational resources.

## Getting started

First, we need to import the corpkit module, as well as *pandas*, which can help
us manipulate results:

```python
# show plots in this notebook
%matplotlib inline

# import corpkit
from corpkit import Corpora

# some wordlists we'll use later
from dictionaries.process_types import processes
from dictionaries.wordlists import wordlists
from dictionaries.roles import roles

# for editing/combining results:
import pandas as pd
```

We'll also need to set paths to our corpora:

```python
from os.path import join, isdir
all_corpora = Corpora([join('data', d) for d in os.listdir('data')]\
                       if isdir(join('data, d')))
```

If you already have data saved, you might want to load it all into memory now.
This saves a lot of time, as running some queries over the entire corpus can
take hours.

```python
from corpkit.other import load_result
allwords = load_result('6_allwords_newest')
riskwords = load_result('6_riskwords_newest')
riskclasses = load_result('6_riskclasses_newest')
risktags = load_result('6_risktags_newest')
govrole = load_result('6_gr_collapsed_newest')
funct = load_result('6_fnct_newest')
riskers = load_result('6_noun_riskers_newest')
noun_lemmata = load_result('6_noun_lemmata_newest')
noun_riskers = load_result('6_noun_riskers_newest')
atrisk = load_result('6_atrisk_newest')
risky = load_result('6_risky_newest')

# another way to do this creates a dictionary, but we want to 
# avoid nested dictionaries so that things are eaier
# to read:

#from corpkit import load_all_results
#r = load_all_results()
```

```python
print allwords.results.sum().sum()
print sum([riskwords[i].totals.sum() for i in riskwords.keys()])
```

And finally, let's set our very simple regular expression for *risk words*:

```python
# case insensitive matching a word boundary, followed by 'risk', then anything
# this allows at-risk, but disallows asterisk
riskword = r'(?i)\brisk'
```

Ready? OK, let's interrogate.

## Basic training

*corpkit* is essentially comprised of a few classes, subclasses, methods, functions and wordlists. The main class is `Corpus()`, which provides access to parsing, interrogating and concordancing. A list of corpora, or paths to corpora, can be turned into a `Corpora()` object.

### Instantiate a corpus

```python
corpus = Corpus('data/NYT-parsed')
corpus
```

### Instantiate multiple corpora

```python
corpora = Corpora(['data/NYT-parsed', 'data/TBT-parsed'])
corpora
```

### Interrogate a corpus

```python
result = corpus.interrogate(searchtype, query, **optional_args)
result
```

### Interrogate corpora

```python
result = corpora.interrogate(searchtype, query, **optional_args)
result
```

### Interrogate a subcorpus or corpus file

```python
result = corpus.subcorpora[0].interrogate(searchtype, query, **optional_args)
result = corpus.files[0].interrogate(searchtype, query, **optional_args)
result
```

### Concordance

```python
conclines = corpus.concordance(searchtype, query, **optional_args)
conclines
```

### Edit interrogation results

```python
ed = result.edit(operation, denominator, **optional_args)`
ed
```


### Visualise results

```python
ed.plot(title, **_optional_args)
ed.results.plot(title, **_optional_args)
ed.totals.plot(title, **_optional_args)

### Wordlists

The wordlists can be accessed like this:

```python
print processes.relational
```

```python
print wordlists.determiners
```

```python
print roles.process
```

Wordlists can be used as queries, or as criteria to match during editing.

## Getting started

So, the first thing we'll need to do is get some basic stuff:

1. The number of words in each corpus
2. The number of risk words in each corpus
3. The part of speech tags for risk words in each corpus
4. The word class of risk words

The basic syntax for using the `interrogate()` method is to provide:

1. a *search* `dict`, containing things to be searched as keys, and queries as values
2. an *exclude* `dict`, which uses the same syntax to exclude unwanted matches
3. A *show* list, listing what should be returned from the interrogation
4. Optional arguments, for saving results, limiting search to speakers, etc.

When `interrogate()` gets a single string as its first argument, it treats the
string as a path to a corpus, and outputs an object with `query`, `results` and
`totals` attributes. When it receives a list of strings, it understands that
there are multiple corpora to search. Using parallel processing, it searches
each one, and returns a `dict` object with paths as keys and named tuple objects
as values.

Note that our risk regular expression needs to be inside `"/ /"` boundaries,
because here we're using
[Tregex](http://nlp.stanford.edu/manning/courses/ling289/Tregex.html) syntax.


```python
# returns a named tuple with results, totals and query:
allwords = all_corpora.interrogate('count', 'any', quicksave = '6_allwords')

# returns a dict with paths as keys and named tuples as values:
riskwords = all_corpora.interrogate('words', '/%s/' % riskword, quicksave = '6_riskwords')
risktags = all_corpora.interrogate('pos', '__ < /%s/' % riskword, quicksave = '6_risktags')

# the lemmatise option turns words to their stem 
# form, but turns pos tags to their major word class
riskclasses = all_corpora.interrogate('pos', '__ < /%s/' % riskword, 
                        lemmatise = True, quicksave = '6_riskclasses')
```

We can now set some data display options, and then view an example result:

```python
pd.options.display.max_rows = 30
pd.options.display.max_columns = 6
allwords.results
```

It's then quite easy to visualise this data:

```python
allwords.plot('Word counts in each corpus')
```

So, the word counts vary between papers, and across time. It's important that we
always remember to deal with that issue. One way to do this is to make these
into relative frequencies:

```python
rel = allwords.edit('%', allwords.totals)
# equivalent in this case:
# rel = allwords.edit('%', 'self')
```

```python
rel.results
```

Then, we can plot again:

```python
rel.plot('Relative word counts in the subcorpora')
```

```python
# or, we could view this data cumulatively!
allwords.plot('Cumulative number of words in the corpus',
        cumulative = True, figsize = (5,3))
print 'Total: %s words!' % "{:,}".format(allwords.totals.sum())
```

So, we have a fairly consistently sized dataset, with one major notable caveat:
we have little data from USA Today until 1993. That's worth bearing in mind.
Generally, we'll use relative frequencies, instead of absolute frequencies, in
order to normalise our counts a little better.

`allwords`, was simply counting tokens. As such, it could return a single
dataframe as output. The other searches return dictionaries, with corpus names
as keys and results as values:

```python
print type(riskwords)
print type(riskwords['UST'])
print type(riskwords['UST'].results)
riskwords['UST'].results
```

Each dictionary entry also has a totals count:

```python
riskwords['WSJ'].totals
```

If we want to visualise these totals, we can make a simply helper function to
concatenate totals:

```python
def get_totals(interrogation):
    """helper function: get totals from dict of interrogations"""
    lst = []
    # for each interrogation name and data
    for k, v in interrogation.items():
        # get the totals
        tot = v.totals
        # name the totals with the newspaper
        tot.name = k.upper()
        # add to a list
        lst.append(tot)
    # turn the list into a dataframe
    return pd.concat(lst, axis = 1)
```

```python
rwt = get_totals(riskwords)
rwt
```

We might now like to determine the percentage of all words that are risk words
in each newspaper:


```python
# get risk words in each year in each newspaper as a percentage of
# all words in that same year and newspaper
rel = rwt.edit('%', allwords.results)
rel.plot('Relative frequency of risk words by publication')
```

Because we extracted paragraphs containing risk words, we can have little to say
about whether these dips reflect changes in the relative frequency of risk
language, or some other feature, such as paragraph size.

## Part-of-speech tags

A good starting point is to find out whether there is any change in the most
common part-of-speech (POS) tags for risk words.

```python
risktags['CHT'].results[:5]
```

It might be nice to look generally at all the data, without worrying about
individual newspapers. We can write another function to collapse the distinction
between each corpus:

```python
def collapsed(interrogation):
    import pandas as pd
    order = list(interrogation.values()[0].results.columns)
    df = interrogation.values()[0].results
    for i in interrogation.values()[1:]:
        df = df.add(i.results, fill_value = 0)
    return df[order]
```

```python
# collapse newspapers
tags = collapsed(risktags)
# relativise
rel_tags = tags.edit('%', 'self')
# separate plots for each data point
rel_tags.plot('Most common POS tags for risk words', subplots = True, 
               num_to_plot = 8, figsize = (7, 7), layout = (4, 2))
```

There are some mixed signals here. Risk as an adjective seems to decrease, while
risk as a comparative adjective increases.

## Word classes

Next, we can try collapsing the distinction between kinds of nouns, adjectives,
adverbs and verbs.

```python
classes = collapsed(riskclasses)
rel_classes = classes.edit('%', 'self', print_info = False)
rel_classes.plot('Most common word classes of risk words',
          kind = 'area', figsize = (6,7), colours = 'copper')
rel_classes.plot('Most common word classes of risk words',
        subplots = True, num_to_plot = 4, figsize = (6, 3), layout = (2, 2))
```

The clearest trends are toward nominalisation and away from verbal *risk*. Let's
look at how they behave longitudinally in each publication:

```python
for cls in ['Noun', 'Verb']:
    print 'Relative frequency of %ss:' %cls.lower()
    in_each = entry_across_corpora(riskclasses, cls)
    rel = in_each.edit('%', get_totals(riskwords), print_info = False)
    rel.plot('Relative frequency of %ss' %cls, subplots = True, layout = (2,3), figsize = (8,4))
```

So, we can see that these that trends in risk word behaviour are often
generalisable across publications. This is a good start.

The limitation of this kind of approach, however, is that word classes and POS
tags are *formal features*. Though they correlate with semantics (as nouns are
likely to be *things*, and verbs are more likely to be *events*), it is a fairly
loose correlation: *to run a risk* features a nominal risk, but semantically, it
is not really a thing.

## Using dependencies

We can also look at risk words by dependency role. Dependency roles are closer
to functional than formal labels. Below, we get the dependency function of every
risk word.

```python
funct = all_corpora.interrogate({'w': riskword}, show = ['f'], quicksave = '6_riskfunct')
```

### Finding functions undergoing trajectory shift

We can use `funct`, alongside linear regress models, to determine which
functions of risk words according to dependency grammar are undergoing
longitudinal shifts in relative frequency.

```python
coll_funct = collapsed(funct)
inc = coll_funct.edit('%', 'self', sort_by = 'increase', keep_top = 10, 
             keep_stats = True, remove_above_p = True, print_info = False)
#dec = coll_funct.edit('%', 'self', sort_by = 'decrease', keep_top = 10, 
             #keep_stats = True, remove_above_p = True, print_info = False)
```

```python
inc.results
```

Interestingly, there are only two functions in which risk is increasingly
common: `dobj` (direct object) and `amod` (adjectival modifier). Looking to the
right-hand columns, we can see those results decreasing most in frequency. These
display a striking patten: the top four results are each examples of risk as a
process/predicator in either a main or embedded clause. This confirms to the
results from our pilot study, where risk in the NYT was seen to shift out of
predicatorial roles.

```python
inc.results[[0,1,-4,-3,-2,-1]].plot('Functions of risk words undergoing longitudinal shifts', tex = True, 
        num_to_plot = 6, subplots = True, figsize = (7,5), layout = (3,2), show_p_val = True, save = True)
```

Next, let's try grouping these into systemic-functional categories. We can
access wordlists corresponding to systemic categories as follows:

```python
print roles._asdict().keys()
```

The code below converts the functions to systemic labels using `edit()`.
`edit()` can receive either a results attribute as its main input, or a `dict`
object outputted by `interrogate()`. In the case of the latter, it outputs
another `dict` object.

```python
merges = {'Participant': roles.participant,
          'Process': roles.process,
          'Modifier': roles.circumstance + roles.epithet + roles.classifier}

sysfunc = funct.edit(merge_entries = merges, just_entries = merges.keys())
```

We can then plot a single newspaper by absolute or relative frequencies:

```python
sysfunc['WSJ'].plot('Systemic role of risk words in the WSJ')
rel_sysfunc = sysfunc.edit('%', 'self', print_info = False)
rel_sysfunc['WSJ'].plot('Systemic role of risk words in the WSJ')
```

Or, we can look at the behaviour of a given role in every paper. To do this,
let's write a simple function that extracts an entry from each result and
concatenates the output:

```python
def entry_across_corpora(result_dict, entry_name, regex = False):
    """
    get one entry from each newspaper and make a new dataframe
    regex allows us to search by regular expression if need be
    """
    import pandas as pd
    import re
    res = []
    # for each corpus name and data
    for k, v in sorted(result_dict.items()):
        # grab the process result for each paper
        if not regex:
            try:
                column = v.results[entry_name]
            except:
                continue
        else:
            column = v.results[[c for c in list(v.results.columns) if re.search(entry_name, c)]].iloc[:,0]
        # rename it to the corpus name
        column.name = k
        # append to a list
        res.append(column)
    # concatenate and return
    return pd.concat(res, axis = 1)
```

```python
proc = entry_across_corpora(sysfunc, 'Process')
proc
```

```python
rel_proc = proc.edit('%', riskwords)
rel_proc.plot('Frequency of risk processes by newspaper', legend = 'or')
```

Well, that's rather hard to make sense of. A problem with this kind of analysis
of risk as process, however, is that it misses risk processes where risk is a
noun, not a verb:

    1. They took a risk
    2. They ran a risk
    3. It posed a risk
    4. They put it at risk

One of our search options, 'governor', can distinguish between these accurately.
The query below shows us the function of risk words, and the lemma form of their
governor.

```python
govrole = all_corpora.interrogate({'g': riskword}, show = ['l'], 
                       dep_type = 'collapsed-ccprocessed-dependencies', quicksave = '6_govrole')
```

We can now fix up our earlier count of risk by functional role. It's tricky, but
shows the power of `edit()` and `pandas`:

```python
# make a copy, to be safe
from copy import deepcopy
syscopy = deepcopy(sysfunc)

# for each corpus
for k, v in syscopy.items():
    # calculate number to add to process count
    are_proc = ['dobj:run', 'dobj:take', 'dobj:pose', 'nmod:at:put', 'prep_at:put']
    add_to_proc = govrole[k].results[[i for i in are_proc if i in govrole[k].results.columns]].sum(axis = 1)
    # calculate number to subtract from participant count
    subtract_from_part = govrole[k].results[['dobj:run', 'dobj:take', 'dobj:pose']].sum(axis = 1)
    # calculate number to subtract from modifier count
    submod = ['prep_at:put', 'nmod:at:put']
    subtract_from_mod = govrole[k].results[[i for i in submod if i in govrole[k].results.columns]].sum(axis = 1)
    # do these calculations
    v.results['Process'] = v.results['Process'] + add_to_proc
    v.results['Participant'] = v.results['Participant'] - subtract_from_part
    v.results['Modifier'] = v.results['Modifier'] - subtract_from_mod
```

```python
print 'Uncorrected:'
print sysfunc['NYT'].results
print 'Corrected:'
print syscopy['NYT'].results
```

Let's look at the frequencies of each of these risk processes:

Now, let's plot more accurately, by role, and then by paper:

```python
for role in ['Participant', 'Process', 'Modifier']:
    df = entry_across_corpora(syscopy, role)
    edi = df.edit('%', get_totals(riskwords), print_info = False)
    edi.plot('Frequency of risk as %s by newspaper' % role)
```

```python
for name, data in syscopy.items():
    rel_data = data.edit('%', 'self', print_info = False)
    rel_data.plot('Functional roles of risk words in the %s' % name, figsize = (5, 4))
```

```python
collapsed(syscopy)
```

```python
tot = get_totals(riskwords)
for entry in ['Participant', 'Process', 'Modifier']:
    en = entry_across_corpora(syscopy, entry)
    rel_en = en.edit('%', tot, print_info = False)
    print entry
    rel_en.plotter('X', subplots = True, figsize = (6,4), layout = (2,3))
```

We can see that basic trends observed in the NYT, away from risk processes and
toward risk participants and modifiers, hold true to some extent amongst other
mainstream U.S. publications. This is especially so in the case of risk-as-
modifiers, which are increasingly common in every publication sampled.

That said, the trends are not always as clear cut in other newspapers as they
are in the NYT.

## Risk processes

The next thing we can do with our `govrole` interrogation is to plot the
frequencies of the five identified risk processes. To do this, we can rename the
combination of role and governor to something more readable, and then remove all
other entries:

```python
renames = {'to risk': 'root:root',
           'to run risk':'dobj:run',
           'to take risk': 'dobj:take',
           'to pose risk': 'dobj:pose',
           'to put at risk': 'nmod:at:put'}

# nyt was parsed with a slightly different grammar. 
# this standardises 'put at risk'
govrole['NYT'].results.rename(columns={'prep_at:put': 'nmod:at:put'}, inplace=True)

risk_processes = govrole.edit(replace_names = renames, 
                               just_entries = renames.keys(), sort_by = 'total')
```

Let's take a look at what we have:

```python
print risk_processes['WAP'].results
```

Displaying all this information properly is tricky. First, we can try collapsing
distinctions between subcorpora---though this means that we can't observe
longitudinal change:

```python
out = []
for k, v in risk_processes.items():
    data = v.results.sum(axis = 0)
    data.name = k
    out.append(data)
collapsed_years = pd.concat(out, axis = 1)
print collapsed_years
```

```python
collapsed_years.plot('Risk processes: absolute frequency', kind = 'bar', rot = False, 
        x_label = 'Publication', figsize = (8, 5))
rel_proc = collapsed_years.edit('%', 'self', print_info = False)
rel_proc.plot('Risk processes: relative frequency',
                                kind = 'bar', rot = False, x_label = 'Publication', figsize = (8, 5))
```

Or, we can collapse the distinction between newspapers. Perhaps we could make
another function for this:

```python
def collapsed(interrogation):
    import pandas as pd
    order = list(interrogation.values()[0].results.columns)
    df = interrogation.values()[0].results
    for i in interrogation.values()[1:]:
        df = df.add(i.results, fill_value = 0)
    df = df[order]
    return df
```

```python
print collapsed(risk_processes)
ed = collapsed(risk_processes).edit('%', allwords.totals, print_info = False)
ed.plot('Longitudinal behaviour of risk processes in U.S. print media', 
        figsize = (8, 5), style = 'seaborn-talk', save = True, legend_pos = 'outside right')
```

We can see whether this pattern is similar for each newspaper:

```python
for name, data in govrole.items():
    res = govrole[name].edit('%', syscopy[name].results['Process'], sort_by = 'name',
                       replace_names = renames, just_entries = renames.keys(), print_info = False)
    res.plot('Risk processes in %s' % name, figsize = (6,4), 
              legend_pos = 'outside right')
```

Let's look a little closer, and see whether the trend toward `to put at risk`
and away from `to run risk` is reflected in every publication:

```python
lst = []
renames = {#'to risk': 'root:root',
           'to run risk':'dobj:run',
           #'to take risk': 'dobj:take',
           #'to pose risk': 'dobj:pose',
           'to put at risk': r'(nmod:at:put|prep_at:put)'}
for n, i in renames.items():
    ent = entry_across_corpora(govrole, i, regex = True)
    rel_ent = ent.edit('%', entry_across_corpora(syscopy, 'Process'), print_info = False)
    print n
    rel_end.plot(n, subplots = True, layout = (2, 3), figsize = (6, 5), save = True)
```

Indeed, some patterns seem quite regular. *Running risk* decreases in every
publication, and *put at risk* increases.

### Risk as classifier/pre-head modifier

We also found growth in the use of risk as a nominal pre-head modifier (*risk
factor*, *risk brokerage*, etc.). We can use the same interrogation to find out
what risk modifies in this way:

```python
# this is a bit of a hack: delete nnmod: from names, then remove 
# any entry with a ':' in it
nom_mod = govrole.edit('%', riskwords, replace_names = r'^(nn|compound):', 
                 skip_entries = r':', use_df2_totals = True)
```

```python
inc_class = collapsed(nom_mod).edit(sort_by = 'increase', keep_stats = True, print_info = False)
dec_class = collapsed(nom_mod).edit(sort_by = 'decrease', keep_stats = True, print_info = False)
collapsed(nom_mod).plot('Risk as classifier')
inc_class.plot('Risk as classifier, increasing', show_p_val = True)
dec_class.plot('Risk as classifier, decreasing', show_p_val = True)
```

`Risk group` drops from extremely high prevalence due to its use during the
beginning of the HIV/AIDS epidemic:

```python
treg = r'NP << /(?i)\brisk/ <<# /(?i)group/'
lines = corpora['WAP'].subcorpora.c1987.concordance({'t': treg}, print_output = False)
lines.format(columns = ['l', 'm', 'r'])
```

```python
for k, v in nom_mod.items():
    v.plot('Nouns modified by risk as classifier (%s)' % k, figsize = (7, 4), legend_pos = 'outside right')
```

```python
entry_across_corpora(nom_mod, 'appetite').plot('\emph{Risk appetite}', legend_pos = 'upper left')
```

```python
treg = r'NP < (/NN.?/ < /(?i)\brisk/) < (/NN.?/ < /(?i)\bappetit/)
lines = corpora['WSJ'].subcorpora.c2009.concordance({'t': treg}, print_output=False)
lines.format(columns = ['l', 'm', 'r'])
```

Risk appetite is a good example of the increasing number of ways in which `risk`
is employed in the financial sector.

Still focussing on risk as a classifier, we can find out which words are
increasing and decreasing the most over time:

```python
nom_mod_inc = govrole.edit(replace_names = r'(nn|compound):', skip_entries = ':', 
                     sort_by = 'increase', print_info = False)
nom_mod_dec = govrole.edit(replace_names = r'(nn|compound):', skip_entries = ':', 
                     sort_by = 'decrease', print_info = False)
```

```python
nom_mod_inc['TBT'].results
```

```python
collapsed(nom_mod_inc).plot('Nouns modified by \emph{risk} as classifier, increasing', 
             legend_pos = 'upper left', figsize = (9, 5), y_label = 'Absolute frequency')
```

## Adjectival risks

One thing we noticed in our pilot investigation of the NYT was that while some
adjectival risk words are declining in frequency (*risky* is a good example),
others, like *at-risk* are becoming more prominent. We can check the other
newspapers to see if the trend is general:

### Risky, riskier, riskiest

Here, we want to find the percentage of risk-as-modifiers that are
risky/riskier/riskier. We can start by conflating the six newspapers.

```python
adjr = r'/(?i)\brisk(y|ier|iest)/'
risky = all_corpora.interrogate({'t': adjr}, show = ['c'], quicksave = '6_risky')
```

```python
# the overall frequency of risk as modifier
mod = entry_across_corpora(sysfunc, 'Modifier')
mod.sum(axis = 1)
```

```python
#print risky.results.sum(axis = 1)
#rwt = get_totals(riskwords)
#print rwt
rel_risky_sum = risky.results.sum(axis = 1).edit('%', mod.sum(axis = 1))
rel_risky_sum.results
```

```python
rel_risky.plot('Risky/riskier/riskiest')
```

Like we found in the NYT, there is an overall decrease. Let's take a look at the
individual newspapers:

```python
res = []
for paper in list(risky.results.columns):
    ed = risky.results[paper].edit('%', mod[paper], print_info = False)
    res.append(ed.results)

concatted = pd.concat(res, axis = 1)
concatted.plot('Relative frequency of risky/riskier/riskiest')
```

We can see that the trend is not as clear in other papers as it is in the NYT.

### at-risk

We also saw growth in the use of the at-risk modifier. We can check this too:

```python
atrisk = all_corpora.interrogate('count', r'/(?i)\bat-risk/', quicksave = '6_atrisk')
```

```python
atrisk.results
```

```python
rel_atrisk_sum = collapsed(syscopy)['Modifier'].edit(atrisk.results, '%')
rel_atrisk_sum.plot('Relative frequency of \emph{at-risk} modifier')
```

Now, let's split the corpora again:

```python
rel_atrisk_sum.plot('Relative frequency of \emph{at-risk}', subplots = True, 
                    figsize = (10, 5), layout = (2,3))
```

Interesting that both the peaks before 9/11 and the general rise are observable
in most papers.

## Mood role of risk words

In our last investigation, we found that risk is increasingly occurring within
complements and adjuncts, and less often within subject and finite/predicator
positions. This was taken as evidence for decreasing arguability of risk in news
discourse.

We can attempt to replicate that result using a previous interrogation.

```python
print roles
```

```python
# we collapse the finite/predicator distinction because it's not very
# well handled by dependency parses. this is a pity, since finite plays
# a more important role in arguability than predicator.

merges = {'Subject': roles.subject,
          'Finite/Predicator': roles.predicator,
          'Complement': roles.complement,
          'Adjunct': roles.adjunct}

moodrole = funct.edit(merge_entries = merges, just_entries = merges.keys())
```

```python
rel_role = collapsed(moodrole).edit('%', 'self', print_info = False)
#rel_role.plot('Mood role of risk words')
rel_role.plot('Mood role of risk words', subplots = True, 
              layout = (2,2), figsize = (7, 5), save = 'moodrole-6')
```

This finding aligns with our pilot study, showing that risk is shifting from
more arguable to less arguable positions within clauses.

## Risk and power

The last thing we'll look at (for now) is the relationship beween risking and
power.

In our previous analysis, we found that powerful people are much more likely to
do risking.

To determine this, we needed to make two search queries. The first finds the
nominal heads when risk/run risk/take risk is the process:


```python
query = r'/NN.?/ !< /(?i).?\brisk.?/ >># (@NP $ (VP <+(VP) (VP ( <<# (/VB.?/ < /(?i).?\brisk.?/) | <<# (/VB.?/ < /(?i)(take|taking|takes|taken|took|run|running|runs|ran)/) < (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))))'
noun_riskers = all_corpora.interrogate({'t': query}, show = 'l', quicksave = '6_noun_riskers', num_proc = 3)
```

Next, we need to get the frequencies of nouns generally, so that we can account
for the fact that some nouns are very common.

```python
query = r'/NN.?/ >># NP !< /(?i).?\brisk.?/'
noun_lemmata = all_corpora.interrogate({'t': query}, show = 'l', quicksave = '6_noun_lemmata')
```

Now, we can combine the lists:

```python
# entities of interest
people = ['man', 'woman', 'child', 'baby', 'politician', 
          'senator', 'obama', 'clinton', 'bush']

# make summed versions of the noun_lemmata data
summed_n_lemmata = {}
for name, data in noun_lemmata.items():
    summed_n_lemmata[name] = data.results.sum(axis = 0)

# calculate percentage of the time word is in 
# risker position for each paper

# newpaper names
cols = []
# the results go here
res = []
# for each newspaper
for name, data in noun_riskers.items():
    # collapse years
    data = data.results.sum(axis = 0)
    # make a new column
    ser = {}
    # for each risker
    for i in list(data.index):
        # if not a hapax
        if summed_n_lemmata[name][i] < 2:
            continue
        # get its percentage
        try:
            sm = data[i] * 100.0 / summed_n_lemmata[name][i]
        except:
            continue
        # add this to the data for this paper
        ser[i] = sm
    
    # turn the data into a column
    as_series = pd.Series(ser)
    # sort it
    as_series.sort(ascending = False)
    # add it to a master list
    res.append(as_series)
    # add the newspaper name
    cols.append(name)
    
# put data together into spreadsheet
df = pd.concat(res, axis = 1)
# name newspapers again
df.columns = cols
# just named entries
df_sel = df.T[people].T
# show us what it looks like
print df_sel
# sort by frequency
sort_by = list(df_sel.sum(axis = 1).sort(ascending = False, inplace = False).index)
df_sel = df_sel.T[sort_by].T
```

```python
df_sel.plot(kind = 'bar', title = '')
```

```python
# visualise
df_sel.plot('Risk and power', kind = 'bar', figsize = (8, 5),
            x_label = 'Entity', y_label = 'Risker percentage', style = 'seaborn-talk', save = 'rp6')
df_sel.T.plot('Risk and power', kind = 'bar', figsize = (8, 5), num_to_plot = 'all',
           x_label = 'Publication', y_label = 'Risker percentage')
```

We can see here that each paper construes powerful people as riskers. Also
interesting is that entities favoured by the political orientation of the
newspapers are more often positioned as riskers.

Finally, we can look longitudinally, to see if there are more or fewer riskers
in general:

```python
lemmata_tots = {}
for name, data in noun_lemmata.items():
    lemmata_tots[name] = data.totals
output = []
for name, data in noun_riskers.items():
    tot = data.totals
    tot = tot * 100.0 / lemmata_tots[name]
    tot.name = name
    output.append(tot)
df = pd.concat(output, axis = 1)
df.plot('Percentage of noun lemmata in the risker position', style = 'seaborn-talk', save = True)
df.plot('Percentage of noun lemmata in the risker position', kind = 'area', reverse_legend = False)
```

So, interestingly, there are fewer and fewer grammatical riskers in mainstream
U.S. print news.

## Discussion

* A key issue we faced was turning a mind-boggling amount of data into something
more reasonable.
* Typically, the most telling visualisations are those that conflate corpora,
conflate sampling periods, or limit findings to a single linguistic feature at a
time.
* Being able to programmatically work with data is a huge plus, especially when
it has a complex structure

## Next steps

* Computationally, an interesting next step would be to develop algorithms that
rank the importance of various features, in order to condense complex,
multidimensional findings into 'scores' for concepts such as implicitness,
density, arguability, and the like.
* Sociologically, qualitative analysis of risk words in their immediate co-text
and context would also prove valuable.

