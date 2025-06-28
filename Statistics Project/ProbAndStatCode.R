# Load Data
heart <- read.csv("/Users/nikunjfotedar/Downloads/heart_cleveland_upload.csv", stringsAsFactors = TRUE)
library(psych)

summary(heart)
# Descriptive statistics
describe(heart)


# One sample T test
# Is resting BP different from 130?
t.test(heart$trestbps, mu = 130)


# Two sample T test
# Compare cholesterol levels by sex (0 = female, 1 = male)
t.test(chol ~ sex, data = heart)


#One-Tailed T-Test
# Label condition variable
heart$condition <- factor(heart$condition, levels = c(0,1), labels = c("No Disease", "Disease"))

# Is max heart rate lower in diseased patients?
t.test(thalach ~ condition, data = heart, alternative = "greater")

# Paired T test
# Comparing max HR to resting BP
t.test(heart$thalach, heart$trestbps, paired = TRUE, alternative = "greater")

# One Way Annova
# ANOVA: trestbps across chest pain types
heart$cp <- as.factor(heart$cp)
aov_result <- aov(trestbps ~ cp, data = heart)
summary(aov_result)

# TukeyHSD
TukeyHSD(aov_result)


# Correaltion Matrix
# Numeric columns only
heart_numeric <- heart[sapply(heart, is.numeric)]

# Correlation matrix
cor_matrix <- cor(heart_numeric, use = "complete.obs")
round(cor_matrix, 3)
