# A CYK based parser

A basic implementation a parser based on the CYK algorithm. This code can be used to understand how to use the CYK  algorithm to obtain a parse tree and eventually to develop a more complex parser. The result of the analyzis is a ParseTree object.

# Usage
Run the following command in a terminal with python 3 installed:

`python3 src/test.py <grammar_file> <sentence>`

Example: 
 
`python3 src/test.py data/grammar.cfg "I prefer the morning flight through Denver"`

The result should be as follows:

```
S
|--VP
|  |--NP
|  |  |--Nom
|  |  |  |--PP
|  |  |  |  |--NP
|  |  |  |  |  |--Pro
|  |  |  |  |     |--denver
|  |  |  |  |--P
|  |  |  |     |--through
|  |  |  |--Nom
|  |  |     |--Noun
|  |  |     |  |--flight
|  |  |     |--Nom
|  |  |        |--Noun
|  |  |           |--morning
|  |  |--Det
|  |     |--the
|  |--Verb
|     |--prefer
|--NP
   |--Pro
      |--i
```

