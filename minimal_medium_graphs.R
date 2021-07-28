library(reshape2)
library(ggplot2)
library(pheatmap)


################# Heatmap #########################

data<-read.csv("C:/Users/Sophia Santos/Desktop/comparison_medium.csv", sep=";", header=T)
rownames(data) = data[,1] #identificar as amostras com os dados da coluna 1
data = data[,-1]
data = as.matrix(data)

pheatmap(data, cutree_rows = 2, cutree_cols = 6)


################### Create BarPlot with Positive and Negative parts #########################

data<-read.csv("C:/Users/Sophia Santos/Desktop/Biomass_ori_vs_opt.csv", sep=";", header=T)
rownames(data) = data[,1] #identificar as amostras com os dados da coluna 1
data = data.frame(data)

data$colour <- ifelse(data$value < 0, "decrease","increase")
data$hjust <- ifelse(data$value > 0, 1.3, -0.3)

g = ggplot(data, aes (model_id, value,label="", hjust=hjust)) + geom_text(aes(y=0, colour=colour)) + geom_bar(stat = "identity", aes(fill = colour))
g + theme(axis.text.x = element_blank()) + labs(x = "Genome Scale Metabolic Models", y = "Differences to original (%)") + ggtitle("Objective function differences - Orginal vs Optimized")


################### Create area plot ##############################

data<-read.csv("C:/Users/Sophia Santos/Desktop/medium_optimization_data.csv", sep=";", header=T)

rownames(data) = data[,1] #identificar as amostras com os dados da coluna 1
data=as.data.frame(data)
data=data[,-1]

ggplot(data, aes(x= Model, y=Value, fill=Type, colour=Type)) + 
  geom_area(aes(colour=Type, fill=Type), alpha=0.3, position='identity')+
  scale_x_continuous(name="Genome Scale Metabolic Models")+
  scale_y_continuous(name="Number of Metabolites")+
  geom_line(aes(color=Type), size = 1)+
  theme_bw()
  