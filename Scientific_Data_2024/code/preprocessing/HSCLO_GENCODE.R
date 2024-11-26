#THis scripts creates GENCODE mapping of transcript and genes found in Petgraph to HSCLO nodes at 1kbp resolution
for (i in 1:295559) {l <- floor(as.numeric(G[i,2])/1000)*1000; 
if (G[i,2]>l) {L[i,3] = paste("HSCLO"," ",G[i,6],".",l+1,"-",l+1000,sep = "")} else {L[i,3] = paste("HSCLO"," ",G[i,6],".",l-999,"-",l,sep = "")}}
