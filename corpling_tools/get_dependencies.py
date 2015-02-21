#!/usr/local/bin/python

#   Building scripts: make corpus of just collapsed dependencies
#   for ResBaz NLTK stream
#   Author: Daniel McDonald

def get_dependencies(path, newpath):
    """get just the collapsed dep xml from a corpus with annual subcorpora"""
    import os
    from bs4 import BeautifulSoup
    sorted_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    sorted_dirs.sort(key=int)
    for d in sorted_dirs:
        print 'Doing ' + d + ' ...'
        new_subcorpus_directory = os.path.join(newpath, d)
        if not os.path.exists(new_subcorpus_directory):
            os.makedirs(new_subcorpus_directory)
        filelist = os.listdir(os.path.join(path, d))
        for f in filelist:
            bits_to_keep = []
            with open(os.path.join(path, d, f), "r") as text:
                data = text.read()
                soup = BeautifulSoup(data)
                for dep_elem in soup.find_all('dependencies'):
                    deptype = dep_elem.attrs.get('type')
                    # get just collapsed
                    if deptype == 'collapsed-ccprocessed-dependencies':
                        bits_to_keep.append(dep_elem)
            with open(os.path.join(newpath, d, 'dependencies.xml'), "a") as newfile:
                for bit in bits_to_keep:
                    newfile.write(str(bit))        

print 'Doing politics ... '
get_dependencies("../data/nyt/politics", "../data/only_dep/politics")
print 'Doing health ... '
get_dependencies("../data/nyt/health", "../data/only_dep/health")
print 'Doing years ... '
get_dependencies("../data/nyt/years", "../data/only_dep/years")
print 'Doing economics ... '
get_dependencies("../data/nyt/economics", "../data/only_dep/economics")