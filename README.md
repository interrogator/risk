## Discourse-semantics of risk in the *New York Times*, 1963&mdash;2014: a corpus linguistic approach

This repository contains everything created and used in our longitudinal analysis of risk language in the *New York Times*. The investigation involves systematic analysis of over 150,000 NYT paragraphs containing a risk token (*risk*, *risking*, *at-risk*, *risk-to-reward*, *risk-laden*, etc), though the tools and functions could easily be used with other datasets. These paragraphs have been parsed with *Stanford CoreNLP*, and are interrogated using *Tregex* queries, combined with custom-built Python functions:

| **Function name** | **Purpose**                            |
| ----------------- | ---------------------------------- |
| `interrogator()`  | interrogate bracketted trees using Tregex, NLTK lemmatisation, etc.         |
| `dependencies()`  | interrogate dependency parses         |
| `plotter()`       | visualise `interrogator()` results using Matplotlib |
| `table()`          | return plotter() results as table using Pandas |
| `quickview()`     | view top `interrogator()` results      |
| `tally()`       | get total frequencies for `interrogator()` results      |
| `surgeon()`       | quickly edit `interrogator()` results      |
| `merger()`       | quickly merge `interrogator()` results      |
| `conc()`          | Concordancing using Tregex, regex |
| `keywords()`          | get keywords and ngrams from subcorpora, concordance lines (uses Spindle) |
| `collocates()`          | get collocates from from subcorpora, concordance lines, etc. |
| misc | A few other simple functions for working with corpora |

Here's a basic example of `interrogator()` and `plotter()':

```python
# set path to corpus
corpus = 'data/nyt/trees/years'
# make tregex query
q = r'/NN.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
# count terminals/leaves of trees only, and do lemmatisation:
riskofnoun = interrogator(corpus, '-t', q, lemmatise = True)
# plot top 7 entries as percentage of all entries:
plotter('Risk of ... ', riskofnoun.results, fract_of = riskofnoun.totals, num_to_plot = 7, skip63 = False)
```

Output: 

<br>
<img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/riskofnoun.png" />
<br>


Our *IPython Notebook* presents the code used in our analysis side-by-side with our results. It can be viewed via *nbviewer* [here](http://nbviewer.ipython.org/github/interrogator/risk/blob/master/risk.ipynb). 

Theoretically, our interest is in empirically examining sociological claims about risk made by (e.g.) Beck, Giddens and Luhmann. To do this, we rely on *Systemic Functional Linguistics* (e.g. Halliday & Matthiessen, 2004), with particular focus on experiential meaning. Our report, which contextualises and elaborates on these results, is available [as PDF](https://raw.githubusercontent.com/interrogator/risk/master/report/risk_report.pdf) and (bleeding-edge) [.tex source](https://github.com/interrogator/risk/blob/master/report/risk_report.tex). If you want to interrogate the corpus yourself, you are advised to clone the repository, which includes the parse trees, and use the provided functions within the IPython Notebook.

## Installation:

On OSX, [*Anaconda*](http://continuum.io/downloads) should contain all the necessary dependencies (*Python*, *IPython*, *matplotlib*, etc. For the dependency parsing, I was getting segfaults until upgrading lxml to version 3.4.2 with:

      sudo pip install lxml --upgrade

though you could probably try setting [*Beautiful Soup*](http://www.crummy.com/software/BeautifulSoup/) to use a different parser.

## IPython Notebook usability

When running the Notebook locally, a couple of IPython extensions come in very handy:

* First, you can use [this](https://github.com/minrk/ipython_extensions) to generate a floating table of contents that makes the Notebook much easier to navigate.
* Second, given that some of the code can take a while to process, it can be handy to have [browser-based notifications](https://github.com/sjpfenninger/ipython-extensions) when the kernel is no longer busy.

More elaborate installation info, alongside code, is available once you've got `risk.ipynb` up and running.

## Forthcoming:

* Host for dependency parses
* Parse tree visualisation
* (More) code used to build corpora
* (More) installation info
* Dedicated cloud host for data and IPython Notebook (so that you can play with the data without installing anything!)
