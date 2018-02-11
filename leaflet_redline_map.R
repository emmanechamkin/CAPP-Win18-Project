library(rgdal)
library(leaflet)
library(htmltools)

chicago_redline <- rgdal::readOGR(dsn = path.expand("~/Documents/CS 122 Project Files/HOLC_Chicago.geojson"), "OGRGeoJSON")

holc_grade <- sapply(chicago_redline$features, function(feat) {feat$holc_grade})
holc_descriptions <- sapply(chicago_redline$features, function(feat) {feat$properties$area_description_data$'8'})
factpa1 <- colorFactor(c('green', 'blue', 'yellow', 'red'), unique(chicago_redline$holc_grade))

leaflet(chicago_redline) %>%
  addTiles() %>%
  addPolygons(stroke = TRUE, smoothFactor = 0.2, 
              color = 'black', opacity = 1, weight = 0.5, 
              fillColor = ~factpa1(holc_grade), fillOpacity = 0.4,
              highlightOptions = highlightOptions(color = 'white', weight = 2,
                                                  bringToFront = TRUE))
