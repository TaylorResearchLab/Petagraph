
#CMAP edgelist data is required and can be obtained from https://maayanlab.cloud/Harmonizome/resource/Connectivity+Map
CM <- read.delim("~/CMAP.txt")
CM<-cbind(CM$source,CM$target,CM$weight)
colnames(CM)<-c('subject','object','predicate')
CM <-as.data.frame(CM)
CM<-CM[-1,]
SM <-cbind(unique(CM[,2]),unique(CM[,2]))
SMS<-strsplit(SM[,1],'-')
for (i in 1:length(SMS)){v<-SMS[[i]];u<-v[1];l<-length(v);if (l>2) {for (j in 2:(l-1)){u<-paste(u,v[j],sep = '-')}};SM[i,2]<-u}
colnames(SM)<-c('object','object-')
CM<-merge(CM,SM,by = 'object')