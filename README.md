# MODALIZER: The Use of Modals in Debates and Dialogue

Count the number of modals for each person participating in the dialogue.

## Introduction
In the past few years political debates have become much more heated and further fuel the polarization of the left and right. Different fields of linguistics can help analyze these debates, for example through investigating the use of modal verbs (i.e. modality) between the participants (Dunmire 2007). 

However, finding modals can be a laborious task, since they include a large variety of different forms (e.g. _will_ alone can occur as _will, 'll, won't_). Furthermore, the question of _how_ to classify modals is also disputed since the boundaries of what a modal can or cannot indicate are fuzzy. 

This program helps to take a first step of both finding and categorizing the modals quickly, so that a more fine-grained (re)analysis is possible later on. 

## Installation
Install this package using [poetry](https://python-poetry.org/docs/#installation) by running 

    poetry install

## Usage
Assuming that the data/file is in the format described in the **Data** section and your current directory is in the outer _modalizer_ folder, you can call the number of modals (raw and relative frequencies) as follows:

    python3 modalizer/main.py data/presidential_debate1.txt

To receive an example for every modal lemma a person used, you can indicate the optional --example or -e flag:

    python3 modalizer/main.py data/presidential_debate1.txt -e

To categorize the modals and receive a word count and percentage for every category, you can indicate the optional --categorize or -c flag:

    python3 python3 modalizer/main.py data/presidential_debate1.txt -c

It is also possible to call both flags at the same time:

    python3 modalizer/main.py data/presidential_debate1.txt -e -c

For further options use the --help or -h flag: 

    python3 modalizer/main.py data/presidential_debate1.txt -h

## Data
The `data` directory contains 3 different presidential debate files, all around 300 lines long. This data was taken from the NewYorkTimes debate transcripts:

* The first debate: https://www.nytimes.com/2016/09/27/us/politics/transcript-debate.html
* The second debate: https://www.nytimes.com/2016/10/10/us/politics/transcript-second-debate.html
* The third debate: 
https://www.nytimes.com/2016/10/20/us/politics/third-debate-transcript.html

Furthermore, the directory includes William Shakespeare's _Hamlet_ as an example for a slightly larger file (1117 lines). This was taken from the ProjectGutenberg website (https://www.gutenberg.org/ebooks/1524).

The required format for the data files is as follows:

    SPEAKER: Text

Each line must be headed by the speaker's name followed by a colon. 

## Background
Classifying modals is not a black and white task, which is why the categorization implementation is based on multiple sources but also somewhat subjective. The categorization is mainly based on the following sources:

* Coates (1983)
* Huddleston & Pullum (2002)
* Palmer (2001)

The reason for using sources that are a bit older is that these papers (especially Coates and Palmer) are still considered to be some of the most influential works on modality.

## Comments
I am aware that the test for the modal classifier does not cover every possible grammatical variation. This would include a lot of background research and would in the end still be faulty. The most ideal implementation for a classification task such as this one would likely have been to train a classifier on a larger corpus. Especially in hamlet.txt there are some examples that are not classified correctly / that are not covered by my implementation. This is primarily because it is an old text where modality is not used the same way as in modern English.

I have included implementations to measure the time and memory usage of the program.

## References
Coates, J. (1983). The Semantics of Modal Auxiliaries. London: Croom Helm.

Dunmire, P. L. (2007). The use of modals in political discourse: A cross-linguistic perspective. John Benjamins Publishing. 

Huddleston, R. & Pullum, G. K. (2002). The Cambridge Grammar of the English Language. Cambridge: Cambridge University Press.

Palmer, F.R. (2001). Mood and Modality. Cambridge: Cambridge University Press. 
