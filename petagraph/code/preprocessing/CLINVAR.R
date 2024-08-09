# Requires the latest variant_summary.txt from the ClinVar website at NCBI
library(stringr)
VS <- read.delim("~/Path/variant_summary.txt", header=FALSE, comment.char="#")
VS<-unique(VS[,c(6,7,13,25)])
VS<-VS[str_which(VS[,2],'pathogenic'),]
VS<-VS[-str_which(VS[,2],'uncertain'),]
VS<-VS[-str_which(VS[,2],'conflicting'),]
VS<-VS[-which(VS[,4]=='no assertion criteria provided'),]
VS[,3]<-str_replace_all(VS[,3],'\\|',',')
VS[,3]<-str_replace_all(VS[,3],';',',')
V<-strsplit(VS[,3],',')
VR<-array("",c(1,2))
for (i in 1:length(V)){v<-V[[i]];l<-length(v);u<-array(VS[i,1],c(l,2));u[,2]<-v;VR<-rbind(u,VR)}
VR<-unique(VR)
VR<-VR[-which(VR[,2]==""),]
VR<-VR[-str_which(VR[,2],'condition'),]
VR<-VR[-which(VR[,2]=='-'),]
VR<-VR[-which(VR[,1]=='-'),]
VR[,2]<-str_remove_all(VR[,2],'Human Phenotype Ontology:')
VR[,2]<-str_replace_all(VR[,2],'MONDO:MONDO:','MONDO:')
rm(VS,VR,u,v,i)
ClinVar_Edgelist<-cbind(VR,array('gene_assoicated_with_disease_or_phenotype',c(dim(VR)[1],1)))
colnames(ClinVar_Edgelist)<-c('subject','object','predicate')