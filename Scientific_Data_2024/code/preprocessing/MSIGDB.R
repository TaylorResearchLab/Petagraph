library('msigdbr')
library('stringr')
C1 <- msigdbr(species = 'human', category = 'C1');C1 <- as.data.frame(C1[,c(3,2,7)])
C2 <- msigdbr(species = 'human', category = 'C2');C2 <- as.data.frame(C2[,c(3,2,7)])
C2<-C2[-str_which(C2[,1],'KEGG'),]
C3 <- msigdbr(species = 'human', category = 'C3');C3 <- as.data.frame(C3[,c(3,2,7)])
C8 <- msigdbr(species = 'human', category = 'C8');C8 <- as.data.frame(C8[,c(3,2,7)])
H <- msigdbr(species = 'human', category = 'H');H <- as.data.frame(H[,c(3,2,7)])
C1[,2]<-'chr_band_contains_gene'
C2[,2]<-'pathway_associated_with_gene'
C3[,2]<-'targets_expression_of_gene'
C8[,2]<-'has_marker_gene'
H[,2]<-'has_signature_gene'
MSIGDB<-unique(rbind(C1,C2,C3,C8,H))
colnames(MSIGDB)<-c('subject','predicate','object')