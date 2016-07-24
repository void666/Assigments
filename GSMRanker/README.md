# GSMRanker
Extractor from gsmarena.com for mobile data for each available phone and saves as JSON file. 

### Working:
  - Extracts links for all brands from gsmarena.com/makers.php3
  - Iteratively calls all the links extracted from the above page and extracts the links to all phones for all brands mentioned
  - Iteratively calls individual phone links and extracts the data (name, phone img url, ram, memory,battery,camera) and saves list of such phone objects in JSON format.

### Completed:
  - Data Extractor
  - File Write to JSON

### To-do:
  - Create UI in Angular JS to read the JSON data
  - Create rules for retriving data based on user input and preferences. 

### Test
run of main.py gives the following output and json file:
   - Console Output :  https://gist.github.com/void666/7c4c40b596536edec20b4e661a0b9dc7 
   - Output file (data.json) : https://gist.github.com/void666/94d3ee5f130d36755b39504bfe3a7152

### Libraries used :
   - BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/)
   - Requests for Humans (http://docs.python-requests.org/en/master/)
   - json (https://docs.python.org/2/library/json.html)

