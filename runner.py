import os
from articles import Article
from cluster import cluster
from cluster import average_relation
from cluster import group_sentences
from cluster import common_keywords
from utils import vectorize_text
from utils import split_sentences

CUTOFF = 0.55

articles = []
for file in os.listdir("articles/"):
    if file.endswith(".txt"):
    	text = open(os.path.join("articles/", file), "r").read()
    	source = file[:file.index("-")]
        articles.append(Article(text, source))
groups = cluster(articles)
num_groups = max(groups) + 1
groupings = [[] for _ in range(num_groups)]
for i in range(len(groups)):
	group_num = groups[i]
	article = articles[i]
	groupings[group_num].append(article)

correlations = []
for group in groupings:
	correlations.append((average_relation(group), len(group)))

i = len(correlations) - 1
while i >= 0:
	corr = correlations[i][0]
	if corr < CUTOFF:
		correlations.pop(i)
		groupings.pop(i)
	i -= 1

i = len(groupings) - 1
while i >= 0:
	group = groupings[i]
	if len(group) <= 1:
		correlations.pop(i)
		groupings.pop(i)
	i -= 1

processed_articles = []
text = []
for gr in groupings:
	scoring = group_sentences(gr)
	common = common_keywords(gr)
	processed_articles.append((common, scoring))

for article in processed_articles:
	text_list = article[1]
	temp = ""
	for sentence in text_list:
		sentence = sentence[0]
		if len(sentence) != 0:
			if sentence[0] == ".":
				sentence = sentence[2:]
			temp += sentence + " "
	text.append(temp)

i = 0
while i < len(text):
	article = text[i]
	fw = open("output_articles/" + str(correlations[i][0]) + ".txt", "w")
	fw.write(article)
	fw.flush()
	i += 1