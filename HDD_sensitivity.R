library("foreign")

HDD_18<-read.dbf("India_20yr_18C.dbf")
HDD_20<-read.dbf("India_20yr_20C.dbf")
HDD_22<-read.dbf("India_20yr_22C.dbf")

HDD_18<-HDD_18[,4:11]
HDD_20<-HDD_20[,4:11]
HDD_22<-HDD_22[,4:11]

HDD_18<-colSums(HDD_18, na.rm=TRUE)
HDD_20<-colSums(HDD_20, na.rm=TRUE)
HDD_22<-colSums(HDD_22, na.rm=TRUE)

HDD_18_1<-data.frame(Temperature=rep(18,8),HDD=HDD_18,Calculation_method=c("mean","min","max","2_point"))
HDD_20_1<-data.frame(Temperature=rep(20,8),HDD=HDD_20,Calculation_method=c("mean","min","max","2_point"))
HDD_22_1<-data.frame(Temperature=rep(22,8),HDD=HDD_22,Calculation_method=c("mean","min","max","2_point"))

HDD_0<-rbind(HDD_18_1[1:4,],HDD_20_1[1:4,],HDD_22_1[1:4,])
HDD_0[,2]<-abs(HDD_0[,2])
HDD_pop<-rbind(HDD_18_1[5:8,],HDD_20_1[5:8,],HDD_22_1[5:8,])
HDD_pop[,2]<-abs(HDD_pop[,2])

graph_of_HDD<-ggplot(HDD_0,aes(Temperature,HDD,col=Calculation_method))+geom_point()+geom_line()
graph_of_HDDxpop<-ggplot(HDD_pop,aes(Temperature,HDD,col=Calculation_method))+geom_point()+geom_line()
