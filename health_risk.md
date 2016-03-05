# Health risks in U.S. newspapers: a corpus linguistic approach

### [Daniel McDonald](mailto:mcdonaldd@unimelb.edu.au?Subject=IPython%20NYT%20ri
sk%20project), [Jens
Zinn](mailto:jzinn@unimelb.edu.au?Subject=IPython%20NYT%20risk%20project),
University of Melbourne

> This notebook builds on our earlier investigations:

1. Risk in the NYT
2. Risk in U.S. news

Previous literature and our pilot study both support the idea that health risks
are both particularly and increasingly prominent. We want to test that in our 60
million word U.S. print news corpus.

As in our previous investigation, we begin by importing *corpkit*, setting paths
to corpora, and the like.

```python
# show plots in this notebook
%matplotlib inline
import os

# import corpkit
from corpkit import interrogator, editor, plotter, conc

# some wordlists we'll use later
from dictionaries.process_types import processes
from dictionaries.wordlists import wordlists
from dictionaries.roles import roles

# for editing/combining results:
import pandas as pd
pd.options.display.max_rows = 30
pd.options.display.max_columns = 6
```

```python
nyt = 'data/NYT-parsed'
wsj = 'data/WSJ-parsed'
wap = 'data/WAP-parsed'
cht = 'data/CHT-parsed'
ust = 'data/UST-parsed'
tbt = 'data/TBT-parsed'
all_corpora = [nyt, wsj, wap, cht, ust, tbt]
```

```python
from corpkit import load_result
allwords = load_result('6_allwords_newest')
riskwords = load_result('6_riskwords_newest')
riskclasses = load_result('6_riskclasses_newest')
risktags = load_result('6_risktags_newest')
n_risk = load_result('6_n_risk')
risk_of = load_result('6_risk_of')
```

```python
riskword = r'(?i)\brisk'
```

Let's begin.

### Locating health risks

The simplest and most effective way of determining the extent to which risk and
health co-occur is to investigate the behaviour of *participants* in clauses.
More specifically,

1. The risk of something
2. The something risk

These can be defined using Tregex queries:

```python
# noun in NP in PP headed by of in NP headed by nominal risk
risk_of_query = r'/NN.?/ >># (NP > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))))'
risk_of = interrogator(corpora, 'words', risk_of_query, lemmatise = True,
        num_proc = 3,  quicksave = '6_risk_of')
```

```python
risk_of['CHT'].results[:10]
```

```python
n_risk_query = r'/NN.?/ !># NP > (NP <<# (/NN.?/ < /(?i).?\brisk.?/))'
n_risk = interrogator(corpora, 'words', n_risk_query, lemmatise = True,
        num_proc = 3,  quicksave = '6_n_risk')
```

```python
n_risk['WAP'].results[:10]
```

As in our last investigation, we can define a few helper functions to collapse
distinctions betwee newspapers, years and entries:

```python
def collapsed(interrogation):
    """collapse distinction between newspapers"""
    import pandas as pd
    interroformat = False
    if type(interrogation.values()[0]) == pd.core.frame.DataFrame:
        dat = interrogation.values()[0]
    else:
        dat = interrogation.values()[0].results
        interroformat = True
    order = list(dat.columns)
    for i in interrogation.values()[1:]:
        if interroformat:
            dat = dat.add(i.results, fill_value = 0)
        else:
            dat = dat.add(i, fill_value = 0)
    return dat[order]


def entry_across_corpora(result_dict, entry_name, regex = False):
    """get a single entry as a dataframe"""
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

With these interrogations and functions, we have everything we need to do some
visualisation.

```python
rel_coll = editor(collapsed(risk_of), '%', 'self', print_info = False)
inc_rel_coll = editor(collapsed(risk_of), '%', 'self', sort_by = 'increase', print_info = False)
dec_rel_coll = editor(collapsed(risk_of), '%', 'self', sort_by = 'decrease', print_info = False)

plotter('Risk of \emph{noun}', rel_coll.results)
plotter('Risk of \emph{noun}, increasing', inc_rel_coll.results)
plotter('Risk of \emph{noun}, decreasing', dec_rel_coll.results)
```

What jumps out here, of course, is the *risk of attack*, which rises quickly in
popularity at the turn of the millenium. Let's look at this result across
newspapers:

```python
attack = entry_across_corpora(risk_of, 'attack')
attack[:10]
```

```python
rel_attack = editor(attack, '%', get_totals(risk_of), print_info = False)
plotter('Risk of attack', rel_attack.results, subplots = True, layout = (2,3), figsize = (9,6), save = 'rattack')
```

... but, it's not what you think. While it's perhaps only natural that we assume
that this construction occurs in the context of terrorism, closer inspection
shows us something different:

```python
r_of_attack = r'NP <<# (/NN.?/ < /(?i)\battack/) > (PP <<# /(?i)of/ > (NP <<# (/NN.?/ < /(?i).?\brisk.?/)))'
lines = conc(os.path.join(wap, '2004'), 't', r_of_attack, print_output = False, random = True)
lines[['l', 'm', 'r']]
```

```python

```

Risk patterns with health topics much more than we seem to assume it does. In
fact, if we do two searches, for *risk of heart attack* and *risk of terror
attack*, we can measure the difference:

```python

```

```python

```

```python

```

```python
rel_coll = editor(collapsed(n_risk), '%', 'self', print_info = False)
plotter('\emph{Noun} risk', rel_coll.results)
```



The important thing to note is that these two categories have overlap, but are
not grammatically interchangable. You can say "the risk of cancer" or "the
cancer risk", but you can't say "the risk of health".

Semantically, only the *negative outcome* can occur in both positions: the
*risked thing* can only occur before the risk.

Fortunately for us, it's unambiguous whether or not a word is the *negative
outcome* or the *risked thing*. Furthermore, we can apply grammatical tests to
be certain:

> 1a. I risked my life

> 1b. I risked losing my life

> 2a. I risked death

> 2b. * I risked losing death

So, let's make a simple list:

```python

```

```python
riskedthing = ['life', 'everything', 'money', 'career', 'health', 'lot',
               'reputation', 'capital', 'future', 'job', 'safety', 'credit', 'currency',
               'possibility', 'anything', 'return', 'neck', 'nothing']
```

```python

```

```python

```

Let's combine the two results (knowing full well that they aren't perfect
equivalents):

```python
riskthings = {}
for name, data in risk_of.items():
    df = data.results.add(n_risk[name].results, fill_value = 0)
    df.ix['total'] = df.sum()
    df = df.T.sort('total', ascending = False).T
    df = df.drop('total', axis = 0)
    riskthings[name] = df
```

```python
#collapsed(riskthings)

rel_coll = editor(collapsed(riskthings), '%', 'self')
plotter('Risk of \emph{noun}\slash \emph{noun} risk', rel_coll.results)
```

```python

```

```python

```

We can define some fairly unambiguous wordlists, too:

```python
cats = {'Health': ['cancer', 'health', 'attack', 'disease', 'death', 'infection', 'heart', 'stroke', 'injury',  
          'smoking', 'clot', 'complication', 'heart-attack', 'diabetes', 'fracture', 'drug',  'bleeding', 
          'suicide', 'contagion', 'mortality', 'illness', 'aid', 'breast', 'miscarriage',  'dementia', 
          'radiation', 'surgery', 'life', 'depression', 'osteoporosis', 'pregnancy', 'breast-cancer', 
          'birth', 'disorder', 'leukemia'],
        'Finance': ['credit', 'inflation', 'default', 'market', 'currency', 'investment', 'interest-rate', 'recession', 
           'business', 'deflation', 'price', 'return', 'litigation', 'rate', 'cost', 'loan', 'counterparty', 
           'trading', 'portfolio', 'stock', 'liability', 'prepayment', 'fund', 'bond', 'growth', 'asset', 
           'decline', 'liquidity', 'lending', 'volatility', 'bank', 'fraud', 'insurance', 'mortgage', 'rollover', 
           'company', 'accident', 'debt', 'interest', 'bankruptcy', 'slowdown', 'expense', 
           'collapse', 'foreign-exchange', 'deal', 'downturn', 'transmission', 
           'foreclosure', 'exchange-rate', 'exchange', 'bubble', 'derivative', 
           'stock-market', 'devaluation', 'capital', 'pressure', 'downgrade', 
           'fluctuation', 'investor', 'crash', 'taxpayer', 'economy', 'investing', 'dollar', 
           'tax', 'national-security', 'equity', 'trade', 'transaction', 'money', 'career', 
           'executive', 'industry', 'run', 'insolvency', 'underwriting', 'claim', 'settlement']}

uncategorised = [u'downside', 'security', 'loss', 'benefit', 'safety', 'failure', 'problem', 'reward', 'event', 
                 'war', 'flight', 'damage', 'effect', 'course', 'exposure', 'fire', 'country', 'policy', 'control', 
                 'execution', 'u.s', 'increase', 'crisis', 'terrorism', 'defect', 'harm', 'uncertainty', 
                 'lifetime', 'strategy', 'product', 'change', 'recurrence', 'conflict', 'lawsuit', 'contamination', 
                 'government', 'development', 'disruption', 'move', 'opportunity', 'action', 'violence', 'error', 
                 'mr', 'theft', 'use', 'type', 'inventory', 'treatment', 'explosion', 'proliferation', 'headline', 
                 'behavior', 'project', 'material', 'risk', 'china', 'delay', 'weakness', 'abuse', 'earthquake', 
                 'backlash', 'flooding', 'correction', 'approach', 'integration', 'strike', 'reaction', 'collision', 
                 'spill', 'program', 'casualty', 'shock', 'system', 'hurricane', 'flood', 'challenge', 'instability', 
                 'longevity', 'activity', 'catastrophe', 'overheating', 'issue', 'disaster', 'cut', 'property', 
                 'meltdown']
```

```python
#get_totals(risk_of)
comp_n_risk = editor(n_risk, merge_entries = cats, just_entries = cats.keys())
```

```python

```

```python
rel_tot = editor(collapsed(comp_risk_of), '%', get_totals(risk_of), 
                 use_df2_totals = True, sort_by = 'total')
plotter('Health and financial risks', rel_tot.results, style = 'seaborn-notebook')
```

Breaking this down by publication, we can expect to see more financially
oriented newspapers focussing more on financial risks:

```python
rel_comp_risk_of = editor(risk_of, '%', risk_of, use_df2_totals = True, \
                      merge_entries = cats, just_entries = cats.keys(), print_info = False)
for name, data in rel_comp_risk_of.items():
    plotter('Health and financial risk in the %s' % name, data.results, 
            style = 'seaborn-notebook', figsize = (6, 3), legend_pos = 'upper right')
```

```python

```

```python

```
