library(tidyverse)
library(caret)
library(cluster)
library(dplyr)

movies <- read.csv("recommendation.csv")
movies$movie_id <- paste0("id.", movies$movie_id)
movie_distance <- movies[1:10000,c('movie_id', 'genre', 'averageRating')]

movie_distance$movie_id <- as.factor(movie_distance$movie_id)
movie_distance$genre <- as.factor(movie_distance$genre)
movie_distance$averageRating <- as.factor(movie_distance$averageRating)

dissimilarity <- daisy(movie_distance, metric = "gower", weights = c(2, 1, 0.7))
dissimilarity <- as.matrix(dissimilarity)
row.names(dissimilarity) <- movies$movie_id[1:10000]
colnames(dissimilarity) <- movies$movie_id[1:10000]


dissimilarity[1:10, 1:10]

selected_movie <- data.frame(movie_id = c('id.7329858', 'id.1012756', 'id.448115', 'id.6532374', 'id.1001125'), rating = c(3,6,2,7,5))

recomendar <- function(selected_movies, dissimilarity_matrix, movies, n_recommendation = 5){
  selected_movie_indexes <- which(colnames(dissimilarity_matrix) %in% selected_movies$movie_id)
  results <- data.frame(dissimilarity_matrix[, selected_movie_indexes], 
                       recommended_movie = row.names(dissimilarity_matrix),
                       stringsAsFactors = FALSE)

  recomendaciones <- results %>% 
    pivot_longer(cols = c(- "recommended_movie"), names_to = "watched_movie",
                 values_to = "dissimilarity") %>%
    left_join(selected_movies, by = c("watched_movie" = "movie_id")) %>%
    arrange(desc(dissimilarity)) %>%
    filter(recommended_movie != watched_movie) %>%
    filter(!is.na(rating)) %>%
    mutate(
      similarity = 1 - dissimilarity,
      weighted_score = similarity * rating) %>% 
    arrange(desc(weighted_score > 0)) %>%
    group_by(recommended_movie) %>% slice(1) %>%
    arrange(desc(weighted_score))
   
  return(recomendaciones[1:n_recommendation,])
}

res <- recomendar(selected_movie, dissimilarity, movies)
res2 <- data.frame(movie_id = substring(res$recommended_movie, 4))
write.csv(res2, "recommanded_movies.csv", row.names = FALSE)
