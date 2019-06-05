library(ggplot2)
library(rjson) 
library(lubridate)
library(scales)

setwd('/home/akara/.task/')
tasks <- fromJSON(file = "tasks.json") 


atts  <- c()
for (task in tasks) {
	atts  <- append(atts, names(task))
}
cols  <- unique(atts) # the name of every possible attributes among the tasks

task.lead  <- tasks[[1]]
memb  <- cols %in% names(task.lead)
miss  <- cols[!memb]
task.lead2 <- vector(mode = "character", length = length(miss)) 
names(task.lead2) <- miss
tasks.df  <- data.frame(append(task.lead,task.lead2))
tasks.df$annotations <- I(list(tasks.df$annotations))
tasks.df$tags <- I(list(tasks.df$tags))

for (task in 1:length(tasks[-1])) {
	task  <- tasks[[task]]
	tags <- task$tags  #tags and annotations can have multiple entries
	ann <- task$annotations
	task$tags <- NULL 
	task$annotations <- NULL
	memb  <- cols %in% names(task)
	miss  <- cols[!memb]
	task2 <- vector(mode = "character", length = length(miss)) 
	names(task2) <- miss
	task3  <- data.frame(append(task,task2))
	if (length(tags)>0) {
		task3$tags=I(list(tags))
	}
	if (length(ann)>0) {
		task3$annotations=ann
	}
	tasks.df  <- rbind(tasks.df,task3)
}


date <- na.omit(ymd(substring(tasks.df$end, 1, 8)))
label <- as.factor("Done")
endings <- data.frame(date, label)
date <- na.omit(ymd(substring(tasks.df$entry, 1, 8)))
label <- as.factor("Added")
entries <- data.frame(date, label)
events <- rbind(endings, entries)

featsum <- ggplot(events, aes(date, fill=label)) +
	geom_histogram(binwidth=1) +
	theme(plot.title = element_text(hjust = .5), legend.title = element_blank()) +
	labs(title = 'All Recorded Task Addition and Completion', x='Date',y='Count')

ggsave('/home/akara/Dropbox/spatialawareness/images/TaskSummaryForever.png',featsum,width=7,height=2.5,units='in') 

last30  <- interval(today() - days(30), today())
events.recent <- events[events$date %within% last30,]
featsum30 <- ggplot(events.recent, aes(date, fill=label)) +
	geom_histogram(binwidth=1) +
	theme(plot.title = element_text(hjust = .5), legend.title = element_blank()) +
	labs(title = 'Recent Task Addition and Completion', x='Date',y='Count')

ggsave('/home/akara/Dropbox/spatialawareness/images/TaskSummary30Days.png', featsum30,width=7,height=2.5,units='in') 

