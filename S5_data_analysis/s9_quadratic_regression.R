# 加载必要的库  
library(ggplot2)  
  
# 定义函数进行二次函数回归并绘制置信带  
quadratic_regression_with_bands <- function(x, y, x_seq_length = 2000, conf_level = 0.95, my_title="Arousal-Valence Relationship", xlabel='Valence', ylabel='Arousal') {  
    
  # 拟合二次回归模型  
  model <- lm(y ~ x + I(x^2))  
    
  # 生成预测值及其置信带  
  new_x <- seq(min(x), max(x), length.out = x_seq_length)  
  predictions <- predict(model, newdata = data.frame(x = new_x), interval = "confidence", level = conf_level)  
    
  # 提取预测值和置信带  
  predicted_y <- predictions[, "fit"]  
  lower_ci <- predictions[, "lwr"]  
  upper_ci <- predictions[, "upr"]  
    
  # 创建数据框以便绘图  
  data_for_plot <- data.frame(x = new_x, y = predicted_y, lower_ci = lower_ci, upper_ci = upper_ci)  
    
  # 使用ggplot2绘图，设置x轴和y轴范围都为[1,7]
  p <- ggplot(data = data_for_plot, aes(x = x)) +  
    geom_point(data = data.frame(x = x, y = y), aes(y = y), color = "blue") +  # 绘制原始数据点  
    geom_line(aes(y = y), color = "blue", linewidth = 1) +  # 绘制回归曲线  
    geom_ribbon(aes(ymin = lower_ci, ymax = upper_ci), fill = "lightblue", alpha = 0.5) +  # 绘制置信带  
    labs(title = my_title,  
         x = xlabel,  
         y = ylabel) +   
    theme(plot.title = element_text(hjust = 0.5),
          axis.title = element_text(),
          text = element_text()) +
     coord_cartesian(xlim = c(1, 7), ylim = c(1, 7))
    
  # 返回ggplot对象  
  print(p)
  return(p)  
}  
  
set.seed(2024)  

library(readxl)
df <- read_excel("FED.xlsx")

V <- df$Valence_mean
A <- df$Arousal_mean

# compare linear and quadratic model
linear_model <- lm(V ~ A)
print(summary(linear_model))

quadratic_model <- lm(V ~ A + I(A^2))
print(summary(quadratic_model))

# call the function
p.va <- quadratic_regression_with_bands(V, A, my_title = "U-shaped Relation of Valence and Arousal", 
                                        xlabel="Valence", ylabel='Arousal')

ggsave(plot = p.va, filename = "./images/Arousal-Valence Relationship.png", width = 6, height = 6, units = "in", dpi = 300)




