#############################################################################
# PROJECT: Envejecimiento
#'Author: *Miguel Moreno-Palacios*
# Mail: miguel.moreno[at]unibague.edu.co
# Date: 13 de octubre de 2025
# Content: EDA, correlaciones policóricas + coherencia interna, 
#          y modelos logísticos (completo y “sin fuga”)
#############################################################################

###############################
# 0) PAQUETES Y RUTAS ----
###############################
# Utilidad de los paquetes:
# - readxl:      leer hojas de Excel
# - dplyr:       manipulación de datos (pipes, mutate, select, etc.)
# - tidyr:       pivot_longer/wider, drop_na
# - ggplot2:     visualizaciones
# - ggpubr:      ggqqplot (QQ plots rápidos)
# - stringr:     utilidades de texto (str_replace, str_wrap, etc.)
# - broom:       tidiers para modelos: tidy(), glance(), augment()
# - pROC:        curvas ROC y AUC
# - car:         diagnóstico de colinealidad (VIF)
# - forcats:     manipulación de factores (fct_relevel, fct_lump)
# - psych:       alfa de Cronbach, correlaciones policóricas
# - corrplot:    visualización rápida de matrices de correlación
# - pheatmap:    heatmaps con dendrogramas jerárquicos
# - RColorBrewer: paletas de color
# - purrr:       programación funcional (map/lapply con azúcar sintáctico)
# - writexl:     exportar a Excel (XLSX)
suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(ggpubr)
  library(stringr)
  library(broom)
  library(pROC)
  library(car)
  library(forcats)
  library(psych)
  library(corrplot)
  library(pheatmap)
  library(RColorBrewer)
  library(purrr)
  library(writexl)
})

# Directorio de trabajo
setwd("/Users/miguelmoreno/Downloads/envejecimiento/")

# Rutas base
ruta_xlsx <- "/Users/miguelmoreno/Downloads/envejecimiento/database4.xlsx"
fig_dir   <- path.expand("/Users/miguelmoreno/Downloads/envejecimiento/figuras")
tab_dir   <- path.expand("/Users/miguelmoreno/Downloads/envejecimiento/tablas")
if (!dir.exists(fig_dir)) dir.create(fig_dir, recursive = TRUE)
if (!dir.exists(tab_dir)) dir.create(tab_dir, recursive = TRUE)

# Paletas globales (reutilizadas en todo el script)
pal_heat  <- colorRampPalette(rev(brewer.pal(11, "RdYlBu")))(200)
breaks_hm <- seq(-1, 1, length.out = 201)   # length(pal_heat) == length(breaks_hm)-1


###############################
# 1) LECTURA DE DATOS ----
###############################
neuropatia_diab <- read_excel(ruta_xlsx, sheet = "base_neuropatia_diab")
ecv             <- read_excel(ruta_xlsx, sheet = "base_ecv")
estres          <- read_excel(ruta_xlsx, sheet = "base_estres")
familiar        <- read_excel(ruta_xlsx, sheet = "base_familiar")
depresion       <- read_excel(ruta_xlsx, sheet = "base_depresion")
# Convención: *_PUNTOS son ítems; score_* es total de escala.


#############################################################################
# 2) EDA – NEUROPATÍA DIABÉTICA ----
#############################################################################

## 2.1 Originales numéricas: boxplots
p_nd_box <- neuropatia_diab %>%
  select(where(is.numeric), -contains("puntos"), -contains("score")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = variable, y = valor)) +
  geom_boxplot(fill = "skyblue", alpha = 0.6, outlier.shape = NA) +
  geom_jitter(width = 0.2, alpha = 0.6) +
  coord_flip() +
  theme_minimal() +
  labs(title = "Distribución de variables originales (numéricas) - Neuropatía diabética",
       x = "Variable", y = "Valor")
ggsave(file.path(fig_dir, "nd_boxplots.png"), p_nd_box, width = 9, height = 6, dpi = 300)

## 2.1b Originales numéricas: histogramas
p_nd_hist <- neuropatia_diab %>%
  select(where(is.numeric), -contains("puntos"), -contains("score")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, fill = "steelblue", color = "white") +
  facet_wrap(~variable, scales = "free") +
  theme_minimal() +
  labs(title = "Histogramas de variables originales (numéricas) - Neuropatía diabética",
       x = "Valor", y = "Frecuencia")
ggsave(file.path(fig_dir, "nd_hist_num.png"), p_nd_hist, width = 10, height = 7, dpi = 300)

## 2.2 Ítems *_PUNTOS: medias con IC95%
p_nd_ic <- neuropatia_diab %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "item", values_to = "x") %>%
  group_by(item) %>%
  summarise(
    n = sum(!is.na(x)),
    media = mean(x, na.rm = TRUE),
    sd = sd(x, na.rm = TRUE),
    se = sd / sqrt(n),
    li = media - 1.96 * se,
    ls = media + 1.96 * se,
    .groups = "drop"
  ) %>%
  ggplot(aes(y = item, x = media)) +
  geom_point() +
  geom_errorbarh(aes(xmin = li, xmax = ls), height = 0.2) +
  theme_minimal() +
  labs(title = "Media de puntuación por ítem (IC95%) - Neuropatía diabética",
       x = "Media de puntos", y = "Ítem")
ggsave(file.path(fig_dir, "nd_ic_item.png"), p_nd_ic, width = 9, height = 7, dpi = 300)

## 2.2b Ítems *_PUNTOS: histogramas
p_nd_hist_puntos <- neuropatia_diab %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, fill = "darkorange", color = "white") +
  facet_wrap(~variable, scales = "free_y") +
  theme_minimal() +
  labs(title = "Histogramas de puntuaciones parciales - Neuropatía diabética",
       x = "Puntos del ítem", y = "Frecuencia")
ggsave(file.path(fig_dir, "nd_hist_puntos.png"), p_nd_hist_puntos, width = 10, height = 7, dpi = 300)


#############################################################################
# EDA – EVENTO CEREBRO VASCULAR ----
#############################################################################

##  Ítems *_PUNTOS: medias con IC95%
p_ecv_ic <- ecv %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "item", values_to = "x") %>%
  group_by(item) %>%
  summarise(
    n = sum(!is.na(x)),
    media = mean(x, na.rm = TRUE),
    sd = sd(x, na.rm = TRUE),
    se = sd / sqrt(n),
    li = media - 1.96 * se,
    ls = media + 1.96 * se,
    .groups = "drop"
  ) %>%
  ggplot(aes(y = item, x = media)) +
  geom_point() +
  geom_errorbarh(aes(xmin = li, xmax = ls), height = 0.2) +
  theme_minimal() +
  labs(title = "Media de puntuación por ítem (IC95%) - ecv",
       x = "Media de puntos", y = "Ítem")
ggsave(file.path(fig_dir, "ecv_ic_item.png"), p_nd_ic, width = 9, height = 7, dpi = 300)

##  Ítems *_PUNTOS: histogramas
p_ecv_hist_puntos <- ecv %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, fill = "darkorange", color = "white") +
  facet_wrap(~variable, scales = "free_y") +
  theme_minimal() +
  labs(title = "Histogramas de puntuaciones parciales - ECV",
       x = "Puntos del ítem", y = "Frecuencia")
ggsave(file.path(fig_dir, "ecv_hist_puntos.png"), p_nd_hist_puntos, width = 10, height = 7, dpi = 300)




#############################################################################
# 3) EDA – ESTRÉS ----
#############################################################################

## 3.1 Originales categóricas: barras
p_est_bar <- estres %>%
  select(-contains("PUNTOS"), -contains("score")) %>%
  select(where(~ !is.numeric(.))) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "respuesta") %>%
  ggplot(aes(x = respuesta)) +
  geom_bar() +
  facet_wrap(~variable, scales = "free_x") +
  scale_x_discrete(labels = function(x) stringr::str_wrap(x, width = 10)) +
  theme_minimal() +
  theme(axis.text.x = element_text(margin = margin(t = 4))) +
  labs(title = "Distribución de respuestas originales - Estrés",
       x = "Categoría", y = "Frecuencia")
ggsave(file.path(fig_dir, "estres_barras.png"), p_est_bar, width = 10, height = 7, dpi = 300)

## 3.2 Ítems *_PUNTOS: medias con IC95%
p_est_ic <- estres %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "item", values_to = "x") %>%
  group_by(item) %>%
  summarise(
    n = sum(!is.na(x)),
    media = mean(x, na.rm = TRUE),
    sd = sd(x, na.rm = TRUE),
    se = sd / sqrt(n),
    li = media - 1.96 * se,
    ls = media + 1.96 * se,
    .groups = "drop"
  ) %>%
  ggplot(aes(y = item, x = media)) +
  geom_point() +
  geom_errorbarh(aes(xmin = li, xmax = ls), height = 0.2) +
  theme_minimal() +
  labs(title = "Media de puntos por ítem (IC95%) - Estrés",
       x = "Media de puntos", y = "Ítem")
ggsave(file.path(fig_dir, "estres_ic_item.png"), p_est_ic, width = 9, height = 7, dpi = 300)

## 3.2b Ítems *_PUNTOS: histogramas
p_est_hist_puntos <- estres %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, color = "white") +
  facet_wrap(~variable, scales = "free_y") +
  theme_minimal() +
  labs(title = "Histogramas de puntuaciones parciales - Estrés",
       x = "Puntos del ítem", y = "Frecuencia")
ggsave(file.path(fig_dir, "estres_hist_puntos.png"), p_est_hist_puntos, width = 10, height = 7, dpi = 300)


#############################################################################
# 4) EDA – DINÁMICA FAMILIAR (APGAR) ----
#############################################################################

## 4.1 Originales categóricas: barras
p_fam_bar <- familiar %>%
  select(-contains("PUNTOS"), -contains("score")) %>%
  select(where(~ !is.numeric(.))) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "respuesta") %>%
  ggplot(aes(x = respuesta)) +
  geom_bar() +
  facet_wrap(~variable, scales = "free_x") +
  theme_minimal() +
  labs(title = "Distribución de respuestas originales - Dinámica familiar",
       x = "Categoría", y = "Frecuencia")
ggsave(file.path(fig_dir, "familiar_barras.png"), p_fam_bar, width = 10, height = 7, dpi = 300)

## 4.2 Ítems *_PUNTOS: medias con IC95%
p_fam_ic <- familiar %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "item", values_to = "x") %>%
  group_by(item) %>%
  summarise(
    n = sum(!is.na(x)),
    media = mean(x, na.rm = TRUE),
    sd = sd(x, na.rm = TRUE),
    se = sd / sqrt(n),
    li = media - 1.96 * se,
    ls = media + 1.96 * se,
    .groups = "drop"
  ) %>%
  ggplot(aes(y = item, x = media)) +
  geom_point() +
  geom_errorbarh(aes(xmin = li, xmax = ls), height = 0.2) +
  theme_minimal() +
  labs(title = "Media de puntos por ítem (IC95%) - Dinámica familiar",
       x = "Media de puntos", y = "Ítem")
ggsave(file.path(fig_dir, "familiar_ic_item.png"), p_fam_ic, width = 9, height = 7, dpi = 300)

## 4.2b Ítems *_PUNTOS: histogramas
p_fam_hist_puntos <- familiar %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, color = "white") +
  facet_wrap(~variable, scales = "free_y") +
  theme_minimal() +
  labs(title = "Histogramas de puntuaciones parciales - Dinámica familiar",
       x = "Puntos del ítem", y = "Frecuencia")
ggsave(file.path(fig_dir, "familiar_hist_puntos.png"), p_fam_hist_puntos, width = 10, height = 7, dpi = 300)


#############################################################################
# 5) EDA – DEPRESIÓN ----
#############################################################################

## 5.1 Originales categóricas: barras
p_dep_bar <- depresion %>%
  select(-contains("PUNTOS"), -contains("score")) %>%
  select(where(~ !is.numeric(.))) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "respuesta") %>%
  ggplot(aes(x = respuesta)) +
  geom_bar() +
  facet_wrap(~variable, scales = "free_x") +
  theme_minimal() +
  labs(title = "Distribución de respuestas originales - Depresión",
       x = "Categoría", y = "Frecuencia")
ggsave(file.path(fig_dir, "dep_barras.png"), p_dep_bar, width = 10, height = 7, dpi = 300)

## 5.2 Ítems *_PUNTOS: proporciones + histogramas
p_dep_prop <- depresion %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "item", values_to = "x") %>%
  group_by(item) %>%
  summarise(
    n   = n(),
    prop = mean(x, na.rm = TRUE),
    se   = sqrt(pmax(prop*(1 - prop)/n, 0)),
    li   = pmax(0, prop - 1.96*se),
    ls   = pmin(1, prop + 1.96*se),
    .groups = "drop"
  ) %>%
  ggplot(aes(y = item, x = prop)) +
  geom_point() +
  geom_errorbarh(aes(xmin = li, xmax = ls), height = 0.2) +
  scale_x_continuous(limits = c(0,1)) +
  theme_minimal() +
  labs(title = "Proporción de respuesta = 1 por ítem - Depresión",
       x = "Proporción", y = "Ítem")
ggsave(file.path(fig_dir, "dep_prop_item.png"), p_dep_prop, width = 9, height = 7, dpi = 300)

p_dep_hist_puntos <- depresion %>%
  select(contains("PUNTOS")) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "valor") %>%
  ggplot(aes(x = valor)) +
  geom_histogram(bins = 15, color = "white") +
  facet_wrap(~variable, scales = "free_y") +
  theme_minimal() +
  labs(title = "Histogramas de puntuaciones parciales - Depresión",
       x = "Puntos del ítem", y = "Frecuencia")
ggsave(file.path(fig_dir, "dep_hist_puntos.png"), p_dep_hist_puntos, width = 10, height = 7, dpi = 300)


#############################################################################
# 6) NORMALIDAD – QQ PLOTS DE SCORES ----
#############################################################################
p_nd_qq  <- ggqqplot(neuropatia_diab, x = "score_neurodiab") + labs(title = "QQ Plot Score total - Neuropatía")
p_ecv_qq <- ggqqplot(ecv,        x = "score_ecv")  + labs(title = "QQ Plot Score total - ECV")
p_est_qq <- ggqqplot(estres,          x = "score_estres")    + labs(title = "QQ Plot Score total - Estrés")
p_dep_qq <- ggqqplot(depresion,       x = "score_depresion") + labs(title = "QQ Plot Score total - Depresión")
p_fam_qq <- ggqqplot(familiar,        x = "score_familiar")  + labs(title = "QQ Plot Score total - Apgar familiar")

ggsave(file.path(fig_dir, "qq_neuropatia.png"), p_nd_qq,  width = 6, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "qq_ecv.png"),     p_ecv_qq, width = 6, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "qq_estres.png"),     p_est_qq, width = 6, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "qq_depresion.png"),  p_dep_qq, width = 6, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "qq_apgar.png"),      p_fam_qq, width = 6, height = 6, dpi = 300)


#############################################################################
# 7) COMPARATIVO – SCORE TOTAL POR MATRIZ ----
#############################################################################
p_scores_box <- bind_rows(
  transmute(neuropatia_diab, matriz = "Neuropatía", score = score_neurodiab),
  transmute(ecv,          matriz = "ecv",     score = score_ecv),
  transmute(estres,          matriz = "Estrés",     score = score_estres),
  transmute(familiar,        matriz = "Familiar",   score = score_familiar),
  transmute(depresion,       matriz = "Depresión",  score = score_depresion)
) %>%
  ggplot(aes(x = matriz, y = score)) +
  geom_boxplot(fill = "grey80") +
  geom_jitter(width = 0.15, alpha = 0.5) +
  coord_flip() +
  theme_minimal() +
  labs(title = "Score total por matriz", x = "Matriz", y = "Score total")
ggsave(file.path(fig_dir, "scores_box.png"), p_scores_box, width = 8, height = 6, dpi = 300)

# Histogramas con umbrales
p_s_neuro <- ggplot(neuropatia_diab, aes(x = score_neurodiab)) +
  geom_histogram(binwidth = 1, boundary = 0, color = "white") +
  geom_vline(xintercept = 12, linetype = "dashed", linewidth = 1, color = "red") +
  theme_minimal() + labs(title = "Histograma Score - Neuropatía", x = "Score", y = "Frecuencia")
p_s_ecv <- ggplot(ecv, aes(x = score_ecv)) +
  geom_histogram(binwidth = 1, boundary = 0, color = "white") +
  geom_vline(xintercept = 12, linetype = "dashed", linewidth = 1, color = "red") +
  theme_minimal() + labs(title = "Histograma Score - ECV", x = "Score", y = "Frecuencia")
p_s_est   <- ggplot(estres, aes(x = score_estres)) +
  geom_histogram(binwidth = 1, boundary = 0, color = "white") +
  geom_vline(xintercept = 14, linetype = "dashed", linewidth = 1, color = "red") +
  theme_minimal() + labs(title = "Histograma Score - Estrés", x = "Score", y = "Frecuencia")
p_s_fam   <- ggplot(familiar, aes(x = score_familiar)) +
  geom_histogram(binwidth = 1, boundary = 0, color = "white") +
  geom_vline(xintercept = 13, linetype = "dashed", linewidth = 1, color = "red") +
  theme_minimal() + labs(title = "Histograma Score - Familiar", x = "Score", y = "Frecuencia")
p_s_dep   <- ggplot(depresion, aes(x = score_depresion)) +
  geom_histogram(binwidth = 1, boundary = 0, color = "white") +
  geom_vline(xintercept = 1, linetype = "dashed", linewidth = 1, color = "red") +
  theme_minimal() + labs(title = "Histograma Score - Depresión", x = "Score", y = "Frecuencia")

ggsave(file.path(fig_dir, "score_hist_neuropatia.png"), p_s_neuro, width = 8, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "score_hist_ecv.png"), p_s_ecv, width = 8, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "score_hist_estres.png"),     p_s_est,   width = 8, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "score_hist_familiar.png"),   p_s_fam,   width = 8, height = 6, dpi = 300)
ggsave(file.path(fig_dir, "score_hist_depresion.png"),  p_s_dep,   width = 8, height = 6, dpi = 300)


#############################################################################
# 8) COHERENCIA INTERNA Y CORRELACIONES ENTRE ÍTEMS ----
#    Matriz policórica por instrumento + alfa
#############################################################################

# Helper: filtro de ítems no constantes
not_constant <- function(v) length(unique(na.omit(v))) > 1

# --- NEUROPATÍA
X_neuro <- neuropatia_diab %>% select(contains("PUNTOS")) %>% select(where(not_constant))
pc_neuro <- psych::polychoric(X_neuro)$rho # Aca deben salen dos warnings asociados a la estructura de los datos.
png(file.path(fig_dir, "corrplot_neuropatia.png"), width = 1600, height = 1200, res = 180)
corrplot(pc_neuro, method = "color", type = "lower", tl.col = "black",
         number.cex = .7, title = "Correlación policórica – Neuropatía", mar = c(0,0,2,0))
dev.off()
alpha_neuro <- psych::alpha(X_neuro, check.keys = TRUE)
pheatmap(
  pc_neuro, color = pal_heat, breaks = breaks_hm,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE, border_color = NA,
  main = "Heatmap correlación (policórica) - Neuropatía",
  fontsize = 9, fontsize_row = 8, fontsize_col = 8,
  filename = file.path(fig_dir, "heatmap_policorico_neuropatia.png"),
  width = 10, height = 9
)

# --- EVENTO CEREBRO VASCULAR - ecv - 
X_ecv <- ecv %>% select(contains("PUNTOS")) %>% select(where(not_constant))
pc_ecv <- psych::polychoric(X_ecv)$rho # Aca deben salen dos warnings asociados a la estructura de los datos.
png(file.path(fig_dir, "corrplot_ecv.png"), width = 1600, height = 1200, res = 180)
corrplot(pc_ecv, method = "color", type = "lower", tl.col = "black",
         number.cex = .7, title = "Correlación policórica – ecv", mar = c(0,0,2,0))
dev.off()
alpha_ecv <- psych::alpha(X_ecv, check.keys = TRUE)
pheatmap(
  pc_ecv, color = pal_heat, breaks = breaks_hm,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE, border_color = NA,
  main = "Heatmap correlación (policórica) - ecv",
  fontsize = 9, fontsize_row = 8, fontsize_col = 8,
  filename = file.path(fig_dir, "heatmap_policorico_ecv.png"),
  width = 10, height = 9
)

# --- ESTRÉS
X_estres <- estres %>% select(contains("PUNTOS")) %>% select(where(not_constant))
pc_estres <- psych::polychoric(X_estres)$rho
png(file.path(fig_dir, "corrplot_estres.png"), width = 1600, height = 1200, res = 180)
corrplot(pc_estres, method = "color", type = "lower", tl.col = "black",
         title = "Correlación policórica – Estrés", mar = c(0,0,2,0))
dev.off()
alpha_estres <- psych::alpha(X_estres, check.keys = TRUE)
pheatmap(
  pc_estres, color = pal_heat, breaks = breaks_hm,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE, border_color = NA,
  main = "Heatmap correlación (policórica) - Estrés",
  fontsize = 9, fontsize_row = 8, fontsize_col = 8,
  filename = file.path(fig_dir, "heatmap_policorico_estres.png"),
  width = 10, height = 9
)

# --- DINAMICA FAMILIAR
X_apgar <- familiar %>% select(contains("PUNTOS")) %>% select(where(not_constant))
pc_apgar <- psych::polychoric(X_apgar)$rho
png(file.path(fig_dir, "corrplot_apgar.png"), width = 1600, height = 1200, res = 180)
corrplot(pc_apgar, method = "color", type = "lower", tl.col = "black",
         title = "Correlación policórica – Dinámica Familiar", mar = c(0,0,2,0))
dev.off()
alpha_apgar <- psych::alpha(X_apgar, check.keys = TRUE)
pheatmap(
  pc_apgar, color = pal_heat, breaks = breaks_hm,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE, border_color = NA,
  main = "Heatmap correlación (policórica) - Apgar",
  fontsize = 9, fontsize_row = 8, fontsize_col = 8,
  filename = file.path(fig_dir, "heatmap_policorico_apgar.png"),
  width = 10, height = 9
)

# --- DEPRESIÓN
X_dep <- depresion %>% select(contains("PUNTOS")) %>% select(where(not_constant))
pc_dep <- psych::polychoric(X_dep)$rho
png(file.path(fig_dir, "corrplot_depresion.png"), width = 1600, height = 1200, res = 180)
corrplot(pc_dep, method = "color", type = "lower", tl.col = "black",
         title = "Correlación policórica – Depresión", mar = c(0,0,2,0))
dev.off()
alpha_dep <- psych::alpha(X_dep, check.keys = TRUE)
pheatmap(
  pc_dep, color = pal_heat, breaks = breaks_hm,
  cluster_rows = TRUE, cluster_cols = TRUE,
  show_rownames = TRUE, show_colnames = TRUE, border_color = NA,
  main = "Heatmap correlación (policórica) - Depresión",
  fontsize = 9, fontsize_row = 8, fontsize_col = 8,
  filename = file.path(fig_dir, "heatmap_policorico_depresion.png"),
  width = 10, height = 9
)


#############################################################################
# 9) CONFIABILIDAD: ALFA CLÁSICO vs ORDINAl (policórico) + ALFA DROP ----
#############################################################################

# --- NEUROPATÍA
alpha_neuro_cl  <- psych::alpha(X_neuro, check.keys = TRUE)
alpha_neuro_ord <- psych::alpha(pc_neuro, n.obs = nrow(X_neuro), check.keys = FALSE)
ad_neuro_cl  <- data.frame(Item = rownames(alpha_neuro_cl$alpha.drop),
                           Alfa_clasico_sin_item = alpha_neuro_cl$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_neuro_ord <- data.frame(Item = rownames(alpha_neuro_ord$alpha.drop),
                           Alfa_ordinal_sin_item = alpha_neuro_ord$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_neuro <- merge(ad_neuro_cl, ad_neuro_ord, by = "Item", all = TRUE)
write.csv(ad_neuro, file.path(tab_dir, "alpha_drop_neuropatia.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# --- EVENTO CEREBRO VASCULAR (ecv)
alpha_ecv_cl  <- psych::alpha(X_ecv, check.keys = TRUE)
alpha_ecv_ord <- psych::alpha(pc_ecv, n.obs = nrow(X_ecv), check.keys = TRUE)
ad_ecv_cl  <- data.frame(Item = rownames(alpha_ecv_cl$alpha.drop),
                           Alfa_clasico_sin_item = alpha_ecv_cl$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_ecv_ord <- data.frame(Item = rownames(alpha_ecv_ord$alpha.drop),
                           Alfa_ordinal_sin_item = alpha_ecv_ord$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_ecv <- merge(ad_ecv_cl, ad_ecv_ord, by = "Item", all = TRUE)
write.csv(ad_ecv, file.path(tab_dir, "alpha_drop_ecv.csv"), row.names = FALSE, fileEncoding = "UTF-8")


# --- ESTRÉS
alpha_estres_cl  <- psych::alpha(X_estres, check.keys = TRUE)
alpha_estres_ord <- psych::alpha(pc_estres, n.obs = nrow(X_estres), check.keys = TRUE)
ad_estres_cl  <- data.frame(Item = rownames(alpha_estres_cl$alpha.drop),
                            Alfa_clasico_sin_item = alpha_estres_cl$alpha.drop[, "raw_alpha"],
                            row.names = NULL, check.names = FALSE)
ad_estres_ord <- data.frame(Item = rownames(alpha_estres_ord$alpha.drop),
                            Alfa_ordinal_sin_item = alpha_estres_ord$alpha.drop[, "raw_alpha"],
                            row.names = NULL, check.names = FALSE)
ad_estres <- merge(ad_estres_cl, ad_estres_ord, by = "Item", all = TRUE)
write.csv(ad_estres, file.path(tab_dir, "alpha_drop_estres.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# --- FAMILIAR
alpha_apgar_cl  <- psych::alpha(X_apgar, check.keys = TRUE)
alpha_apgar_ord <- psych::alpha(pc_apgar, n.obs = nrow(X_apgar), check.keys = FALSE)
ad_apgar_cl  <- data.frame(Item = rownames(alpha_apgar_cl$alpha.drop),
                           Alfa_clasico_sin_item = alpha_apgar_cl$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_apgar_ord <- data.frame(Item = rownames(alpha_apgar_ord$alpha.drop),
                           Alfa_ordinal_sin_item = alpha_apgar_ord$alpha.drop[, "raw_alpha"],
                           row.names = NULL, check.names = FALSE)
ad_apgar <- merge(ad_apgar_cl, ad_apgar_ord, by = "Item", all = TRUE)
write.csv(ad_apgar, file.path(tab_dir, "alpha_drop_familiar.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# --- DEPRESIÓN
alpha_dep_cl  <- psych::alpha(X_dep, check.keys = TRUE)
alpha_dep_ord <- psych::alpha(pc_dep, n.obs = nrow(X_dep), check.keys = FALSE)
ad_dep_cl  <- data.frame(Item = rownames(alpha_dep_cl$alpha.drop),
                         Alfa_clasico_sin_item = alpha_dep_cl$alpha.drop[, "raw_alpha"],
                         row.names = NULL, check.names = FALSE)
ad_dep_ord <- data.frame(Item = rownames(alpha_dep_ord$alpha.drop),
                         Alfa_ordinal_sin_item = alpha_dep_ord$alpha.drop[, "raw_alpha"],
                         row.names = NULL, check.names = FALSE)
ad_dep <- merge(ad_dep_cl, ad_dep_ord, by = "Item", all = TRUE)
write.csv(ad_dep, file.path(tab_dir, "alpha_drop_depresion.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# Resumen comparativo (clásico vs ordinal)
alpha_resumen <- data.frame(
  Matriz       = c("Neuropatía", "ecv", "Estrés", "Familiar", "Depresión"),
  Alfa_clasico = c(alpha_neuro_cl$total$raw_alpha,
                   alpha_ecv_cl$total$raw_alpha,
                   alpha_estres_cl$total$raw_alpha,
                   alpha_apgar_cl$total$raw_alpha,
                   alpha_dep_cl$total$raw_alpha),
  Alfa_ordinal = c(alpha_neuro_ord$total$raw_alpha,
                   alpha_ecv_ord$total$raw_alpha,
                   alpha_estres_ord$total$raw_alpha,
                   alpha_apgar_ord$total$raw_alpha,
                   alpha_dep_ord$total$raw_alpha)
)
write.csv(alpha_resumen, file.path(tab_dir, "resumen_alfa_clasico_vs_ordinal.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")


#############################################################################
# 10) MODELOS LOGÍSTICOS – NEUROPATÍA ----
#############################################################################

## 10.1 Variable objetivo (completa) para contraste
df <- neuropatia_diab %>% mutate(y = as.integer(score_neurodiab >= 12))
pred_num <- df %>% select(where(is.numeric), -contains("PUNTOS"), -score_neurodiab, -y) %>% names()
pred_cat <- df %>% select(-contains("PUNTOS"), -score_neurodiab) %>% select(where(~ !is.numeric(.))) %>% names()

df_model_neuro <- df %>%
  mutate(across(all_of(pred_cat), as.factor)) %>%
  select(y, all_of(pred_num), all_of(pred_cat)) %>%
  drop_na() %>%
  mutate(across(all_of(pred_num), scale),
         SEXO = fct_relevel(SEXO, "Femenino"))

# Diagnóstico rápido
mean(df_model_neuro$y)
lapply(df_model_neuro[c("ROL","SEXO","ESTRATO","ZONA")], table)
with(df_model_neuro, table(y, ROL))
with(df_model_neuro, table(y, SEXO))
with(df_model_neuro, table(y, ESTRATO))
with(df_model_neuro, table(y, ZONA))

# Reagrupación por separación
df_model_neuro1 <- df_model_neuro %>%
  mutate(
    ESTRATO_g = case_when(
      ESTRATO %in% c("1","2") ~ "bajo",
      ESTRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ESTRATO_g = factor(ESTRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

# Modelo “general” ajustado
form_neuro <- y ~ SEXO + ESTRATO_g + ZONA
fit_glm_neuro1 <- glm(form_neuro, data = df_model_neuro1, family = binomial("logit"))
summary(fit_glm_neuro1)

# OR + Forest
or_tbl_neuro1 <- broom::tidy(fit_glm_neuro1, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(estimate))
p_or_neuro1 <- or_tbl_neuro1 %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(y = term, x = estimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - Neuropatía (modelo general)", x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forest_neuropatia_general.png"), p_or_neuro1, width = 8, height = 6, dpi = 300)

# ROC/AUC (modelo general)
prob_neuro <- predict(fit_glm_neuro1, type = "response")
roc_neuro  <- pROC::roc(df_model_neuro1$y, prob_neuro, quiet = TRUE)
png(file.path(fig_dir, "roc_neuropatia_general.png"), width = 1200, height = 900, res = 160)
plot(roc_neuro, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Neuropatía (modelo general)")
dev.off()

# Exportar tabla del modelo general
write_xlsx(
  broom::tidy(fit_glm_neuro1, conf.int = TRUE) |>
    mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_glm_neuro1) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_neuropatia_general.xlsx")
)

## 10.2 Modelo “sin fuga” (EDAD_PUNTOS + IMC_PUNTOS)
df_noLeak_neuro <- neuropatia_diab %>%
  mutate(y = as.integer((score_neurodiab - EDAD_PUNTOS - IMC_PUNTOS) >= 12)) %>%
  transmute(y, IMC, EDAD, ROL, IMC_PUNTOS, EDAD_PUNTOS, DIABEFAMI_PUNTOS, PERIABDO_PUNTOS) %>%
  drop_na()

fit_noLeak_neuro <- glm(y ~ EDAD_PUNTOS + IMC_PUNTOS, data = df_noLeak_neuro, family = binomial())
summary(fit_noLeak_neuro)

# Comparación EDAD vs ROL
m_age  <- glm(y ~ EDAD, data = df_noLeak_neuro, family = binomial())
m_role <- glm(y ~ ROL,  data = df_noLeak_neuro, family = binomial())
m_both <- glm(y ~ EDAD + ROL, data = df_noLeak_neuro, family = binomial())
AIC(m_age, m_role, m_both)
anova(m_age,  m_both, test = "Chisq")
anova(m_role, m_both, test = "Chisq")

# OR + Forest (sin fuga)
or_tbl_neuro_nl <- broom::tidy(fit_noLeak_neuro, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(estimate))
p_or_neuro_nl <- or_tbl_neuro_nl %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(y = term, x = estimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - Neuropatía (sin fuga)", x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forest_neuropatia_sin_fuga.png"), p_or_neuro_nl, width = 8, height = 6, dpi = 300)

# ROC/AUC (sin fuga) — usar el modelo sin fuga y su y correspondiente
prob_noLeak_neuro <- predict(fit_noLeak_neuro, type = "response")
roc_noLeak_neuro  <- pROC::roc(df_noLeak_neuro$y, prob_noLeak_neuro, quiet = TRUE)
png(file.path(fig_dir, "roc_neuropatia_sin_fuga.png"), width = 1200, height = 900, res = 160)
plot(roc_noLeak_neuro, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Neuropatía (sin fuga)")
dev.off()

# Exportar tabla del modelo sin fuga
write_xlsx(
  broom::tidy(fit_noLeak_neuro, conf.int = TRUE) |>
    mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_noLeak_neuro) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_neuropatia_sin_fuga.xlsx")
)


#############################################################################
# 11) MODELOS LOGÍSTICOS – ESTRÉS ----
#############################################################################

# y “completa” (score_estres >= 14)
df_est <- estres %>% mutate(y = as.integer(score_estres >= 14))
pred_num_est <- df_est %>% select(where(is.numeric), -contains("PUNTOS"), -score_estres, -y) %>% names()
pred_cat_est <- df_est %>% select(-contains("PUNTOS"), -score_estres) %>% select(where(~ !is.numeric(.))) %>% names()

df_model_est <- df_est %>%
  mutate(across(all_of(pred_cat_est), as.factor)) %>%
  select(y, all_of(pred_num_est), all_of(pred_cat_est)) %>%
  drop_na()

if (length(pred_num_est) > 0) df_model_est <- df_model_est %>% mutate(across(all_of(pred_num_est), scale))
if ("SEXO" %in% names(df_model_est)) df_model_est <- df_model_est %>% mutate(SEXO = fct_relevel(SEXO, "Femenino"))

# Diagnóstico y reagrupación
mean(df_model_est$y)
lapply(df_model_est[c("ROL","SEXO","ESTRATO","ZONA")], table)
with(df_model_est, table(y, ROL)); with(df_model_est, table(y, SEXO))
with(df_model_est, table(y, ESTRATO)); with(df_model_est, table(y, ZONA))

df_model_est2 <- df_model_est %>%
  mutate(
    ESTRATO_g = case_when(
      ESTRATO %in% c("1","2") ~ "bajo",
      ESTRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ESTRATO_g = factor(ESTRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

# Modelo general
fit_glm_est <- glm(y ~ ROL + SEXO + ESTRATO_g, data = df_model_est2, family = binomial("logit"))
summary(fit_glm_est)

# ROC/AUC (modelo general)
prob_est_full <- predict(fit_glm_est, type = "response")
roc_est_full  <- pROC::roc(df_model_est2$y, prob_est_full, quiet = TRUE)
png(file.path(fig_dir, "roc_estres_general.png"), width = 1200, height = 900, res = 160)
plot(roc_est_full, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Estrés (modelo general)")
dev.off()

# Exportar tabla del modelo general (aunque sin OR útiles si no hay significancia)
write_xlsx(
  broom::tidy(fit_glm_est, conf.int = TRUE) |>
    bind_cols(
      broom::glance(fit_glm_est) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_estres_general.xlsx")
)

# “SIN FUGA” (resta ENFADADO + DIFICUVIDA)
df_est_noLeak <- estres %>%
  mutate(y = as.integer((score_estres - ENFADADO_PUNTOS - DIFICUVIDA_PUNTOS) >= 14)) %>%
  transmute(y, SEXO, ESTRATO, EDAD, ROL, 
            ESTRES_PUNTOS, PROBLPERSO_PUNTOS, NERVIOSO_PUNTOS,
            CONTROL_PUNTOS, BIEN_PUNTOS, AFRONTAR_PUNTOS,
            DIFICUVIDA_PUNTOS, TODOCONTROL_PUNTOS, ENFADADO_PUNTOS,
            SUPERAR_PUNTOS) %>%
  drop_na()

fit_noLeak_est <- glm(y ~ DIFICUVIDA_PUNTOS + ENFADADO_PUNTOS, data = df_est_noLeak, family = binomial())
summary(fit_noLeak_est)

# Exportar tabla (sin fuga)
write_xlsx(
  broom::tidy(fit_noLeak_est, conf.int = TRUE) |>
    mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_noLeak_est) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_estres_sin_fuga.xlsx")
)

# OR + Forest (sin fuga)
or_tbl_est_nl <- broom::tidy(fit_noLeak_est, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(estimate))
p_or_est_nl <- or_tbl_est_nl %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(y = term, x = estimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - Estrés (sin fuga: ENFADADO + DIFICUVIDA)",
       x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forest_estres_sin_fuga.png"), p_or_est_nl, width = 8, height = 6, dpi = 300)

# ROC/AUC (sin fuga)
prob_est_nl <- predict(fit_noLeak_est, type = "response")
roc_est_nl  <- pROC::roc(df_est_noLeak$y, prob_est_nl, quiet = TRUE)
png(file.path(fig_dir, "roc_estres_sin_fuga.png"), width = 1200, height = 900, res = 160)
plot(roc_est_nl, print.auc = TRUE, legacy.axes = TRUE,
     main = "ROC - Estrés (sin fuga: ENFADADO + DIFICUVIDA)")
dev.off()


#############################################################################
# 12) MODELOS LOGÍSTICOS – DEPRESIÓN ----
#############################################################################

# y “completa” (score_depresion >= 1)
df_dep <- depresion %>% mutate(y = as.integer(score_depresion >= 1))
pred_num_dep <- df_dep %>% select(where(is.numeric), -contains("PUNTOS"), -score_depresion, -y) %>% names()
pred_cat_dep <- df_dep %>% select(-contains("PUNTOS"), -score_depresion) %>% select(where(~ !is.numeric(.))) %>% names()

df_model_dep <- df_dep %>%
  mutate(across(all_of(pred_cat_dep), as.factor)) %>%
  select(y, all_of(pred_num_dep), all_of(pred_cat_dep)) %>%
  drop_na()

if (length(pred_num_dep) > 0) df_model_dep <- df_model_dep %>% mutate(across(all_of(pred_num_dep), scale))
if ("SEXO" %in% names(df_model_dep)) df_model_dep <- df_model_dep %>% mutate(SEXO = fct_relevel(SEXO, "Femenino"))

# Diagnóstico y reagrupación
mean(df_model_dep$y)
lapply(df_model_dep[c("ROL","SEXO","ESTRATO","ZONA")], table)
with(df_model_dep, table(y, ROL)); with(df_model_dep, table(y, SEXO))
with(df_model_dep, table(y, ESTRATO)); with(df_model_dep, table(y, ZONA))

df_model_dep2 <- df_model_dep %>%
  mutate(
    ESTRATO_g = case_when(
      ESTRATO %in% c("1","2") ~ "bajo",
      ESTRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ESTRATO_g = factor(ESTRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

# Modelo general (variables con mejor comportamiento)
fit_glm_dep <- glm(y ~ SEXO + ESTRATO_g, data = df_model_dep2, family = binomial("logit"))
summary(fit_glm_dep)

# OR + Forest (general)
or_tbl_dep_gen <- broom::tidy(fit_glm_dep, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(estimate))
p_or_dep_gen <- or_tbl_dep_gen %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(y = term, x = estimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - Depresión (modelo general)",
       x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forest_depresion_general.png"), p_or_dep_gen, width = 8, height = 6, dpi = 300)

# ROC/AUC (general)
prob_dep <- predict(fit_glm_dep, type = "response")
roc_dep  <- pROC::roc(df_model_dep2$y, prob_dep, quiet = TRUE)
png(file.path(fig_dir, "roc_depresion_general.png"), width = 1200, height = 900, res = 160)
plot(roc_dep, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Depresión (modelo general)")
dev.off()

# Exportar tabla del modelo general
write_xlsx(
  broom::tidy(fit_glm_dep, conf.int = TRUE) |>
    mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_glm_dep) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_depresion_general.xlsx")
)

# “SIN FUGA” — usar solo un ítem del índice
depresion1 <- depresion %>%
  mutate(
    ESTRATO_g = case_when(
      ESTRATO %in% c("1","2") ~ "bajo",
      ESTRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ESTRATO_g = factor(ESTRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

df_dep_noLeak <- depresion1 %>%
  mutate(y = as.integer((score_depresion - DEPRIMI_PUNTOS) >= 1)) %>%
  transmute(y, DEPRIMI_PUNTOS, INTERES_PUNTOS, ESTRATO_g, SEXO) %>%
  drop_na()

fit_noLeak_dep <- glm(y ~ DEPRIMI_PUNTOS, data = df_dep_noLeak, family = binomial())
summary(fit_noLeak_dep)

# Exportar tabla (sin fuga)
write_xlsx(
  broom::tidy(fit_noLeak_dep, conf.int = TRUE) |>
    mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_noLeak_dep) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_depresion_sin_fuga_DEPRIMI.xlsx")
)

# OR + Forest (sin fuga, DEPRIMI)
or_tbl_dep_nl <- broom::tidy(fit_noLeak_dep, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(estimate))
p_or_dep_nl <- or_tbl_dep_nl %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(y = term, x = estimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - Depresión (sin fuga: DEPRIMI)",
       x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forest_depresion_sin_fuga_DEPRIMI.png"), p_or_dep_nl, width = 8, height = 6, dpi = 300)

# ROC/AUC (sin fuga)
prob_dep_nl <- predict(fit_noLeak_dep, type = "response")
roc_dep_nl  <- pROC::roc(df_dep_noLeak$y, prob_dep_nl, quiet = TRUE)
png(file.path(fig_dir, "roc_depresion_sin_fuga_DEPRIMI.png"), width = 1200, height = 900, res = 160)
plot(roc_dep_nl, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Depresión (sin fuga: DEPRIMI)")
dev.off()


#############################################################################
# 13) MODELOS LOGÍSTICOS – DINÁMICA FAMILIAR (APGAR) ----
#############################################################################

# y “completa” (score_familiar >= 13)
df_fam <- familiar %>% mutate(y = as.integer(score_familiar >= 13))
pred_num_fam <- df_fam %>% select(where(is.numeric), -contains("PUNTOS"), -score_familiar, -y) %>% names()
pred_cat_fam <- df_fam %>% select(-contains("PUNTOS"), -score_familiar) %>% select(where(~ !is.numeric(.))) %>% names()

df_model_fam <- df_fam %>%
  mutate(across(all_of(pred_cat_fam), as.factor)) %>%
  select(y, all_of(pred_num_fam), all_of(pred_cat_fam)) %>%
  drop_na()

if (length(pred_num_fam) > 0) df_model_fam <- df_model_fam %>% mutate(across(all_of(pred_num_fam), scale))
if ("SEXO" %in% names(df_model_fam)) df_model_fam <- df_model_fam %>% mutate(SEXO = fct_relevel(SEXO, "Femenino"))

# Diagnóstico y reagrupación
mean(df_model_fam$y)
lapply(df_model_fam[c("ROL","SEXO","ESTRATO","ZONA")], table)
with(df_model_fam, table(y, ROL)); with(df_model_fam, table(y, SEXO))
with(df_model_fam, table(y, ESTRATO)); with(df_model_fam, table(y, ZONA))

df_model_fam2 <- df_model_fam %>%
  mutate(
    ESTRATO_g = case_when(
      ESTRATO %in% c("1","2") ~ "bajo",
      ESTRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ESTRATO_g = factor(ESTRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

# Modelo general
fit_glm_fam <- glm(y ~ SEXO + ESTRATO_g + ZONA, data = df_model_fam2, family = binomial("logit"))
summary(fit_glm_fam)

# ROC/AUC (general)
prob_fam <- predict(fit_glm_fam, type = "response")
roc_fam  <- pROC::roc(df_model_fam2$y, prob_fam, quiet = TRUE)
png(file.path(fig_dir, "roc_familiar_general.png"), width = 1200, height = 900, res = 160)
plot(roc_fam, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - Familiar (modelo general)")
dev.off()

# Exportar tabla del modelo general
write_xlsx(
  broom::tidy(fit_glm_fam, conf.int = TRUE) |>
    bind_cols(
      broom::glance(fit_glm_fam) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_familiar_general.xlsx")
)

# “SIN FUGA”: un ítem por modelo
df_fam_noLeak1 <- familiar %>% mutate(y = as.integer((score_familiar - FAMIPROBLE_PUNTOS) >= 13)) %>%
  transmute(y, FAMIPROBLE_PUNTOS) %>% drop_na()
df_fam_noLeak2 <- familiar %>% mutate(y = as.integer((score_familiar - FAMIPARTI_PUNTOS) >= 13)) %>%
  transmute(y, FAMIPARTI_PUNTOS) %>% drop_na()
df_fam_noLeak3 <- familiar %>% mutate(y = as.integer((score_familiar - FAMIACTI_PUNTOS) >= 13)) %>%
  transmute(y, FAMIACTI_PUNTOS) %>% drop_na()
df_fam_noLeak4 <- familiar %>% mutate(y = as.integer((score_familiar - FAMIAFEC_PUNTOS) >= 13)) %>%
  transmute(y, FAMIAFEC_PUNTOS) %>% drop_na()
df_fam_noLeak5 <- familiar %>% mutate(y = as.integer((score_familiar - FAMITIEMPO_PUNTOS) >= 13)) %>%
  transmute(y, FAMITIEMPO_PUNTOS) %>% drop_na()

fit_noLeak_fam1 <- glm(y ~ FAMIPROBLE_PUNTOS,  data = df_fam_noLeak1, family = binomial())
fit_noLeak_fam2 <- glm(y ~ FAMIPARTI_PUNTOS,   data = df_fam_noLeak2, family = binomial())
fit_noLeak_fam3 <- glm(y ~ FAMIACTI_PUNTOS,    data = df_fam_noLeak3, family = binomial())
fit_noLeak_fam4 <- glm(y ~ FAMIAFEC_PUNTOS,    data = df_fam_noLeak4, family = binomial())
fit_noLeak_fam5 <- glm(y ~ FAMITIEMPO_PUNTOS,  data = df_fam_noLeak5, family = binomial())

# Exportar todas las hojas en un solo XLSX
write_xlsx(
  lapply(
    list(
      D_familiar1 = fit_noLeak_fam1, 
      D_familiar2 = fit_noLeak_fam2, 
      D_familiar3 = fit_noLeak_fam3, 
      D_familiar4 = fit_noLeak_fam4, 
      D_familiar5 = fit_noLeak_fam5
    ),
    \(m)
    broom::tidy(m, conf.int = TRUE) |>
      mutate(OR = exp(estimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
      bind_cols(
        broom::glance(m) |>
          transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                    McFadden_R2 = 1 - deviance/null.deviance)
      ) |>
      mutate(across(where(is.numeric), ~ round(.x, 4)))
  ),
  path = file.path(tab_dir, "resultados_logit_familiar_sin_fuga.xlsx")
)

# Forest combinado “sin fuga” (Apgar)
or_tbl_fam1 <- broom::tidy(fit_noLeak_fam1, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>% filter(term != "(Intercept)") %>% arrange(desc(estimate))
or_tbl_fam2 <- broom::tidy(fit_noLeak_fam2, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>% filter(term != "(Intercept)") %>% arrange(desc(estimate))
or_tbl_fam3 <- broom::tidy(fit_noLeak_fam3, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>% filter(term != "(Intercept)") %>% arrange(desc(estimate))
or_tbl_fam4 <- broom::tidy(fit_noLeak_fam4, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>% filter(term != "(Intercept)") %>% arrange(desc(estimate))
or_tbl_fam5 <- broom::tidy(fit_noLeak_fam5, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>% filter(term != "(Intercept)") %>% arrange(desc(estimate))
lst <- list(or_tbl_fam1, or_tbl_fam2, or_tbl_fam3, or_tbl_fam4, or_tbl_fam5)

pick_item <- function(tb) {
  tb %>%
    filter(term != "(Intercept)") %>%
    slice(1) %>%
    transmute(
      item      = term,
      estimate  = pmax(estimate, 1e-8),
      conf.low  = pmax(conf.low, 1e-8),
      conf.high = pmax(conf.high, 1e-8)
    )
}
df_all <- bind_rows(lapply(lst, pick_item)) %>%
  mutate(item_label = item %>% str_remove("_PUNTOS$") %>% str_replace_all("_", " ") %>% str_to_sentence())

rng  <- range(c(df_all$conf.low, df_all$conf.high), na.rm = TRUE)
lims <- c(min(rng[1] * 0.9, 1/1.1), max(rng[2] * 1.1, 1.1))

p_apgar_forest <- ggplot(
  df_all %>% mutate(item_label = fct_reorder(item_label, estimate)),
  aes(y = fct_rev(item_label), x = estimate)
) +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_point(size = 2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10(limits = lims) +
  theme_minimal() +
  labs(
    title = "Dinámica familiar — Odds Ratios (IC95%) leave-one-out",
    x = "OR (escala log10)",
    y = NULL
  )
ggsave(file.path(fig_dir, "or_forest_apgar_all.png"), p_apgar_forest, width = 7, height = 4, dpi = 300)

#############################################################################
# FIN DEL SCRIPT
#############################################################################

#############################################################################
# 11) MODELOS LOGÍSTICOS – ACCIDENTE CEREBRO VASCULAR ecv ----
#############################################################################

# y “completa” (score_ecv >= 12)
df_ecv <- ecv %>% mutate(y = as.integer(score_ecv >= 12))
pred_num_ecv <- df_ecv %>% select(where(is.numeric), -contains("PUNTOS"), -score_ecv, -y) %>% names()
pred_cat_ecv <- df_ecv %>% select(-contains("PUNTOS"), -score_ecv) %>% select(where(~ !is.numeric(.))) %>% names()

df_model_ecv <- df_ecv %>%
  mutate(across(all_of(pred_cat_ecv), as.factor)) %>%
  select(y, all_of(pred_num_ecv), all_of(pred_cat_ecv)) %>%
  drop_na()

if (length(pred_num_ecv) > 0) df_model_ecv <- df_model_ecv %>% mutate(across(all_of(pred_num_ecv), scale))
if ("SEXO" %in% names(df_model_ecv)) df_model_ecv <- df_model_ecv %>% mutate(SEXO = fct_relevel(SEXO, "Femenino"))

# Diagnóstico y reagrupación
mean(df_model_ecv$y)
lapply(df_model_ecv[c("ROL","SEXO","ecvRATO","ZONA")], table)
with(df_model_ecv, table(y, ROL)); with(df_model_ecv, table(y, SEXO))
with(df_model_ecv, table(y, ecvRATO)); with(df_model_ecv, table(y, ZONA))

df_model_ecv2 <- df_model_ecv %>%
  mutate(
    ecvRATO_g = case_when(
      ecvRATO %in% c("1","2") ~ "bajo",
      ecvRATO %in% c("3","4") ~ "medio_alto",
      TRUE ~ NA_character_
    ),
    ecvRATO_g = factor(ecvRATO_g),
    ROL  = factor(ROL),
    SEXO = factor(SEXO),
    ZONA = factor(ZONA)
  )

# Modelo general
fit_glm_ecv <- glm(y ~ ecvRATO_g, data = df_model_ecv2, family = binomial("logit"))
summary(fit_glm_ecv)

# ROC/AUC (modelo general)
prob_ecv_full <- predict(fit_glm_ecv, type = "response")
roc_ecv_full  <- pROC::roc(df_model_ecv2$y, prob_ecv_full, quiet = TRUE)
png(file.path(fig_dir, "roc_ecv_general.png"), width = 1200, height = 900, res = 160)
plot(roc_ecv_full, print.auc = TRUE, legacy.axes = TRUE, main = "ROC - ECV (modelo general)")
dev.off()

# Exportar tabla del modelo general (aunque sin OR útiles si no hay significancia)
write_xlsx(
  broom::tidy(fit_glm_ecv, conf.int = TRUE) |>
    bind_cols(
      broom::glance(fit_glm_ecv) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_ecv_general.xlsx")
)

# “SIN FUGA” (resta ??? - No se han escogido las variables)
df_ecv_noLeak <- ecv %>%
  mutate(y = as.integer((score_ecv - DIFICUVIDA_PUNTOS) >= 14)) %>%
  transmute(y, SEXO, ecvRATO, EDAD, ROL, 
  ) %>%
  drop_na()

fit_noLeak_ecv <- glm(y ~ DIFICUVIDA_PUNTOS + ENFADADO_PUNTOS, data = df_ecv_noLeak, family = binomial())
summary(fit_noLeak_ecv)

# Exportar tabla (sin fuga)
write_xlsx(
  broom::tidy(fit_noLeak_ecv, conf.int = TRUE) |>
    mutate(OR = exp(ecvimate), OR_LI95 = exp(conf.low), OR_LS95 = exp(conf.high)) |>
    bind_cols(
      broom::glance(fit_noLeak_ecv) |>
        transmute(n = nobs, null.deviance, df.null, deviance, df.residual, AIC,
                  McFadden_R2 = 1 - deviance/null.deviance)
    ) |>
    mutate(across(where(is.numeric), ~ round(.x, 4))),
  path = file.path(tab_dir, "resultados_logit_ecv_sin_fuga.xlsx")
)

# OR + Forecv (sin fuga)
or_tbl_ecv_nl <- broom::tidy(fit_noLeak_ecv, conf.int = TRUE, conf.level = 0.95, exponentiate = TRUE) %>%
  filter(term != "(Intercept)") %>% arrange(desc(ecvimate))
p_or_ecv_nl <- or_tbl_ecv_nl %>%
  mutate(term = fct_reorder(term, ecvimate)) %>%
  ggplot(aes(y = term, x = ecvimate)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  scale_x_log10() +
  theme_minimal() +
  labs(title = "Odds Ratios (IC95%) - ecv (sin fuga: )",
       x = "OR (log10)", y = NULL)
ggsave(file.path(fig_dir, "or_forecv_ecv_sin_fuga.png"), p_or_ecv_nl, width = 8, height = 6, dpi = 300)

# ROC/AUC (sin fuga)
prob_ecv_nl <- predict(fit_noLeak_ecv, type = "response")
roc_ecv_nl  <- pROC::roc(df_ecv_noLeak$y, prob_ecv_nl, quiet = TRUE)
png(file.path(fig_dir, "roc_ecv_sin_fuga.png"), width = 1200, height = 900, res = 160)
plot(roc_ecv_nl, print.auc = TRUE, legacy.axes = TRUE,
     main = "ROC - ecv (sin fuga: )")
dev.off()