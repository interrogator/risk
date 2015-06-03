# <markdowncell>
# Discourse-semantics of *risk* in the *New York Times*, 1963&ndash;2014
# ==========================================

# <markdowncell>
# **[Jens Zinn](mailto:jzinn@unimelb.edu.au?Subject=IPython%20NYT%20risk%20project), [Daniel McDonald](mailto:mcdonaldd@unimelb.edu.au?Subject=IPython%20NYT%20risk%20project)**
#---------------------------
# <markdowncell>
# <br>

# > **SUMMARY:** This *IPython Notebook* demonstrates the findings from our investigation of *risk* in the NYT, as well as the code used to generate these findings. If you have the necessary dependencies installed, you can also use this notebook to interrogate and visualise the corpus yourself. 

# <markdowncell>
# ### Setup

# <markdowncell>
# If you haven't already done so, the first things we need to do are **install corpkit**, download data for NLTK's tokeniser, and **unzip our corpus**.

# <codecell>
# install corpkit with either pip or easy_install
try:
    import pip
    pip.main(['install', 'corpkit'])
except ImportError:
    import easy_install
    easy_install.main(["-U","corpkit"])

# <codecell>
# download nltk tokeniser data
import nltk
nltk.download('punkt')
nltk.download('wordnet')

# <codecell>
# unzip and untar our data
! gzip -dc data/nyt.tar.gz | tar -xf - -C data

# <markdowncell>
# Great! Now we have everything we need to start.

# <markdowncell>
# ### Orientation

# <markdowncell>
#  Let's import the functions we'll be using to investigate the corpus. These functions are designed for this interrogation, but also have more general use in mind, so you can likely use them on your own corpora.

# | **Function name** | Purpose                            | |
# | ----------------- | ---------------------------------- | |
# | `interrogator()`  | interrogate parsed corpora         | |
# | `editor()`        | edit `interrogator()` results         | |
# | `plotter()`       | visualise `interrogator()` results | |
# | `quickview()`     | view `interrogator()` results      | |
# | `conc()`          | complex concordancing of subcorpora | |
# | `keywords()`          | get keywords and ngrams from `conc()` output | |
# | `collocates()`          | get collocates from `conc()` output| |
# | `quicktree()`          | visually represent a parse tree | |
# | `searchtree()`          | search a parse tree with a Tregex query | |

# <codecell>
import corpkit
import pandas as pd
from corpkit import (interrogator, editor, plotter, quickview, 
                    conc, keywords, colls, save_result, load_result)
# show figures in browser
% matplotlib inline

# <markdowncell>
# Next, let's set the path to our corpus. If you were using this interface for your own corpora, you would change this to the path to your data.

# <codecell>
# corpus of every article, with annual subcorpora
annual_trees = 'data/nyt/years' 

# <markdowncell>
# Let's also quickly set some options for displaying raw data:

# <codecell>
pd.set_option('display.max_columns', 10)
pd.set_option('max_colwidth',70)
pd.set_option('display.width', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('colheader_justify', 'left')

# <markdowncell>
# ### The report

# <markdowncell>
# The focus of this notebook is our methodology and findings. These parts of the project are contextualised and elaborated upon in our written report of the project. Depending on your browser's capabilities/settings, the following will download or display our report:

# <codecell>
# from corpkit import report_display
# report_display()

# <markdowncell>
# ### The data

# <markdowncell>

# Our main corpus is comprised of paragraphs from *New York Times* articles that contain a risk word, which we have defined by regular expression as '(?i)'.?\brisk.?\b'. This includes *low-risk*, or *risk/reward* as single tokens, but excludes *brisk* or *asterisk*.

# The data comes from a number of sources.

# * 1963 editions were downloaded from ProQuest Newsstand as PDFs. Optical character recognition and manual processing was used to create a set of 1200 risk sentences.
# * The 1987&ndash;2006 editions were taken from the *NYT Annotated Corpus*.
# * 2007&ndash;2014 editions were downloaded from *ProQuest Newsstand* as HTML.

# In total, 149,504 documents were processed. The corpus from which the risk corpus was made is over 150 million words in length!

# The texts have been parsed for part of speech and grammatical structure by [`Stanford CoreNLP*](http://nlp.stanford.edu/software/corenlp.shtml). In this Notebook, we are only working with the parsed versions of the texts. We rely on [*Tregex*](http://nlp.stanford.edu/~manning/courses/ling289/Tregex.html) to interrogate the corpora. Tregex allows very complex searching of parsed trees, in combination with [Java Regular Expressions](http://docs.oracle.com/javase/7/docs/api/java/util/regex/Pattern.html). It's definitely worthwhile to learn the Tregex syntax, but in case you're time-poor, at the end of this notebook are a series of Tregex queries that you can copy and paste into *interrogator()` and `conc()` queries.

# <markdowncell>
# ### Interrogating the corpus

# <markdowncell>
# So, let's start by finding out how many words we have in each subcorpus. To do this, we'll interrogate the corpus using `interrogator()`. Its most important arguments are:
#
# 1. **path to corpus**
#
# 2. Tregex **options**:
#   * **'t/w/words'**: return only words
#   * **'c/count'**: return a count of matches
#   * **'p/pos'**: return only the tag
#   * **'b/both'**: return tag and word together
#
# 3. a **Tregex query**

# We only need to count tokens, so we can use the `'count'` option (it's often faster than getting lists of matching tokens). The cell below will run `interrogator()` over each annual subcorpus and count the number of matches for the query.

# Some common Tregex patterns have been predefined. Searching for `'any'` will find any word in the corpus and count it.

# <codecell>
allwords = interrogator(annual_trees, 'count', 'any') 

# <markdowncell>
# When the interrogation has finished, we can view our results:

# <codecell>
# from the allwords results, print the totals
print allwords.totals

# <markdowncell>
# If you want to see the query and options that created the results, you can use:

# <codecell>
print allwords.query

# <markdowncell>
# ### Plotting results

# <markdowncell>
# Lists of years and totals are pretty dry. Luckily, we can use the `plotter()` function to visualise our results. At minimum, `plotter()` needs two arguments:

# 1. a title (in quotation marks)
# 2. a list of results to plot

# <codecell>
plotter('Word counts in each subcorpus', allwords.totals)

# <markdowncell>
# Because we have smaller samples for 1963 and 2014, we might want to project them. To do that, we can pass subcorpus names and projection values to `editor()`:

# <codecell>
proj_vals = [(1963, 5), (2014, 1.37)]
projected = editor(allwords.totals, projection = proj_vals)
plotter('Word counts in each subcorpus (projected)', projected.totals)

# <markdowncell>
# Great! So, we can see that the number of words per year varies quite a lot, even after projection. That's worth keeping in mind.

# <markdowncell>
# ### Frequency of risk words in the NYT

# <markdowncell>
# Next, let's count the total number of risk words. Notice that we are using the `'both'` flag, instead of the `'count'` flag, because we want both the word and its tag.

# <codecell>
# our query:
riskwords_query = r'__ < /(?i).?\brisk.?\b/' # any risk word and its word class/part of speech
# get all risk words and their tags :
riskwords = interrogator(annual_trees, 'both', riskwords_query)

# <markdowncell>
# Even when do not use the `count` flag, we can access the total number of matches as before:

# <codecell>
plotter('Risk words', riskwords.totals)

# <markdowncell>
# At the moment, it's hard to tell whether or not these counts are simply because our annual NYT samples are different sizes. To account for this, we can calculate the percentage of parsed words that are risk words. This means combining the two interrogations we have already performed.

# We can do this by using `editor()`:

# <codecell>
rel_riskwords = editor(riskwords.totals, '%', allwords.totals)

# <codecell>
plotter('Relative frequency of risk words', rel_riskwords.totals)

# <markdowncell>
# That's more helpful. We can now see some interesting peaks and troughs in the proportion of risk words. We can also see that 1963 contains the highest proportion of risk words. This is because the manual corrector of 1963 OCR entries preserved only the sentence containing risk words, rather than the paragraph.

# Here are two methods for excluding 1963 from the chart:

# <codecell>
# using Pandas syntax:
plotter('Relative frequency of risk words', rel_riskwords.totals.drop('1963'))

# <codecell>
rel_riskwords = editor(rel_riskwords.totals, skip_subcorpora = [1963])
plotter('Relative frequency of risk words', rel_riskwords.totals)

# <markdowncell>
# Perhaps we're interested in not only the frequency of risk words, but the frequency of different *kinds* of risk words. We actually already collected this data during our last `interrogator()` query.

# We can print just the first few entries of the results list, rather than the totals list.

# <codecell>
# using Pandas syntax:
riskwords.results.T.head(n = 10)

# <codecell>
# using quickview
from corpkit import quickview
quickview(riskwords.results)

# <markdowncell>
# We now have enough data to do some serious plotting.

# <codecell>
frac1 = editor(riskwords.results, '%', riskwords.totals)

# <codecell>
plotter('Risk word / all risk words', frac1.results, num_to_plot = 9)

# <codecell>
frac2 = editor(riskwords.results, '%', allwords.totals)

# <codecell>
plotter('Risk word / all words', frac2.results)

# <markdowncell>
# Another neat feature is the `.table` attribute of interrogations, which shows the most common `n` results in each subcorpus:

# <codecell>
riskwords.table

# <markdowncell>
# ### Customising visualisations

# <markdowncell>
# By default, `plotter()` plots the seven most frequent results, including 1963.

#  We can use other `plotter()` arguments to customise what our chart shows. `plotter()`'s possible arguments are:

#  | `plotter()` argument | Mandatory/default?       |  Use          | Type  |
#  | :------|:------- |:-------------|:-----|
#  | `title` | **mandatory**      | A title for your plot | string |
#  | `results` | **mandatory**      | the results you want to plot | `interrogator()` or `editor` output |
#  | `num_to_plot` | 7    | Number of top entries to show     |  int |
#  | `x_label` | False    | custom label for the x-axis     |  str |
#  | `y_label` | False    | custom label for the y-axis     |  str |
#  | figsize | (13, 6) | set the size of the figure | tuple: `(length, width)`|
#  | tex | `'try'` | use TeX to generate image text | boolean |
#  | style | `'ggplot'` | use Matplotlib styles | str: `'dark_background'`, `'bmh'`, `'grayscale'`, `'ggplot'`, `'fivethirtyeight'`, `'matplotlib'` |
#  | legend | `'default'` | legend position | str: `'outside right'` to move legend outside chart |

# <codecell>
plotter('Risk words', frac2.results, num_to_plot = 5, y_label = 'Percentage of all words')

# <markdowncell>
# Keyword arguments for Pandas and matplotlib can also be used:

# <codecell>
plotter('Risk words', riskwords.results, subplots = True)
plotter('Risk words', riskwords.results, kind = 'bar', stacked = True)

# <markdowncell>
# Those already proficient with Python can use [Pandas' `plot()` function](http://pandas.pydata.org/pandas-docs/stable/visualization.html) if they like

# <markdowncell>
# Another neat thing you can do is save the results of an interrogation, so they don't have to be run the next time you load this notebook:

# <codecell>
# specify what to save, and a name for the file.
from corpkit import save_result, load_result
save_result(allwords, 'allwords')

# <markdowncell>
# You can then load these results:

# <codecell>
fromfile_allwords = load_result('allwords')
fromfile_allwords.totals

# <markdowncell>
# ### `quickview()`

# <markdowncell>
# `quickview()` is a function that quickly shows the n most frequent items in a list. Its arguments are:

# 1. an `interrogator()` result
# 2. number of results to show (default = 50)

# <codecell>
from corpkit import quickview
quickview(riskwords.results, n = 25)

# <markdowncell>
# The number shown next to the item is its index. You can use this number to refer to an entry when editing results.

# ### `editor()`

# <markdowncell>
# Results lists can be edited quickly with `editor()`. It has a lot of different options.

# First, we can select specific subcorpora to keep, remove or span:

# <codecell>
editor(riskwords.results, skip_subcorpora = [1963, 1987, 1988]).results

# <codecell>
editor(riskwords.results, just_subcorpora = [1963, 1987, 1988]).results

# <codecell>
editor(riskwords.results, span_subcorpora = [2000, 2010]).results

# <markdowncell>
# We can do similar kinds of things with each *result*:

# <codecell>
quickview(riskwords.results)

# <codecell>
editor(riskwords.results, skip_entries = [2, 5, 6]).results

# <codecell>
editor(riskwords.results, just_entries = [2, 5, 6]).results

# <markdowncell>
# We can also use the words themselves, rather than indices, for all of these operations:

# <codecell>
editor(riskwords.results, just_entries = ['(nn risk-management)', '(jj risk-management)']).results

# <markdowncell>
# Or, we can use Regular Expressions:

# <codecell>
# skip any verbal risk
editor(riskwords.results, skip_entries = r'^\(v').results


# <markdowncell>
# We can also merge entries, and specify a new name for the merged items. In lieu of a name, we can pass an index. 

# <codecell>
editor(riskwords.results, merge_entries = [2, 5, 6], newname = 'New name').results

# <codecell>
editor(riskwords.results, merge_entries = ['(nns risks)', '(nns risk-takers)', '(nns risks)'], newname = 1).results

# <markdowncell>
# Notice how the merged result appears as the final column. To reorder the columns by total frequency, we can use `sort_by = 'total'`.

# <codecell>
# if we don't specify a new name, editor makes one for us
generated_name = editor(riskwords.results, merge_entries = [2, 5, 6], sort_by = 'total')
quickview(generated_name.results)

# <markdowncell>
# `editor()` can sort also sort alphabetically, or by least frequent:

# <codecell>
# alphabetically
editor(riskwords.results, sort_by = 'name').results

# <codecell>
# least frequent
editor(riskwords.results, sort_by = 'infreq').results

# <markdowncell>
# Particularly cool is sorting by 'increase' or 'decrease': this calculates the trend lines of each result, and sort by the slope.

# <codecell>
editor(riskwords.results, sort_by = 'increase').results

# <markdowncell>
# We can use `just_totals` to output just the sum of occurrences in each subcorpus:

# <codecell>
editor(riskwords.results, just_totals = True).results

# <markdowncell>
# A handy thing about working with Pandas DataFrames is that we can easily translate our results to other formats:

# <codecell>
increasing = editor(riskwords.results, sort_by = 'decrease')

# <codecell>
# tranpose with T, get just top 5 results, print as CSV
print increasing.results.T.head().to_csv()

# <codecell>
# or, print to latex markup:
print increasing.results.T.head().to_latex()

# <markdowncell>
# Of course, you can perform many of these operations at the same time. Problems may arise, however, especially if your options contradict.

# <codecell>
editor(riskwords.results, '%', riskwords.totals, span_subcorpora = [1990, 2000], just_entries = r'^\(n', merge_entries = r'(nns|nnp)', newname = 'Plural/proper').results


# <markdowncell>
# ### Diversity of risk words

# <markdowncell>
# It's important to note that the kind of results we generate are hackable. We could count the number of unique risk words in each subcorpus by changing any count over 1 to 1.

# <codecell>
import numpy as np
# copy our list
uniques = riskwords.results.copy()
# divide every result by itself
for f in uniques:
    uniques[f] = uniques[f] / uniques[f]
# get rid of inf scores (i.e. 0 / 0) using numpy
uniques = uniques.replace(np.inf, 0)
# sum the results
u = uniques.T.sum()
# give our data a name
u.name = 'Unique risk words'

# <codecell>
plotter('Unique risk words', u.drop(['1963', '2014']), y_label = 'Number of unique risk words')

# <markdowncell>
# So, we can see a generally upward trajectory, with more risk words constantly being used. Many of these results appear once, however, and many are nonwords. *Can you figure out how to remove words that appear only once per year?*

# <markdowncell>
# ### conc()

# <markdowncell>
# `conc()` produces concordances of a subcorpus based on a Tregex query. Its main arguments are:

# 1. A subcorpus to search *(remember to put it in quotation marks!)*
# 2. A Tregex query

# <codecell>
# here, we use a subcorpus of politics articles,
# rather than the total annual editions.
lines = conc('data/nyt/topics/politics/1999', r'/JJ.?/ << /(?i).?\brisk.?\b/') # adj containing a risk word

# <markdowncell>
# You can set `conc()` to print only the first ten examples with `n = 10`, or ten random these with the `n = 15, random = True` parameter.

# <codecell>
lines = conc('data/nyt/years/2007', r'/VB.?/ < /(?i).?\brisk.?\b/', n = 15, random = True)

# <markdowncell>
# `conc()` takes another argument, window, which alters the amount of co-text appearing either side of the match. The default is 50 characters

# <codecell>
lines = conc('data/nyt/topics/health/2013', r'/VB.?/ << /(?i).?\brisk.?\b/', n = 15, random = True, window = 20)

# <markdowncell>
# `conc()` also allows you to view parse trees. By default, it's false:

# <codecell>
lines = conc('data/nyt/years/2013', r'/VB.?/ < /(?i)\btrad.?/', trees = True)

# <markdowncell>
# Just like our other data, conc lines can be edited with `editor()`, or outputted as CSV.

# <codecell>
lines = editor(lines, skip_entries = [1, 2, 4, 5])
print lines

# <markdowncell>
# If the concordance lines aren't print well, you can use `concprinter()`:

# <codecell>
from corpkit import concprinter
lines = concprinter(lines)

# <markdowncell>
# Or, you can just use Pandas syntax:

# <codecell>
# Because there may be commas in the concordance lines, 
# it's better to generate a tab-separated CSV:
print lines.to_csv(sep = '\t')

# <markdowncell>
# You can also print some `TeX`, if you're that way inclined:

# <codecell>
print lines.to_latex()

# <markdowncell>
# ### Keywords, ngrams and collocates

# <markdowncell>
# `corpkit` has some functions for keywording, ngramming and collocation. Each can take a number of kinds of input data:

# 1. a path to a subcorpus (of either parse trees or raw text)
# 2. `conc()` output
# 3. a string of text

# `keywords()` produces both keywords and ngrams. It relies on code from the [Spindle](http://openspires.oucs.ox.ac.uk/spindle/) project.

# <codecell>
from corpkit import keywords
keys, ngrams = keywords(lines)
for key in keys[:10]:
    print key
for ngram in ngrams:
    print ngram

# <markdowncell>
# You can also use `interrogator()` to search for keywords or ngrams. To do this, instead of a Tregex query, pass `'keywords'` or `'ngrams'. You should also specify a dictionary to use as the reference corpus. If you specify `dictionary = 'self'`, a dictionary will be made of the entire corpus, saved, and used.

# <codecell>
all_keys_with_bnc = interrogator(annual_trees, 'words', 'keywords', dictionary = 'bnc.p')

# <codecell>
all_keys_with_self = interrogator(annual_trees, 'words', 'keywords', dictionary = 'self')

# <markdowncell>
# Now, rather than a frequency count, you will be given the keyness of each word.

# <codecell>
quickview(all_keys_with_self.results)

# <codecell>
all_keys_with_self.table

# <markdowncell>
# Similarly, you can generate collocates:

# <codecell>
colls = collocates(lines)
for coll in colls:
    print coll

# <markdowncell>
# With the `collocates()` function, you can specify the maximum distance at which two tokens will be considered collocates.

# <codecell>
colls = collocates(lines, window = 3)
for coll in colls:
    print coll

# <markdowncell>
# ### quicktree() and searchtree()

# <markdowncell>
# The two functions are useful for visualising and searching individual syntax trees. They have proven useful as a way to practice your Tregex queries.

# You could get trees by using `conc()` with a very large window and *trees* set to *True*. Alternatively, you can open files in the data directory directly, and paste them in.

# `quicktree()` generates a visual representation of a parse tree. Here's one from 1989:

# <codecell>
tree = '(ROOT (S (NP (NN Pre-conviction) (NN attachment)) (VP (VBZ carries) (PP (IN with) (NP (PRP it))) (NP (NP (DT the) (JJ obvious) (NN risk)) (PP (IN of) (S (VP (VBG imposing) (NP (JJ drastic) (NN punishment)) (PP (IN before) (NP (NN conviction)))))))) (. .)))'
# currently broken!
quicktree(tree)

# <markdowncell>
# `searchtree()` requires a tree and a Tregex query. It will return a list of query matches.

# <codecell>
print searchtree(tree, r'/VB.?/ >># (VP $ NP)')
print searchtree(tree, r'NP')

# <markdowncell>
# Now you're familiar with the corpus and functions. In the sections below, we'll perform a formal, followed by a functional, analysis of risk. Let's start with the formal side of things:

# <markdowncell>
# ### Word classes of risk words in the NYT

# <markdowncell>
# In formal grammar, as we saw earlier, risk words can be nouns, verbs, adjectives and adverbs. Though we've seen that there are a lot of nouns, and that nouns are becoming more frequent, we don't yet know whether or not nouns are becoming more frequent in the NYT generally. To test this, we can do as follows:

# <codecell>
# 'any' is a special query, which finds any tag if 'pos'
# and any word if 'words'.
baseline = interrogator(annual_trees, 'pos', 'any', lemmatise = True)
risk_pos = interrogator(annual_trees, 'pos', r'__ < /(?i).?\brisk.?/', lemmatise = True)

# <markdowncell>
# In the cell above, the `lemmatise = True` option will convert tags like `'NNS'` to `'Noun'`.

# <codecell>
quickview(baseline.results, n = 10)

# <codecell>
quickview(risk_pos.results, n = 10)

# <markdowncell>
# Now, we can calculate the percentage of the time that a noun is a risk noun (and so on).

# <codecell>
open_words = ['Noun', 'Verb', 'Adjective', 'Adverb']
maths_done = editor(risk_pos.results, '%', baseline.results, sort_by = 'total', just_entries = open_words, skip_subcorpora = [1963])

# <codecell>
plotter('Percentage of open word classes that are risk words', maths_done.results, y_label = 'Percentage')


# <markdowncell>
# Neat, huh? We can see that nominalisation of risk is a very real thing.

# Our problem, however, is that formal categories like noun and verb only take us so far: in the phrase "risk metrics", risk is a noun, but performs a modifier function, for example. In the next section, we interrogate the corpus for *functional*, rather than *formal* categorisations of risk words.

# Before we start our corpus interrogation, we'll also present a *very* brief explanation of *Systemic Functional Linguistics*&mdash;the theory of language that underlies our analytical approach.

# <markdowncell>
# ### Functional linguistics

# <markdowncell>
# *Functional linguistics* is a research area concerned with how *realised language* (lexis and grammar) work to achieve meaningful social functions. One functional linguistic theory is *Systemic Functional Linguistics*, developed by Michael Halliday.

# <codecell>
from IPython.display import HTML
HTML('<iframe src=http://en.mobile.wikipedia.org/wiki/Michael_Halliday?useformat=mobile width=700 height=350></iframe>')

# <markdowncell>
# Central to the theory is a division between **experiential meanings** and **interpersonal meanings**.

# * Experiential meanings communicate what happened to whom, under what circumstances.
# * Interpersonal meanings negotiate identities and role relationships between speakers 

# Halliday argues that these two kinds of meaning are realised **simultaneously** through different parts of English grammar.

# * Experiential meanings are made through **transitivity choices**.
# * Interpersonal meanings are made through **mood choices**

# Here's one visualisation of it. We're concerned with the two left-hand columns. Each level is an abstraction of the one below it.

# <br>
# <img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/egginsfixed.jpg" alt="SFL metafunctions"  height="500" width="800" />
# <br>

# <markdowncell>
# Transitivity choices include fitting together configurations of:

# * Participants (*a man, green bikes*)
# * Processes (*sleep, has always been, is considering*)
# * Circumstances (*on the weekend*, *in Australia*)

# Mood features of a language include:

# * Mood types (*declarative, interrogative, imperative*)
# * Modality (*would, can, might*)
# * Lexical density&mdash;the number of words per clause, the number of content to non-content words, etc.

# Lexical density is usually a good indicator of the general tone of texts. The language of academia, for example, often has a huge number of nouns to verbs. We can approximate an academic tone simply by making nominally dense clauses: 

#       The consideration of interest is the potential for a participant of a certain demographic to be in Group A or Group B.

# Notice how not only are there many nouns (*consideration*, *interest*, *potential*, etc.), but that the verbs are very simple (*is*, *to be*).

# In comparison, informal speech is characterised by smaller clauses, and thus more verbs.

#       A: Did you feel like dropping by?
#       B: I thought I did, but now I don't think I want to

# Here, we have only a few, simple nouns (*you*, *I*), with more expressive verbs (*feel*, *dropping by*, *think*, *want*)

# > **Note**: SFL argues that through *grammatical metaphor*, one linguistic feature can stand in for another. *Would you please shut the door?* is an interrogative, but it functions as a command. *invitation* is a nominalisation of a process, *invite*. We don't have time to deal with these kinds of realisations, unfortunately.

# <markdowncell>
# ### Functional roles of *risk* in the NYT

# <markdowncell>
# > *A discourse analysis that is not based on grammar is not an analysis at all, but simply a running commentary on a text.* - [M.A.K. Halliday, 1994]()
# 
# Our analysis proceeded according to the description of the transitivity system in *systemic functional grammar* ([SFG: see Halliday & Matthiessen, 2004](#ref:hallmat)).

# The main elements of the transitivity system are *participants* (the arguments of main verbs) and *processes* (the verbal group). Broadly speaking, processes can be modified by circumstances (adverbs and prepositional phrases, and participants can be modified through epithets, classifiers (determiners, adjectives, etc).

# > This is an oversimplification, of course. Grab a copy of the [*Introduction to Functional Grammar*](http://www.tandfebooks.com/isbn/9780203783771) to find out more.

# Risk words can potentially be participants, processes or modifiers.

# *Risk-as-participant*: any nominal argument of a process that is headed by a risk word. *Examples*:
#
# * *the big risk*
# * *considerable risk*
# * *the risk of cancer*
# * *risk-management*

# *Risk-as-process*: risk word as the rightmost component of a VP. **Examples**:
#
# * *he risked his life*
# * *the company could potentially risk it*

# *Risk-as-modifier*: any risk word that modifies a participant or process. This includes many adjectival risk words and many risk words appearing within prepositional or adverbial phrases. **Examples**:
#
# * *the chance of risk*
# * *risky business*
# * *they riskily arranged to meet*

# To find the distributions of these, we define three (very long and complicated) Tregex queries as sublists of titles and patterns under *query*. We then use `multiquery()` to search for each query in turn.

# <codecell>
query = (['Participant', r'/(?i).?\brisk.?/ > (/NN.?/ >># (NP !> PP !> (VP <<# (/VB.?/ < '
        '/(?i)\b(take|takes|taking|took|taken|run|runs|running|ran|pose|poses|posed|posing)\b/)))) | >># (ADJP > VP)'], 
    ['Process', r'VP !> VP << (/VB.?/ < /(?i).?\brisk.?/) | > VP <+(VP) (/VB.?/ < '
        '/(?i)(take|taking|takes|taken|took|run|running|runs|ran|put|putting|puts|pose|poses|posed|posing)/'
        '>># (VP < (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'], 
    ['Modifier', r'/(?i).?\brisk.?/ !> (/NN.?/ >># (NP !> PP !> (VP <<# (/VB.?/ < '
        '/(?i)\b(take|takes|taking|took|taken|run|runs|running|ran|pose|poses|posed|posing)\b/)))) & !>># '
        '(ADJP > VP) & !> (/VB.?/ >># VP) & !> (/NN.?/ >># (NP > (VP <<# (/VB.?/ < /(?i)\b('
            'take|takes|taking|took|taken|run|runs|running|ran|pose|poses|posed|posing)\b/))))'])
functional_role = multiquery(annual_trees, query)

# <codecell>
ppm = editor(functional_role.results, '%', allwords.totals)

# <codecell>
plotter('Risk as participant, process and modifier', ppm.results)

# <markdowncell>
# Here we can see that modifier forms are become more frequent over time, and have overtaken risk processes. Later, we determine which modifier forms in particular are becoming more common.

# <codecell>
# Perhaps you want to see the result without 1963?
plotter('Risk as participant, process and modifier', functional_role.results.drop('1963'))

# <markdowncell>
# ### Risk as participant

# <markdowncell>
#
# > *You shall know a word by the company it keeps.* - [J.R. Firth, 1957](#ref:firth)
#
# Functionally, *risk* is most commonly a participant in the NYT. This gives us a lot of potential areas of interest. We'll go through a few here, but there are plenty of other things that we have to leave out for reasons of space.

# <markdowncell>
# ### Process types for participant risk

# <markdowncell>
# Here, we need to import verbose regular expressions that match any relational, verbal or mental process.

# <codecell>
from dictionaries.process_types import processes
print processes.relational
print processes.verbal

# <markdowncell>
# We can use these in our Tregex queries to look for the kinds of processes participant risks are involved in. First, let's get a count for all processes with risk participants:

# <codecell>
# get total number of processes with risk participant
query = r'/VB.?/ ># (VP ( < (NP <<# /(?i).?\brisk.?/) | >+(/.P$/) (VP $ (NP <<# /(?i).?\brisk.?/))))'
proc_w_risk_part = interrogator(annual_trees, 'count', query)


# <markdowncell>
# ### Relational processes with risk participant

# <codecell>
# subj_query = r'/VB.?/ < %s ># (VP >+(/.P$/) (VP $ (NP <<# /(?i).?\brisk.?/)))' % processes.relational
# obj_query = r'/VB.?/ < %s ># (VP < (NP <<# /(?i).?\brisk.?/))'  % processes.relational
query = r'/VB.?/ < /%s/ ># (VP ( < (NP <<# /(?i).?\brisk.?/) | >+(/.P$/) (VP $ (NP <<# /(?i).?\brisk.?/))))' % processes.relational
relationals = interrogator(annual_trees, 'words', query, lemmatise = True)

# <codecell>
rels = editor(relationals.results, '%', proc_w_risk_part.totals)

# <codecell>
plotter('Relational processes', rels.results)

# <markdowncell>
# ### Adjectives modifying risk

# <markdowncell>
# First, we can look at adjectives that modify a participant risk.

# <codecell>
query = r'/JJ.?/ > (NP <<# /(?i).?\brisk.?/ ( > VP | $ VP))'
adj_modifiers = interrogator(annual_trees, 'words', query, lemmatise = True)

# <codecell>
# Adjectives modifying nominal risk (lemmatised)
plotter('Adjectives modifying nominal risk (lemmatised)', adj_modifiers.results, 
    '%', adj_modifiers.totals, num_to_plot = 7)

# <markdowncell>
# Yuck! That doesn't tell us much. Let's try visualising the data in a few different ways. First, let's see what the top results look like...

# <codecell>
quickview(adj_modifiers.results)

# <markdowncell>
# OK, here are some ideas:

# <codecell>
# remove words with five or more letters
small_adjs = editor(adj_modifiers.results, '%', adj_modifiers.totals, skip_entries = r'.{5,}')

plotter('Adjectives modifying nominal risk (lemmatised)', small_adjs.results, num_to_plot = 6)

#get results with seven or more letters
big_adjs = editor(adj_modifiers.results, '%', adj_modifiers.totals, just_entries = '.{10,}')
plotter('Adjectives modifying nominal risk (lemmatised)', big_adjs.results, num_to_plot = 4)

#get a few interesting points
lst = ['more', 'high', 'calculated', 'potential']
select_adjs = editor(adj_modifiers.results, '%', adj_modifiers.totals, just_entries = lst)
plotter('Adjectives modifying nominal risk (lemmatised)', select_adjs.results, 
    num_to_plot = 4)

# <markdowncell>
# Wow! What's happening with *calculated risk* in 1963? Let's modify the original Tregex query a little and use `conc()` to find out.

# <codecell>
### old query: r'/JJ.?/ > (NP <<# /(?i).?\brisk.?/ ( > VP | $ VP))'
calculated_risk = r'/JJ.?/ < /(?i)calculated/> (NP <<# /(?i).?\brisk.?/ ( > VP | $ VP))'
# remove '( > VP | $ VP)' from the line above to get more instances
lines = conc('data/nyt/years/1963', calculated_risk)

# <markdowncell>
# ### Risk of ... ?

# <markdowncell>
# Next, we'll look at risk of (noun) constructions, as in:

# <codecell>
lines = conc('data/nyt/years/1988', r'/NN.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))', n = 25, random = True)

# <markdowncell>
# Notice that singular and plural forms may be in the results: both *substance* and *substances* are returned, and would be counted as unique items.

# If we want to ignore the difference between singular and plural (or different inflections of a verb), we need to use a *lemmatiser*. Luckily, `interrogator()` has one built in.

# When lemmatisation is necessary, we can pass a `lemmatise = True` parameter to `interrogator()`.

# Lemmatisation requires knowing the part of speech of the input. `interrogator()` determines this by looking at the first part of the Tregex query: if it's `/JJ.?/`, the lemmatiser will be told that the word is an adjective. If the part of speech cannot be located, noun is used as a default. You can also manually pass a tag to the lemmatiser with a `lemmatag = 'n/v/r/a'` option.

# <codecell>
# Risk of (noun)
query = r'/NN.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
risk_of = interrogator(annual_trees, 'words', query, lemmatise = True)

# <codecell>
rel_riskof = editor(risk_of.results, '%', risk_of.totals)
plotter('Risk of (noun)', rel_riskof.results)
plotter('Risk of (noun), 1999-2013', editor(rel_riskof.results, span_subcorpora = [1999,2013]).results)

# <markdowncell>
# ### A cautionary tale ...

# <markdowncell>
# At one point in our investigation, we looked specifically for military risks. From these results, we saw that *risk of attack* and *risk of war* were common. So, we plotted them:

# <codecell>
quickview(risk_of, n = 20)

# <codecell>
military = editor(risk_of.results, '%', risk_of.totals, just_entries = ['attack', 'war'])
plotter('Risk of (noun)', military.results) 

# <markdowncell>
#  We thought it was interesting how *risk of attack* rose in frequency shortly after 9/11. So, we decided to look more closely at *risk of attack*:

# <codecell>
attackrisk = r'/NN.?/ < /(?i)attack.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
lines = conc('data/nyt/years/2004', attackrisk, n = 15, random = True) 

# <markdowncell>
# Whoops. We were wrong. Almost all occurrences actually referred to *heart attack*!

# <codecell>
query = r'/NN.?/ < /(?i)\b(heart|terror).?/ $ (/NN.?/ < /(?i)\battack.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /().?\brisk.?/)))))' 
terror_heart = interrogator(annual_trees, 'words', query, lemmatise = True)

# <codecell>
plotter('Risk of heart and terror* attack', terror_heart.results, num_to_plot = 2)

# <markdowncell>
# So, we were a long way off-base. This is an ever-present danger in corpus linguistics. The decontextualisation needed to investigate the lexicogrammar of texts makes it easy to misunderstand (or worse, misrepresent) the data. Though concordancing is one of the oldest tasks in the corpus linguistic playbook, it remains a fundamental one, especially in discourse-analytic investigations.

# > ... *why did heart attacks become a big deal in 2004, you ask? Stay tuned ...*

# <markdowncell>
# ### Processes in which risk is subject/object

# <markdowncell>
# Here, we look at the kinds of predicators that occur when risk subject or object. Note that we remove *run/take/pose risk*, as these are actually verbal risks (see below).

# <markdowncell>
# By navigating parse trees in more complex ways, we can learn the kinds of processes risk as a participant is involved in.

# <codecell>
query = (r'/VB.?/ !< /(?i)(take|taking|takes|taken|took|run|running|runs|ran|put|putting|puts|pose|poses|posing|posed)/' \
    r' > (VP ( < (NP <<# (/NN.?/ < /(?i).?\brisk.?/))) | >+(VP) (VP $ (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))')
predicators = interrogator(annual_trees, 'words', query, lemmatise = True)
# subjectonly = r'./VB.?/ >># (VP >+(VP) (VP !> VP $ (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
# objectonly  =  (r'/VB.?/ >># (VP !< (/VB.?/ < /(?i)(take|taking|takes|taken|took|run|running'
# '|runs|ran|put|putting|puts|pose|posed|posing|poses)/) $ NP < (NP <<# (/NN.?/ < /(?i).?\brisk.?/)))')

# including take/run/pose/put at:
# query = /VB.?/ >># (VP  < (NP <<# (/NN.?/ < /(?i).?\brisk.?/)))'

# <codecell>
# Processes in which risk is subject/object
plotter('Processes in which risk is subject or object', editor(predicators.results, '%', predicators.totals).results, num_to_plot = 7)
# skip be:
plotter('Processes in which risk is subject or object', editor(predicators.results, 
'%', predicators.totals, skip_entries = ['be']).results, num_to_plot = 5)

# <markdowncell>
# Interesting! 

# <markdowncell>
# ### Risk as process

# <markdowncell>
# When *risk* is the main verb in a clause (e.g. *don't risk it*), it is the process. There are other kinds of risk processes, however: when risk occurs as the first object argument of certain nouns, it may be classified as a *process-range configuration* (an SFL term). Searching the data reveals four other main kinds of risk process:

# 1. *to take risk*
# 2. *to run risk*
# 3. *to put at risk*
# 4. *to pose a risk*

# In these cases, the expression is more or less idiomatic, and the main verb carries little semantic weight ([Eggins, 2004](#ref:eggins)). 

# We tracked the relative frequency of each construction over time.

# <codecell>
query = ([u'risk', r'VP <<# (/VB.?/ < /(?i).?\brisk.?\b/)'], 
    [u'take risk', r'VP <<# (/VB.?/ < /(?i)\b(take|takes|taking|took|taken)+\b/) < (NP <<# /(?i).?\brisk.?\b/)'], 
    [u'run risk', r'VP <<# (/VB.?/ < /(?i)\b(run|runs|running|ran)+\b/) < (NP <<# /(?i).?\brisk.?\b/)'], 
    [u'put at risk', r'VP <<# /(?i)(put|puts|putting)\b/ << (PP <<# /(?i)at/ < (NP <<# /(?i).?\brisk.?/))'], 
    [u'pose risk', r'VP <<# (/VB.?/ < /(?i)\b(pose|poses|posed|posing)+\b/) < (NP <<# /(?i).?\brisk.?\b/)'])
processes = multiquery(annual_trees, query)

# <codecell>
proc_rel = editor(processes.results, '%', processes.totals)

# <codecell>
plotter('Risk processes', processes.results)

# <markdowncell>
# Subordinate processes are often embedded within clauses containing a risk predicator, as in *Obama risks alienating voters*.

# <codecell>
# to risk losing/being/having etc
query = r'VBG >># (VP > (S > (VP <<# (/VB.?/ < /(?i).?\brisk.?/))))'
risk_verbing = interrogator(annual_trees, 'words', query)

# <codecell>
r_verbing = editor(risk_verbing.results, '%', risk_verbing.totals)

plotter('Process as risked thing', r_verbing.results, y_label = 'Percentage of all occurrences')

# <markdowncell>
# In this kind of risk process, the risker is typically a powerful member of society. While this is rather explicit in some cases (it's hard to image that a mechanic would risk alienating his/her apprentice), we can observe that this is the case for less obvious examples, like *to risk becoming*:

# <codecell>
lines = conc('data/nyt/years/2013', r'VBG < /(?i)becom/ >># (VP > (S > (VP <<# (/VB.?/ < /(?i).?\brisk.?/))))', n = 15, random = True)

# <markdowncell>
# ### Subjects of risk processes

# <codecell>
query = r'/NN.?/ !< /(?i).?\brisk.?/ >># (@NP $ (VP <+(VP) (VP ( <<# (/VB.?/ < /(?i).?\brisk.?/) | <<# (/VB.?/ < /(?i)(take|taking|takes|taken|took|run|running|runs|ran|put|putting|puts|pose|poses|posed|posing)/) < (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))))'
subj_of_risk_process = interrogator(corpus, 'words', query, lemmatise = True)

# <codecell>

# <codecell>


# <markdowncell>
# ### Objects of risk processes

# <markdowncell>
# We can locate the most common objects of risk processes:

# <codecell>
# Objects of risk processes
query = r'/NN.?/ >># (NP > (VP <<# (/VB.?/ < /(?i).?\brisk.?/)))'
risk_objects = interrogator(annual_trees, 'words', query, 
    lemmatise = True, titlefilter = False)

# <codecell>
plotter('Objects of risk processes', editor(risk_objects.results, 
    '%', risk_objects.totals).results, y_label = 'Percentage of all occurrences')

# <markdowncell>
# Notice that both the `potential harm* and *risked things* can fit in this position. We can view the most common results and create new lists for risked things/potential harms with *surgeon()`.

# <codecell>
quickview(risk_objects, n = 100)

# <codecell>
riskobject_regex = (r'(?i)^\b(life|everything|money|career|health|reputation|capital|future|'
    r'job|safety|possibility|anything|return|neck|nothing|lot)$\b')
riskedthings = editor(risk_objects.results, skip_entries = riskobject_regex)
potentialharm = editor(risk_objects.results, just_entries = riskobject_regex)
plotter('Risked things', potentialharm.results, num_to_plot = 7)
# a method for quickly removing entries from the plot:
plotter('Risked things (minus life)', potentialharm.results.drop('life', axis = 1), num_to_plot = 3)
plotter('Potential harm', riskedthings.results, num_to_plot = 7)

# <markdowncell>
# It's interesting how powerful people risk losing and alienating electorates, fanbases or contracts, while less powerful people risk their jobs and safety, or their life or neck.

# <markdowncell>
# ### Risk as modifier

# <markdowncell>
# Risk words can serve as modifiers in a number of ways. We divided risk as modifier into five main types.

# <markdowncell>
# | Modifier type | Example  |
# |---|---|
# | Adjectival modifiers of participants  |  *the riskiest decision* | 
# | Pre-head nominal modifiers of participants  |  *risk management* | 
# |  Post-head nominal modifiers of participants |  *the money to risk* | 
# | Adverbial modifiers of processes  |  *it riskily moved* | 
# | As head of NP that is head of a cirumstance  | *she was at risk*  | 

# <codecell>
query = ([u'Adjectival modifier', r'/NN.?/ >># (NP < (/JJ.?/ < /(?i).?\brisk.?/))'],
    [u'Pre-head nominal modifier', r'/NN.?/ < /(?i).?\brisk.?/ $ (/NN.?/ >># NP !> CC)'], 
    [u'Post-head modifier', r'/NN.?/ >># (NP < (PP < (NP <<# /(?i).?\brisk.?/)))'], 
    [u'Adverbial modifier', r'RB < /(?i).?\brisk.?/'],
    [u'Circumstance head', r'/NN.?/ < /(?i).?\brisk.?/ >># (NP > (PP > (VP > /\b(S|SBAR|ROOT)\b/)))'])
modifiers = multiquery(annual_trees, query)

# <codecell>
plotter('Types of risk modifiers', editor(modifiers.results, '%', modifiers.totals, skip_subcorpora = [1963]).results)

# <markdowncell>
# This is very interesting: the most common form in 1987 has become the least common in 2014!

# <markdowncell>
# We can also pull out words modified by adjectival risk:

# <codecell>
# Participants modified by risk word
query = r'/NN.?/ >># (NP < (/JJ.?/ < /(?i).?\brisk.?/) ( > VP | $ VP))'
mod_by_adj_risk = interrogator(annual_trees, 'words', query, 
    lemmatise = True, titlefilter = False)

# <codecell>
plotter('Participants modified by risk', mod_by_adj_risk.results, 
    num_to_plot = 7)

# <markdowncell>
# We looked at the most common adjectival risks:

# <codecell>
query = r'/JJ.?/ < /(?i).?\brisk.?/'
adjrisks = interrogator(annual_trees, 'words', query, 
    lemmatise = False)

# <codecell>
arisk = editor(adjrisks.results, '%', allwords.totals) 

# <codecell>
# remember that we can still plot using all words/all risk words 
plotter('Most common adjectival risks', arisk.results, y_label = 'Percentage of all words', num_to_plot = 5)

# <markdowncell>
# Given the increasing frequency of at-risk constructions, we then looked at what it is that this modifier typically modifies.

# <codecell>
# At-risk thing
query = r'/NN.?/ >># (NP < (/JJ.?/ < /(?i).?\bat-risk/) ( > VP | $ VP))'
at_risk_things = interrogator(annual_trees, 'words', query, 
    lemmatise = True)

# <codecell>
plotter('At-risk things', editor(at_risk_things.results, 
    '%', at_risk_things.totals).results)

# <markdowncell>
# The query below finds both *thing at risk* and *at-risk thing*.

# <codecell>
# at-risk person / person at risk combined
query = r'/NN.?/ ( >># (NP < (PP <<# /(?i)at/ << (NP <<# /(?i)\brisk.?/))) | ( >># (NP < (/JJ.?/ < /(?i)at-risk.?/))))'
n_atrisk_n = interrogator(annual_trees, 'words', query, 
    lemmatise = False, titlefilter = False)

# <codecell>
plotter('At-risk thing or thing at risk', n_atrisk_n.results)

# <markdowncell>
# Vulnerable human populations are the main theme of this category: indeed, it's difficult to imagine *at-risk corporations* or *at-risk leaders*.

# <markdowncell>
# ### Proper nouns and risk sentences

# <markdowncell>
# We searched to find the most common proper noun strings.

# `interrogator()`'s `titlefilter` option removes common titles, first names and determiners to make for more accurate counts. It is useful when the results being returned are groups/phrases, rather than single words.

# <codecell>
# Most common proper noun phrases
query = r'NP <# NNP >> (ROOT << /(?i).?\brisk.?\b/)'
propernouns = interrogator(annual_trees, 'words', query, 
    titlefilter = True)

# <codecell>
plotter('Most common proper noun phrases', editor(propernouns.results, '%', propernouns.totals).results)

# <codecell>
quickview(propernouns, n = 200)

# <markdowncell>
# Notice that there are a few entries here that refer to the same group. (*f.d.a.* and *food and drug administration*, for example). We can use `editor()` to fix these.

# <codecell>
# indices change after editor, remember, so
# make sure you quickview results after every merge.
merged_propernouns = editor(propernouns.results, merge_entries = [13, 21])
merged_propernouns = editor(merged_propernouns, merge_entries = [9, 29])
merged_propernouns = editor(merged_propernouns, merge_entries = [44, 109])
merged_propernouns = editor(merged_propernouns, merge_entries = [61, 112])
merged_propernouns = editor(merged_propernouns, merge_entries = [186, 199])
merged_propernouns = editor(merged_propernouns, merge_entries = [65, 130])
merged_propernouns = editor(merged_propernouns, merge_entries = [85, 152], newname = 152)
merged_propernouns = editor(merged_propernouns, merge_entries = [23, 132])
quickview(merged_propernouns, n = 200)

# <markdowncell>
# Now that we've merged some common results, we can build some basic thematic categories. Let's make a list of lists:

# <codecell>
theme_list = [['People', '(?i)^\b(bush|clinton|obama|greenspan|gore|johnson|mccain|romney|kennedy|giuliani|reagan)$\b'],
    ['Nations', '(?i)^\b(iraq|china|america|israel|russia|japan|frace|germany|iran|britain|u\.s\.|afghanistan|australia|canada|spain|mexico|pakistan|soviet union|india)$\b'],
    ['Geopolitical entities', r'(?i)^\b(middle east|asia|europe|america|soviet union|european union)$\b'],
    ['US places',], r'(?i)^\b(new york|washington|wall street|california|manhattan|new york city|new jersey|north korea|italy|greece|bosniaboston|los angeles|broadway|texas)$\b'],
    ['Companies', r'(?i)^\b(merck|avandia|citigroup|pfizer|bayer|enron|apple|microsoft|empire)$\b'],
    ['Organisations', r'(?i)^\b(white house|congress|federal reserve|nasa|pentagon|f\.d\.a \.|c\.i\.a \.|f\.b\.i \.|e\.p\.a \.)$'],
    ['Medical', r'(?i)^\b(vioxx|aids|aid|celebrex|f\.d\.a \.|pfizer|bayer|merck|avandia)$']]

# <codecell>
# add data to our sublists
for entry in theme_list:
    entry.append(editor(merged_propernouns.results, '%', propernouns.totals, 
                  just_entries = entry[1]))

# <codecell>
# plot some results
ystring = 'Percentage of all proper noun groups'
for name, query, data in theme_list:
    plotter(name, result.results, y_label = ystring)

# <markdowncell>
# Let's compare these topics in the same chart, using Pandas to join everything together:

# <codecell>
import pandas
# get the totals from each theme and put them together
them_comp = pandas.concat([data.totals for name, query, data in theme_list], axis = 1, columns = [name for name, query, data in theme_list])
them_comp = editor(them_comp, '%', propernouns.totals)
quickview(them_comp)

# <codecell>
plotter('Themes', them_comp)
plotter('Themes', them_comp, subplots = True)

# <markdowncell>
# These charts reveal some interesting patterns.

# * We can clearly see presidencies and rival candidates come and go
# * Similarly, the wars in Iraq and Afghanistan are easy to spot
# * Naturally, the Soviet Union is a very frequent topic in 1963. It rises in frequency until its collapse. More recently, Russia can be seen as more frequently co-occurring with risk words.
# * The Eurozone crisis is visible
# * From the Organisations and Things, we can see the appearance of Merck and Vioxx in 2004, as well as Empire...

# <codecell>
vioxx = editor(propernouns.results, '%', propernouns.totals, just_entries = r'(?i)^\b(vioxx|merck)\b$')
plotter('Merck and Vioxx', vioxx.results)
plotter('Merck and Vioxx', vioxx.results, yearspan = [1998,2012])

# <markdowncell>
# Vioxx was removed from shelves following the discovery that it increased the risk of heart attack. It's interesting how even though terrorism and war may come to mind when thinking of *risk* in the past 15 years, this health topic is easily more prominent in the data.


# <markdowncell>
# ### Arguability

# <markdowncell>
# In terms of interpersonal meanings, we were interested in the *arguability* of risk: that is, the extent to which risk words are a core or peripheral part of the meaning being negotiated by writer and reader.

# In SFL, arguability is related to the mood system. Certain roles within the mood of a clause are more arguable than others. In a hypothetical exchange, we can see that certain parts of the proposition can be easily questioned:

#      A: I think Kim was heading over to the little pub on the corner.
#      B1: Was he?

# The two grammatical roles being restated here are the Subject (*he*) and the Finite (*was*). These are the two most arguable roles in which a risk word could appear.

# If the speaker wanted to argue about the size of the pub, simple replies seem almost like *non sequiturs*:

#      A: I think Kim was heading over to the little pub on the corner.
#      B: It's not that little!

# Note how even in this stylistically marked example, B turns the pub and its nature into the Subject and Finite, in order to make it the main area of contention within the conversation.

# Using SFL's description of the mood system as a guide, we constructed a basic (i.e. simplified) scale of arguability.

# | Role in the mood system | Arguability |
# | ----------------------- | ----------- |
# | Subject                 | Very high   |
# | Finite                  | High        |
# | Predicator                  | Medium        |
# | Complement              | Low      |
# | Adjunct                 | Very low         |

# <markdowncell>
# ### Arguability of risk

# <markdowncell>
# We were interested in whether there are any longitudinal changes in the proportion of risk words in each mood role. 

# For this, rather than interrogating phrase-structure parses, we needed to interrogate dependency parses, which provide basic information about the functional role of a word in a clause. By default, the parser we used (Stanford CoreNLP) outputs three different dependency grammars. Any of the three can be selected for analysis.

# `interrogator()` can also work with the dependency parses provided by CoreNLP. To do this, we use some different arguments. Though the first argument is still a path to the corpus, instead of a Tregex query, we use a regular expression. Instead of 'count', 'words', 'pos' or 'both', we use:

# * `funct`: find the functional role of words matching the regular expression
# * `gov`: find the functional role of words matching the regular expression, as well as the word on which the match is dependent.
# * `number`: find the 'index' of words matching the regular expression.

# There is also an optional argument:

# * `dep_type`: the kind of dependencies parses we want to search: *'basic-dependencies'*, '*collapsed-dependencies'*, or *'collapsed-ccprocessed-dependencies'*.

# You can still use the `lemmatise` option, though it will only do something if you're working with the `gov` option.



# We were interested in each of these three kinds of dependency information.

# With regard to (4): though the *collapsed-cc-dependencies* are perhaps the most commonly used, we use basic dependencies here, as this assisted the lemmatisation process (see the report for more information).

# <markdowncell>
# ### Functional role of risk in dependency parses

# <codecell>
# set path to dependency parses
annual_deps = 'data/nyt/basic-dependencies/years'

# <codecell>
risk_functions = interrogator(annual_deps, 'funct', r'(?i)\brisk', dep_type = 'basic-dependencies')

# <codecell>
plotter('Top functions of risk words', risk_functions.results, '%', risk_functions.totals)

# <markdowncell>
# We can divide these functions into experiential categories of Participant, Process and Modifier

# <codecell>
merged = editor(risk_functions.results, [1, 2, 10, 18, 17, 20, 24], newname = 'Participant')
merged = merger(merged.results, [5, 6, 7, 11, 20, 22], newname = 'Process')
merged = merger(merged.results, [1, 4, 5, 8, 9, 12, 13, 14, 17], newname = 'Modifier')

merging = merger(risk_functions.results, r'^(dobj|nsubj|nsubjpass|csubj|acomp|iobj|csubjpass)$', newname = 'Participant')
merged = merger(merged.results, r'^(root|ccomp|xcomp|pcomp|auxpass|aux)$', newname = 'Process')
merged = merger(merged.results, [1, 4, 5, 8, 9, 12, 13, 14, 17], newname = 'Modifier')


# <markdowncell>
# We can also use this information to determine whether risk is more commonly the experiential subject or object:

# <codecell>
subjobj = editor(risk_functions.results, just_entries = r'^(nsubj|(d|i)obj)')
subjobj = editor(subjobj.results, merge_entries = r'', newname = 'Experiential subject')
subjobj = editor(subjobj.results, merge_entries = r'', newname = 'Experiential object')
mergesub = merger(subjobj, [0, 2, 3], newname = 'Experiential object')
mergesub[1][0] = 'Experiential subject'



# <markdowncell>
# We can also merge results into the categories of Subject, Finite/Predicator, Complement and Adjunct:

# <codecell>
quickview(risk_functions, n = 30)
# quickview(merged_role, n = 30)

# <codecell>
# run the first part, uncomment above, check, repeat ...
merged_role = merger(risk_functions.results, [2, 10, 18, 24], newname = 'Subject') # add csubj
#quickview(merged_role)
merged_role = merger(merged_role, [6, 22, 23], newname = 'Finite/Predicator')
merged_role = merger(merged_role, [1, 16, 18, 20], newname = 'Complement')
merged_role = merger(merged_role, [0, 3, 5, 10, 13, 16, 20], newname = 'Adjunct')

# <codecell>
# remove all other items
merged_role = surgeon(merged_role, [0, 1, 2, 4], remove = False)

# <codecell>
# resort this list:
from operator import itemgetter # for more complex sorting
to_reorder = list(merged_role)
mr_sorted = sorted(list(merged_role), key=itemgetter(1), reverse = True)

# <codecell>
plotter('Functional role using dependency parses', merged_role, '%', risk_functions.totals)

# <markdowncell>
# ### Role and governor of risk

# <codecell>
role_and_gov = interrogator(annual_deps, 'gov', r'(?i)\brisk', dep_type = 'basic-dependencies', lemmatise = True)

# <codecell>
plotter('Governors of risk and their roles', role_and_gov.results, '%', role_and_gov.totals)

# <markdowncell>
# We can post-process this list in a couple of interesting ways:

# <codecell>

# <markdowncell>
# ### Dependency index

# <markdowncell>
# In a dependency parse, smaller indices will be given to words close to the root of the dependency string. These correspond (roughly) with more arguable roles in SFL. Large indices are more dependent, and are generally less arguable.

# Thus, we also thought we could roughly approximate arguability by looking for the index of each risk word within each dependency parse.

# <codecell>
risk_indices = interrogator(annual_deps, 'number', r'(?i)\brisk', dep_type = 'basic-dependencies')

# <markdowncell>
# Our existing way of plotting results needed to be modified in order to show the information provided by the `number` search.

# **in progress, sorry...**

# <markdowncell>
# ### Risk in economics, health and politics articles

# <markdowncell>
# We used article metadata features in the NYT annotated corpus to build corpora of economics, health and politics articles.

# > No metadata was available for 1963 editions, and thus they are not plotted in this section.

# <markdowncell>
# Before interrogating topic subcorpora, we built `topix_search()` and `topix_plot()`. These are short functions to interrogate and plot each subcorpus in turn. They have been automatically loaded in with interrogators.ipy in the first cell.

# <codecell>
# get a list of the economics, health and politics subcorpora
trees = 'data/nyt/trees'
topic_trees = [d for d in os.listdir(trees)
          if os.path.isdir(os.path.join(path,d))
          and d != 'years']

# <markdowncell>
# It's useful to keep in mind that `conc()` can loop through subcorpora. Two kinds of loops are presented below.

# <codecell>
import pprint # nice looking results
year_of_interest = '2002'
for topic in topic_trees:
    lines = conc(os.path.join(trees,topic,year_of_interest), 
        r'PP < (NP <# (/NN.?/ < /(?i).?\brisk.?\b/))', n = 15, random = True)
    for line in lines:
        print line

# <codecell>
topic = 'economics'
# note that years here are strings (in quotation marks), rather than integers.
years = ['1989', '1990', '1991']
for year in years:
    lines = conc(os.path.join(trees,topic,year), r'/(?i)risky/', n = 15, random = True, window = 50)
    #print lines

# <markdowncell>
# ### Proper noun phrases

# <codecell>
query = r'NP <# NNP >> (ROOT << /(?i).?\brisk.?\b/)'
topics_propernouns = topix_search(topic_trees, 'words', query, titlefilter = True)

# <markdowncell>
# When working with topic subcorpora, you can add an extra argument to `quickview()` to see the first results from each subcorpus:

# <codecell>
quickview(topics_propernouns, n = 20, topics = True)

# <codecell>
topix_plot('Proper noun phrases', topics_propernouns)

# <codecell>
# people in politics articles
# note, we just use `interrogator()` and `plotter()`, because we're only interested in a single topic subcorpus.
query = r'NP <# NNP >> (ROOT << /(?i).?\brisk.?\b/)'
propnounphrases = interrogator('nyt/politics', 'words', query, titlefilter = True)

# <codecell>
polpeople = surgeon(propnounphrases.results, 
    r'(?i)\b(obama|bush|clinton|dole|romney|reagan|carter|ford|mccain|johnson|kennedy|gore)\b', 
  )
#topix_plot('Proper noun phrases', results)
plotter('Politicians in sentences containing a risk word', polpeople)

# <markdowncell>
# ### Adjectives modifying participant risk

# <codecell>
query = r'/JJ.?/ > (NP <<# /(?i).?\brisk.?/ ( > VP | $ VP))'
topics_adjmod = topix_search(topic_trees, 'words', query)
    
# <codecell>    
topix_plot('Adjectives modifying participant risk', topics_adjmod)

# <markdowncell>
# ### Risk of (noun)

# <codecell>
query = r'/NN.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
topics_riskof = topix_search(topic_trees, 'words', query)

# <codecell>
topix_plot('Risk of (noun)', topics_riskof)

# <markdowncell>
# ### Arguability in topic subcorpora

# <markdowncell>
# We can also look for arguability information using dependency-parsed versions of our topic subcorpora.

# <markdowncell>
# ### General queries

# <markdowncell>
# We also performed some basic querying of all parsed data. Though not discussed in our report, these findings may be interesting in their own right.

# In the examples below, we use *multiplier = 1*. This is for making ratios.

# <codecell>
openwords = r'/\b(JJ|NN|VB|RB)+.?\b/'
clauses = r'S < __'
opencount = interrogator(annual_trees, 'count', openwords)
clausecount = interrogator(annual_trees, 'count', clauses)

# <codecell>
# ratio of open to closed word classes
# already done this one:

# openwords = r'/\b(JJ|NN|VB|RB)+.?\b/'
# opencount = interrogator(annual_trees, 'count', openwords)

closedwords = r'/\b(DT|IN|CC|EX|W|MD|TO|PRP)+.?\b/'
closedcount = interrogator(annual_trees, 'count', closedwords)

# <codecell>
# ratio of nouns/verbs
nounquery = r'/NN.?/ < __'
verbquery = r'/VB.?/ < __'
nouncount = interrogator(annual_trees, 'count', nounquery)
verbcount = interrogator(annual_trees, 'count', verbquery)

# <markdowncell>
# ... and finally, plot the results:

# <codecell>
#plot results
plotter('Lexical density', opencount.totals, '%', clausecount.totals, 
            y_label = 'Lexical Density Score', multiplier = 1)

plotter('Open/closed word classes', opencount.totals, '%', closedcount.totals, 
            y_label = 'Open/closed ratio', multiplier = 1)

plotter('Noun/verb ratio', nouncount.totals, '%', verbcount.totals, 
            y_label = 'Noun/verb ratio', multiplier = 1)

# <markdowncell>
# ### General dependency queries

# <markdowncell>
# Our final area of investigation was general dependency. This is identical to our investigation of risk dependencies, excepyt that we change our token definition from any risk word to any word.

# <codecell>
all_functions = interrogator(annual_deps, 'funct', 
    r'(?i)[a-z0-9]', dep_type = 'basic-dependencies')

# <codecell>
plotter('Most common functional roles in parsed data', 
    all_functions.results, '%', all_functions.totals)

# <markdowncell>
# We could then merge results into the categories of Subject, Finite/Predicator, Complement and Adjunct:

# <codecell>
quickview(all_functions, n = 60)

# <codecell>
merged_role = merger(all_functions.results, [], newname = 'Subject')
merged_role = merger(merged_role, [], newname = 'Finite/Predicator')
merged_role = merger(merged_role, [], newname = 'Complement')
merged_role = merger(merged_role, [], newname = 'Adjunct')
# remove all other items
merged_role = surgeon(merged_role, [])

plotter('Functional role using dependency parses', merged_role, '%', all_functions.totals)

# <markdowncell>
# ### Role and governor

# <codecell>
all_role_and_gov = interrogator(annual_deps, 'gov', r'(?i)[a-z0-9]', 
    dep_type = 'basic-dependencies', lemmatise = True)

# <codecell>
plotter('Most common dependencies for risk words', all_role_and_gov.results, 
    '%', all_role_and_gov.totals)

# <markdowncell>
# ### Dependency index

# <markdowncell>
# We were interested in whether the changes in risk dependency indices were part of a more general trend.

# <codecell>
all_indices = interrogator(annual_deps, 'number', r'(?i)[a-z0-9]', dep_type = 'basic-dependencies')

# <markdowncell>
# Our existing way of plotting results needed to be modified in order to show the information provided by the *number* search.

# <codecell>
from operator import itemgetter # for more complex sorting
# make a new list to reorder
to_reorder = list(all_indices.results)
dep_num = sorted(to_reorder, key=itemgetter(0), reverse = True)


# <codecell>
plotter('Dependency indices for all words', sorted_indices, '%', all_indices.totals)

# Due to limitations in available computational resources, our investigation did not involve parsing the full collection of NYT articles: we only used paragraphs containing a risk word. Longitudinal changes in the examples above are interesting in their own right. We hope in a further project to be able to expand the size of our corpus dramatically in order to determine the causes of these more general changes.

# <markdowncell>
# ### Discussion

# <markdowncell>
# ### Limitations

# <markdowncell>
# A key challenge accounting for the diverse ways in which a semantic meaning can be made in lexis and grammar. If we are interested in how often *money* is the risked thing, we have to design searches that find: 

#      She risked her money
#      She risked losing her money
#      Money was risked
#      It was risked money
#      The risk of money loss was there
#      She took her money from her purse and risked it.

# Though we can design queries to match any of these, it is very difficult to automate this process for every possible 'risked thing'. It's also very hard to know when we have finally developed a query that matches everything we want.

# An added issue is how to treat things like:

#      She didn't risk her money
#      She risked no money
#      She could risk money

# Here, the semantic meanings are very different (the risking of money did not occur), but each would match the queries we designed for the above.

# Should these results be counted or excluded? Why?

# <markdowncell>
# ### References

# <markdowncell>
# <a id="eggins"></a>
# Eggins, S. (2004). Introduction to systemic functional linguistics. Continuum International Publishing Group.
#
# <a id="firth"></a>
# Firth, J. (1957).  *A Synopsis of Linguistic Theory 1930-1955*. In: Studies in Linguistic Analysis, Philological Society, Oxford; reprinted in Palmer, F. (ed.) 1968 Selected Papers of J. R. Firth, Longman, Harlow.
#
# <a id="hallmat"></a>
# Halliday, M., & Matthiessen, C. (2004). An Introduction to Functional Grammar. Routledge.
#


# <headingcell level=1>
# Work in progress


# <markdowncell>
# It's also possible to interrogate the corpus for keywords and/or ngrams:

# <codecell>
kwds = interrogator(annual_trees, 't', 'keywords', lemmatise = True)
ngms =  interrogator(annual_trees, 't', 'ngrams', lemmatise = True)
# <codecell>
ngms =  interrogator(annual_trees, 't', 'ngrams', lemmatise = True)

# <markdowncell>
# Let's sort these, based on those increasing/decreasing frequency:

# <markdowncell>
# Let's make some thematic categories by looping through the results with surgeon, and renaming 'Totals' to the name of the category. Be sure that later categories don't include earlier categories!

# <codecell>
regexes = [(r'\b(legislature|medicaid|republican|democrat|federal|council)\b', 'Government organisations'),
(r'\b(empire|merck|commerical)\b', 'Companies'),
(r'\b(athlete|policyholder|patient|yorkers|worker|infant|woman|man|child|children|individual|person)\b', 'People, everyday'),
(r'\b(marrow|blood|lung|ovarian|breast|heart|hormone|testosterone|estrogen|pregnancy|prostate|cardiovascular)\b', 'The body'),
(r'\b(reagan|clinton|obama|koch|slaney|starzl)\b', 'Specific people'),
(r'\b(implant|ect|procedure|abortion|radiation|hormone|vaccine|medication)\b', 'Treatment'),
(r'\b(addiction|medication|drug|statin|vioxx)\b', 'Drugs'),
(r'\b(addiction|coronary|aneurysm|mutation|injury|fracture|cholesterol|obesity|cardiovascular|seizure|suicide)\b', 'Symptom'),
(r'\b(worker|physician|doctor|midwife|dentist)\b', 'Healthcare professional'),
(r'\b(transmission|infected|hepatitis|virus|hiv|lung|aids|asbestos|malaria|rabies)\b', 'Infectious disease'),
(r'\b(huntington|lung|prostate|breast|heart|obesity)\b', 'Non-infectious disease'), 
(r'\b(policyholder|reinsurance|applicant|capitation|insured|insurer|insurance|uninsured)\b', 'Finance'),
(r'\b(experiment|council|journal|research|university|researcher|clinical)\b', 'Research')]

# <codecell>
themed_keys = []
for regex, name in regexes:
    tmp = surgeon(kwds.results, regex, remove = False)
    tmp.totals[0] = name
    themed_keys.append(tmp.totals)
# here, we are generating a totals branch
themed_keys = surgeon(themed_keys, r'.*', remove = False)

themed_ngrams = []
for regex, name in regexes:
    tmp = surgeon(ngms.results, regex, remove = False)
    tmp.totals[0] = name
    themed_ngrams.append(tmp.totals)
themed_ngrams = surgeon(themed_ngrams, r'.*', remove = False)

# <codecell>
# 

# <codecell>
inc_keys = resorter(themed_keys.results, sort_by = increase)
dec_keys = resorter(themed_keys.results, sort_by = decrease)

# <codecell>
inc_n = resorter(themed_ngms.results, sort_by = increase)
dec_n = resorter(themed_ngms.results, sort_by = decrease)

# <codecell>

# <markdowncell>
# We used the following code to count the number of articles per topic:

import os
output = []
base = 'data/nyt/ts'
for d in os.listdir(base):
    datum = []
    datum.append(d.title())
    tot = 0
    for sub in os.listdir(os.path.join(base, d)):
        count = len(os.listdir(os.path.join(base, d, sub)))
        tot += count
        datum.append([int(sub), count])
    datum.append(['Total', tot])
    output.append(datum)

plotter('Number of articles in each subcorpus', output, y_label = 'Number of articles', legend_totals = True)



# <headingcell level=3>
# Risker value

# <markdowncell>
# A novel thing we can do with our data is determine the amount of time a word occurs in a given role. We know that Bush, Clinton, woman, bank, and child are common nouns in the corpus, but we do not yet know what percentage of the time they are playing a specific role in the risk frame.

# To determine what percentage of the time these words take the role of risker, we start by counting their occurrences as risker, and in the corpus as a whole:

# <codecell>
n_query = r'/NN.?/ !< /(?i).?\brisk.?/ >># NP'
noun_lemmata = interrogator(corpus, 'words', n_query, lemmatise = True)
query = r'/NN.?/ !< /(?i).?\brisk.?/ >># (@NP $ (VP <+(VP) (VP ( <<# (/VB.?/ < /(?i).?\brisk.?/) | <<# (/VB.?/ < /(?i)(take|taking|takes|taken|took|run|running|runs|ran)/) < (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))))'
subj_of_risk_process = interrogator(annual_trees, 'words', query, lemmatise = True)

# <markdowncell>
# Then, we pass `editor()` a second list of results, rather than just totals, and use the `just_totals = True' argument:

# <codecell>
rel_risker = editor(subj_of_risk_process.results, '%', noun_lemmata.results, just_totals = True)

# <markdowncell>
# Note that a `threshold` was printed. This number represents the minimum number of times an entry must occur in `noun_lemmata.totals` in order for the result to count.

# We can pass in a threshold of our own. Note that if we set it to zero, unusual words are at the top of the results list:

# <codecell>
rel_risker = editor(subj_of_risk_process.results, '%', noun_lemmata.results, just_totals = True, threshold = 1)

# <markdowncell>
# Aside from giving it an integer value, you can pass it `'low'`, `'medium' or `'high'`. `editor()` then creates thresholds based on the total total of `noun_lemmata.totals`. Passing no threshold results in '`medium` being used as the default:

rel_risker = editor(subj_of_risk_process.results, '%', noun_lemmata.results, just_totals = True, threshold = 'low')
rel_risker = editor(subj_of_risk_process.results, '%', noun_lemmata.results, just_totals = True, threshold = 'medium')
rel_risker = editor(subj_of_risk_process.results, '%', noun_lemmata.results, just_totals = True, threshold = 'high')



# <codecell>


# <codecell>
plotter('Risker percentage', kind = 'bar')



# <codecell>
