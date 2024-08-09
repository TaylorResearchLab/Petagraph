DNL4<-array("",c(1,3));for (i in 1:4) {D <- read.delim(paste("~/",DS[i,1],".txt",sep = ""));D<-D[,c(1:6,12)];
U<-array("",c(1,3));for (j in 1:dim(D)[1]) {u  <-paste("4DNL ",DS[i,1],".",D[j,1],".",D[j,2],"-",D[j,3],".",D[j,4],".",D[j,5],"-",D[j,6],sep = "");
us <- cbind(u,"loop_us_start",paste("HSCLO ",D[j,1],".",D[j,2]-999,"-",D[j,2],sep = ""));
ue <- cbind(u,"loop_us_end",paste("HSCLO ",D[j,1],".",D[j,3]-999,"-",D[j,3],sep = ""));
ds <- cbind(u,"loop_ds_start",paste("HSCLO ",D[j,4],".",D[j,5]-999,"-",D[j,5],sep = ""));
de <- cbind(u,"loop_ds_end",paste("HSCLO ",D[j,4],".",D[j,6]-999,"-",D[j,6],sep = ""));
anc<-rbind(us,ue,ds,de);U <-rbind(U,anc)};DNL4<-rbind(DNL4,U)}