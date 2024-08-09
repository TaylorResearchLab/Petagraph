DNQ4<-array("",c(1,3));for (i in 1:4) {D <- read.delim(paste("~/",DS[i,1],".txt",sep = ""));D<-D[,c(1:6,12)];
U<-array("",c(dim(D)[1],3));for (j in 1:dim(D)[1]) {U[j,1]  <-paste("4DNL ",DS[i,1],".",D[j,1],".",D[j,2],"-",D[j,3],".",D[j,4],".",D[j,5],"-",D[j,6],sep = "");
U[j,2]<-"loop_has_qvalue_bin";U[j,3]<-paste("4DNQ ","1e",floor(log10(D[j,7])),".","1e",ceiling(log10(D[j,7])),sep = "")};DNQ4<-rbind(DNQ4,U)}
