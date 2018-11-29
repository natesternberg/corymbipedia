*Corymbipedia* is tool that generates random, fanciful semantic clusters of words using glove vectors. A *corymbus* is a Latin term for a cluster of flowers or fruits; the -pedia suffix refers to the fact that the output feels like reading through some sort of thesaurus-like reference book.

[Glove vectors](https://nlp.stanford.edu/projects/glove/) are a neat example of raw quantity yielding quality. The authors calculated co-occurrence frequencies over 6 billion words and used dimensionality reduction to collapse the results into 50-dimensional vectors, one per word. That yields a small enough data set (171MB) that you can reasonably download it, but still so precise that you can actually do analogical reasoning via vector arithmetic: the famous example is that if you take the 50-dimensional vector for “queen”, subtract the vector for “woman” and add the vector for “man”, the resulting vector’s closest neighbor is “king”.

I learned about these at a research talk, and on the way home it occurred to me that since the words were expressed as vectors, you could run a clustering algorithm on them. What would happen if you tried that? Would you get, e.g., one cluster for colors, one for days of the week, one for state capitals, one for marsupials?
 
The answer is, yes! The resulting clusters group by all sorts of crazy categories whose similarities just fall out of the math, but whose semantic connections are obvious to a human reader:

|Category|Words|
|--|--|
|Naval accidents| 'capsized', 'collided', 'sinking', 'sank', 'boat', 'aground', 'freighter', 'crashed', 'tanker', 'collision'|
|Public scandals|'accuser', 'simpson', 'lewinsky', 'o.j.', 'molestation', 'fuhrman', 'affair', 'juror', 'intern', 'berenson'|
|Russian surnames|'dmitri', 'andrei', 'alexei', 'nikolai', 'igor', 'vyacheslav', 'aleksandr', 'pavel', 'petrov', 'oleg'|
|Energy production|'hydroelectric', 'pipeline', 'hydropower', 'coal', 'geothermal', 'gas', 'liquefied', 'onshore', 'hydro', 'refinery'|
|Rhetorical insults|'idiotic', 'illogical', 'inexcusable', 'foolishness', 'disgraceful', 'contemptible', 'ludicrous', 'repugnant', 'unconscionable', 'inexplicable'|
|Fruit|'cherries', 'mango', 'strawberries', 'pineapple', 'peaches', 'raisins', 'pomegranate', 'apples', 'tomato', 'pear'|
|Despotic governments|'imperialist', 'totalitarian', 'tyrannical', 'bloodthirsty', 'dictators', 'oppressors', 'imperialistic', 'expansionism', 'reactionary', 'despotic'|
|Movie characters|'scooby-doo', 'tarzan', 'shrek', 'lassie', 'prequel', 'porky', 'looney', 'terminator', 'hobbit', 'daffy'|
|Singers|'mariah', 'manilow', 'barbra', 'iggy', 'jimi', 'aretha', 'jagger', 'hendrix', 'alanis', 'streisand'|
|Organized crime|'gangsters', 'mafia', 'mobsters', 'gangs', 'yakuza', 'underworld', 'vigilante', 'mob', 'gang', 'thugs'|
|Architecture|'rococo', 'modernistic', 'neo-gothic', 'neo-renaissance', 'neo-baroque', 'red-brick', 'art-deco', 'half-timbered', 'neoclassic', 'brutalist'|
|Rhymes from country/western songs?|'wishin', 'stealin', 'boppin', 'laughin', 'shinin', 'hustlin', 'coolin', 'stylin', 'al-ta', 'sche'|


I find reading these clusters strangely compelling, like paging through an new variety of reference book.  As a bonus, the clustering algorithm uses a random seed to pick the location of the initial cluster centroids, which has the side effect of producing different clusters with each run.

**Usage:**

The script takes three parameters: 
* The file name of the glove vector file (which you can download [here](https://nlp.stanford.edu/projects/glove/)).
* The number of clusters to create (1000 is a good starting point).
* The number of words to read from the glove vector file.  The words appear in descending order of frequency (from "the" to "sandberger"), so the more you read, the obscurer the clusters become (and the slower the algorithm runs).  This can produce some weird, erudite clusters, like: ['eleutherodactylus', 'elachista', 'phyllonorycter', 'hyposmocoma', 'stigmella', 'scopula', 'coleophora', 'eupithecia', 'gerbil', 'mordellistena'] (mostly types of moths).

The output is ordered by "tightness" of the cluster, that is, clusters with the lowest average distance from the words to the cluster centroid come first.  The tightest are usually 'pathological' cases, like clusters of numbers (like ['1878', '1876', '1881', '1877', '1882', '1879', '1869', '1898', '1859', '1871'])...but sometimes they're just words that always occur together (['tristan', 'isolde'], or ['mea', 'culpa']).