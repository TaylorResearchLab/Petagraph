#"9606.protein.links.full.v12.0.txt" can be otained from "https://string-db.org/cgi/download?sessionId=bn5fVmg5rBcg&species_text=Homo+sapiens"
library(stringr)
STG <- read.table("~/9606.protein.links.full.v12.0.txt", quote="\"", comment.char="")
STG <- unique(STG[-1,c(1:2,16)])
STG[,1]<-str_remove_all(STG[,1],"9606.")
STG[,2]<-str_remove_all(STG[,3],"9606.")
I<- t(t(match(do.call(paste, data.frame(STG[,1:2])), do.call(paste, data.frame(STG[,c(2,1)])))))
J <- I*0
I<-I[,c(1,1)]
I[,1]<-1:dim(I)[1]
J[which(as.numeric(I[,2])>as.numeric(I[,1])),1]<-1
STG <- STG[which(as.numeric(J)==1),]
STG <- STG[which(STR2[,3]>450),]
STG<-cbind(STG[,c(1,1)],STG[,c(2,3)])
STG[,2]<-"correlated_with"
colnames(STG)=c("subject","predicate","object","evidence_class")
