library("ggplot2")
library("dplyr")
d = read.csv("AVHV_Main/output/AVHV_Traffic_Lights/av.csv")
d$car_name = as.factor(d$car_name)
ggplot(d, aes(x=car_name, y=speed)) + geom_point(aes(col=stopping_time, size=reaction_time)) 


y = d %>% filter(car_name == "GentleCar29")
y$id = 1:nrow(y)
ggplot(y, aes(x=id, y=speed)) + geom_point(aes(col=stopping_time, size=reaction_time)) 

y = d %>% filter(car_name == "GentleCar60")
y$id = 1:nrow(y)
ggplot(y, aes(x=id, y=speed)) + geom_point(aes(col=stopping_time, size=reaction_time)) 
