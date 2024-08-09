#L1000 edgelist data is required and can be obtained from https://maayanlab.cloud/Harmonizome/resource/LINCS+L1000+Connectivity+Map
L1000 <- read.delim("~/L1000.txt")
L1000<-as.data.frame(L1000)
Target<-strsplit(L1000$target,"_")
Drugs <-array("",c(length(Target),1))
for (i in 1:length(Target)) {v<-Target[[i]];Drugs[i,]<-v[1]}
L1000<-cbind(L1000$source,Drugs,L1000$weight)
Small_Molecules<-read.csv("SM.csv")
colnames(L1000)<-c("subject","object","predicate")
colnames(Small_Molecules)<-c("object","pubchem_cid")
L1000<-merge(L1000,Small_Molecules,by = "object")
L1000<-L1000[,c(4,3,2)]
colnames(L1000)<-c("subject","predicate","object")
L1000[which(as.numeric(L1000$predicate)==1),2]<-"positively_correlated_with_gene"
L1000[which(as.numeric(L1000$predicate)==-1),2]<-"negatively_correlated_with_gene"
L1000$subject<-paste("PUBCHEM",L1000$subject)
L1000 <- unique(L1000)