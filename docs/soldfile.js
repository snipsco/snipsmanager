var Sold = require('sold')

Sold(__dirname) // create new instance in root directory
    .data({
    }) // set custom data for blog
    .engine("ejs")
    .source("src") // set the source for where the markdown files are stored (default is src)
    .destination("build") // set destination path for build files (default is build)
    .build() // build when everything is done