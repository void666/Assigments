# Simple ranking based search implementation

Program reads a list of strings from a file (input.txt), having pages and queries
and returns the relevant pages with words from each query in order of thier weigtage.

Code is commented describing relevance of each component and why it is being used

### Assumptions made
  - In case the weightage of two pages are same, the one that has a lower index is printed first. eg : p7- 32, p6-32, Output is : p6,p7
  - If there exists duplicate words in the pages, the weightage is given to the first occurence of the word.
  - Same words in lower case and upper case are considered as different words.
  - Input is read from a file (input.txt)
  - output is done on console.

### Keypoints 
  - Taken special measures to dynamically assign weightag variable, avoiding constant assigment, which could have resulted in wrong weightage calculation.
  - taken measures for avoiding repeatitive searching of same page.
  - optimised whereever possible.

### Test case
  - input : input.txt
  - output : https://gist.github.com/void666/b4186ae11136f33873d579bd72a7018e
