#This script needs "GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt" and "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct"
#Those files can be otained from "https://gtexportal.org/home/downloads/adult-gtex/metadata" and 
#"https://gtexportal.org/home/downloads/adult-gtex/bulk_tissue_expression" respectively
ATR <- read.delim("~/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt", header=FALSE)
GTX <- read.delim("~/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct", header=FALSE, comment.char="#")
Genes<-GTX[3:dim(GTX)[1],1:2]
colnames(GTX)<-GTX[2,]
GTX<-GTX[3:dim(GTX)[1],3:dim(GTX)[2]]
GS <- ATR[-1,c(1,7)]
obsv <- t(t(colnames(GTX)))
obsv <- obsv[,c(1,1)]
obsv[,2] <- match(obsv[,1],GS[,1])
obsv[,2] <- GS[obsv[,2],2]
Tissues <- t(t(sort(unique(obsv[,2]))))
for (i in 1:length(Tissues)) {I <- which(obsv[,2]==Tissues[i,1]);D <- GTX[,I];C <- cor(t(D));diag(C)=0;L <- t(t(which(C>=0.99)))}
l = dim(C)[1];
L = cbind(L,array("",c(length(L),5)));
L[,2] = round(ceiling(L[,1]/l));
L[,3] = L[,1]%%l;L[which(L[,3]==0),3] = l;
L[,4] = paste("coexpression_",Tissues[i,1],sep = "");
L[,5] = Genes[L[,2],2];
L[,6] = Genes[L[,3],2]
