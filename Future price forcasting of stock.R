# Clear the workspace
rm(list=ls())
cat("\014")

# set working directory
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

#data cleanup
library(dplyr)
library(tidyr)
library(magrittr)
library(stringr)
library(lubridate)

#API and json
library(httr)
library(jsonlite)
library(config)

#Web Scraping
library(rvest)

#Visualization
library(plotly)

#Data
library(gtrendsR)

#Text Analysis
library(tidytext)
library(textdata)
library(wordcloud)

#Forecasting
library(quantmod)
library(forecast)
library(tseries)
library(prophet)


# Gathering Price Movement data from Yahoo Finance via quantmod
symbol <- 'TGT'
config <- config::get()
date_from <- format(today()-dyears(5), "%Y-%m-%d")

price_movement <- getSymbols(c(symbol), from = date_from, env = NULL) %>%
 data.frame(symbol,index(.),.)

colnames(price_movement) <- c('name','date','open','high','low','close','volume','adjusted')
rownames(price_movement) <- NULL


# Get company name from symbol
company <- paste0("https://www.marketwatch.com/investing/stock/",symbol) %>%
  read_html() %>%
  html_element('.company__name') %>%
  html_text() %>%
  as.character()


# Plotting ticker price movement data with plotly

p1 <- price_movement %>%
  plot_ly(x = ~date,
          type = "candlestick", 
          open = ~open, 
          close = ~close, 
          high = ~high,
          low = ~low,
          name = "Price") %>%
  layout(
    xaxis = list(
      rangeselector = list(
        buttons = list(
          list(count = 1, label = "1 mo", step = "week", stepmode = "backward"),
          list(count = 3, label = "3 mo", step = "month", stepmode = "backward"),
          list(count = 6, label = "6 mo", step = "month", stepmode = "backward"),
          list(count = 1, label = "1 yr", step = "year", stepmode = "backward"),
          list(count = 3, label = "3 yr", step = "year", stepmode = "backward"),
          list(step = "all"))),
      rangeslider = list(visible = FALSE)),
    yaxis = list(title = "Price ($)", showgrid = TRUE, showticklabels = TRUE))

p2 <- price_movement %>%
  plot_ly(x=~date, y=~volume, type='bar', name = "Volume") %>%
  layout(yaxis = list(title = "Volume"))

p <- subplot(p1, p2, heights = c(0.7,0.3), nrows=2,
             shareX = TRUE, titleY = TRUE) %>%
  layout(title = paste(symbol,'-',company))
p


# Google Search Trends Analysis

trends <- gtrends(keyword = company, onlyInterest = TRUE) %>%
  .$interest_over_time %>%
  as.data.frame() %>%
  select(c(date, hits, keyword))


trends$date <- as_date(ceiling_date(trends$date, unit = "weeks", 
                                    change_on_boundary = NULL,
                                    week_start = getOption("lubridate.week.start", 1)))


# Interest over time plot
p3 <- trends %>%  
  plot_ly(x=~date, y=~hits, mode = 'lines', 
          name = "Google Search Trends", type = 'scatter') %>%
  layout(yaxis = list(title = "Interest on 0-100 scale"))

p <- subplot(p1, p2, p3, heights = c(0.5,0.25,0.25), nrows=3,
             shareX = TRUE, titleY = TRUE) %>%
  layout(title = paste(symbol,'-',company))
p


############################
# Fetching recent stock news
############################

# Google News API Query
url_news = paste0("https://newsapi.org/v2/everything?q=",
                  str_replace_all(company, pattern = " ", replacement = "%20"),
                  "&from=",today()-ddays(30),
                  "&sortBy=relevance&pageSize=100&language=en&apiKey=",
                  config$api.newsapi.key)


# Call URL extract dataframe from JSON
results <- GET(url = url_news)
news <- content(results, "text")
news %<>%
  fromJSON(flatten = TRUE) %>%
  as.data.frame() %>%
  select(c(articles.title, articles.description, articles.content, articles.publishedAt))


###############
# Text Analysis
###############

news_words <- news %>%
  unnest_tokens(word, articles.description) %>%
  filter(!word %in% append(stop_words$word, values = "chars"), str_detect(word, "^[a-z']+$"))


# Word cloud analysis
words_only <- news_words %>%
  count(word, sort =TRUE)

wordcloud(words = words_only$word, freq = words_only$n,
          max.words=50, colors=brewer.pal(8, "Dark2"))


# Positive or Negative analysis
afinn <- get_sentiments("afinn")

news_words$date = as_date(news_words$articles.publishedAt)

sentiment_summary <- news_words %>%
  left_join(afinn) %>%
  filter(!is.na(value)) %>%
  group_by(articles.title, date) %>%
  summarise(value = mean(value)) %>%
  mutate(sentiment = ifelse(value>0, "positive","negative")) 

ggplot(sentiment_summary, aes(date, value)) + 
  geom_bar(stat = "identity", aes(fill=sentiment))  + 
  ggtitle(paste0(symbol, ": News Sentiment Over Time")) 


######################################################
# Time Series Forecasting using Facebook Prophet model
######################################################

# pre-processing
df <- price_movement %>%
  select(c("date","close")) %>%
  rename(ds = date, y = close)

# predictions
m <- prophet(df, daily.seasonality=TRUE)
future <- make_future_dataframe(m, periods = 365) %>% 
  filter(!wday(ds) %in% c(1,7))
forecast <- predict(m, future)

# Prophet Forecast Results
plot(m, forecast, xlabel = "date", ylabel = "stock close price ($)") + 
  ggtitle(paste0(symbol, ": Stock Price Prediction"))


# Forecast Evaluation
forecast$ds <- as_date(forecast$ds)

residuals <- df %>% 
  left_join(forecast[c('ds','yhat','yhat_lower','yhat_upper')], by = "ds") %>%
  filter(ds < today()) %>%
  mutate(res = (y-yhat))

ggplot(residuals, aes(ds, res)) + 
  geom_point() + 
  geom_hline(yintercept =0, color = "red") + 
  labs(title ="Prophet Forecasting Residuals", x = "date", y = "residual")
