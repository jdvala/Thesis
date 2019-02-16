# EUR-LEX Scrapper

The Parallel_Scrapper.py will download the most recent summaries from [EUR-LEX website](https://eur-lex.europa.eu/browse/summaries.html)

By default it will download *English* and *German* summaries into the same folder you run the file from. 

The data will be stored in same file seperated by **three newline charater --> '\n\n\n'**, so the parallelness is preserved.

```python
with open(file_path, 'r') as readfilehandle:
  content = readfilehandle.read()

# and then split the content.

en_data = content.split('\n\n\n')[0]
de_data = content.split('\n\n\n')[1]

```
