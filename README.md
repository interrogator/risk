## Discourse-semantics of risk in the *New York Times*, 1963&ndash;2014: a corpus linguistic approach

This repository contains much of what was created for our longitudinal analysis of risk language in the *New York Times*. The investigation involves systematic analysis of over 150,000 NYT paragraphs containing a risk token (*risk*, *risking*, *at-risk*, *risk-to-reward*, *risk-laden*, etc), though the tools and functions could easily be used with other datasets. These paragraphs have been parsed with *Stanford CoreNLP*, and are interrogated using [`corpkit`](https://github.com/interrogator/corpkit), which was developed for this project.

Our *IPython Notebook* presents the code used in our analysis side-by-side with our results. It can be viewed via *nbviewer* [here](http://nbviewer.ipython.org/github/interrogator/risk/blob/master/risk.ipynb). Basically, we were interrogating the corpus for lexicogrammatical features of risk, and looking for sites of change. Here are a few examples, made using `corpkit`'s `interrogator()` and `plotter()` functions:


<img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/risk_processes-2.png" />
<br>

<img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/risk-and-power-2.png" />
<br>

<img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/pie-chart-of-common-modals-in-the-nyt.png" />
<br>

<img style="float:left" src="https://raw.githubusercontent.com/interrogator/risk/master/images/types-of-risk-modifiers.png" />
<br>

Theoretically, our interest is in empirically examining sociological claims about risk made by (e.g.) Beck, Giddens and Luhmann. To do this, we rely on *Systemic Functional Linguistics* (e.g. Halliday & Matthiessen, 2004), with particular focus on experiential meaning. Our report, which contextualises and elaborates on these results, is available [as PDF](https://raw.githubusercontent.com/interrogator/risk/master/report/risk_report.pdf) and (bleeding-edge) [.tex source](https://github.com/interrogator/risk/blob/master/report/risk_report.tex).

If you want to download and interrogate the corpus yourself, read on.

## Getting the data and Notebook

Once you've got [IPython](http://ipython.org/install.html) (`pip install ipython` should do it for non-Windows users), you should downlad the contents of this repository. Either download and unzip via 'Download ZIP', or clone the repository with:

```shell
git clone https://github.com/interrogator/risk.git
```

Then, change into the project directory and start the IPython Notebook:

```shell
cd risk
# or, cd risk-master if you downloaded the .zip
ipython notebook risk.ipynb
```

The first few cells in the notebook will then help you:

1. install and import `corpkit`
2. unzip corpus data

The remainder of the notebook demonstrates our methods and findings, which you can freely manipulate if you like.

## IPython Notebook usability

When running the Notebook locally, a couple of IPython extensions come in very handy:

* First, you can use [this](https://github.com/minrk/ipython_extensions) to generate a floating table of contents that makes the Notebook much easier to navigate.
* Second, given that some of the code can take a while to process, it can be handy to have [browser-based notifications](https://github.com/sjpfenninger/ipython-extensions) when the kernel is no longer busy.

More elaborate installation info, alongside code, is available once you've got `risk.ipynb` up and running.

## Forthcoming:

* Host for corpus dependencies
* Code used to build corpora
* Dedicated cloud host for data and IPython Notebook (so that you can play with the data without installing anything!)
