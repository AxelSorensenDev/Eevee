### Annotate slot and intent detection for a new language with Eevee

[back to main README](../README.md)

On this page we are going to describe how we can create a new evaluation set
for an already existing benchmark. More conretely, we will assume 
that we have an English dataset annotated for slot and
intent detection. We want to create a new evaluation dataset for these tasks
for Dutch.  The English dataset looks as follows:

```
# text = Is it going to rain today?
# intent = weather/find
# slots: 15:19:weather/attribute,20:25:datetime
1	Is	weather/find	O
2	it	weather/find	O
3	going	weather/find	O
4	to	weather/find	O
5	rain	weather/find	B-weather/attribute
6	today	weather/find	B-datetime
7	?	weather/find	O

```

And can be found in `docs/en.train.conll`. We also have raw data (i.e. not
annotated) for Dutch available in a `.txt` format. These are available in
`docs/nl.eval.txt`. 

## Creating the data configuration
After starting up the annotation tool, we import the English training file with 
gold annotations. This allows us to easily create an Eevee task configuration by
importing the labels. To do this, we click on the `import "Conll-like" file` button:

[![import-conll](docs/import-conll.png)]()

Now we add the slot detection task through clicking on the `add task +` button.
We have to:
* name the task
* pick the task-type (`span`)
* select the input column where the tool can read the input words, this can
  easily be identified in the data field on the bottom of the page: 1
* select the output column where the tool can write the annotation: 3
* we can now click import from column

[![slot-detection](docs/slot-detection.png)]()


For the intent detection task, the procedure is highly similar. Note that the
input column is the same, and the output column is now identified with a string:
[![slot-detection](docs/slot-detection.png)]()

## Importing the data
Now we can export the task configuration file, and either: 1) restart Eevee, and
load the task configuration and the Dutch data as txt file, or: 2) remove the current
data and load the Dutch data. In this tutorial we choose the second option.





