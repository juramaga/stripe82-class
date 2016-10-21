rm(list=ls())

## read in source catalog
dat <- read.table("stripe82candidateVar_v1.1.dat")
col.names <- c("ID","ra","dec","P","r","ug","gr","ri","iz","gN","gAmpl","rN","rAmpl","iN","iAmpl","zQSO","MiQSO")
colnames(dat) <- col.names
dat$class <- "unknown" ## initial classification

## qsos have zQSO!=-9.9
dat$class[dat$zQSO!=-9.9] <- "QSO"

## RR Lyrae were identified by sesar
rrlyrae <- read.table("apj326724t2_mrt.txt",skip=42)
rrlyrae <- rrlyrae[,1:2]
rrlyrae[,2] <- paste0("rr_",rrlyrae[,2])
names(rrlyrae) <- c("ID","classrr")
mean(rrlyrae$ID %in% dat$ID) ## PROBLEM: not all rrlyrae IDs are in dat
rrlyrae <- rrlyrae[rrlyrae$ID %in% dat$ID,] ## SOLUTION: get rid of these RR lyrae ids
dat <- merge(dat,rrlyrae,all=TRUE)
dat$class[!is.na(dat$classrr)] <- dat$classrr[!is.na(dat$classrr)]
dat$classrr <- NULL

## eclipsing binary sources
