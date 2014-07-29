## To-Do List
######(Updated: July 24)

#### Details:

* [X] Make it so that JSON written to database stores the data necessary for rendering the positive/negative display on webapp
* [X] Make it so that sentence objects in JSON store their probability of pos/neg
	* Will sort by this / filter low-confidence examples in the front end display 
* Figure out a good way to **bold** the aspect in the sentence
	* Ask Ryan/Jon how to do this

#### Must-Dos:

* Figure out how to deploy to EC2
* Populate full DB
* [X] Improve sentiment analysis

#### Nice-to-Haves:
	
* Create a fancier summary of the comments about an aspect
* Make the aspect-browsing UI more intuitive
	*  Hide/unhide the individual sentences??
	
### TODAY:

1. Update my info online
	* be sure to update github repo address. 
	* Update name of project & description. Match with resume.  
	
2. Fix bug with get_sents_by_asect (or sent.has_aspect) ==> retrieve using tokenized version or something--not raw string form… 

3. Finish up front-end stuff. Render the new information that I have... 

#### De-embarassement techniques
* Don't display really long 	sentences…
* But be careful about doing too much filtering --> this is what's leading to the empty aspects. Need to at least check at the end of filtering to see if there is still enough stuff left to display
* Filter aspects that are close to or contain the restaurant's name??
* Maybe filter sentences with multiple aspects?
* More aspect stop-words: 
"way", "minutes"(?)
* Maybe make the aspect-extraction a little more stringent??

ABSOLUTELY NEED TO DO sentence_by_aspect retrieval by TOKENS. otherwise "waiter" gets retrieved for wait

Same thing with "way" and "always"

#### Deploying: 

* A Record => point to publice EC2 IP
* CNAME
* Alias (URL Redirect)


**Y**elp S**um**marization **M**iner


