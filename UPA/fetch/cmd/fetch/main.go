package main

import (
	"flag"
	"github.com/MarekSalgovic/UPA2020/fetch/internal"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
)

//function to fetch content of the source data url to string for later use
// the size of data source is small enough to store it all in memory at once to work on without segmenting the input
// this makes the function simpler
func getDataFromSource(url string) (string, error) {
	// GET request
	response, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer response.Body.Close()

	// was the HTTP response code 200, if not exit
	if response.StatusCode == http.StatusOK {

		//read the reponse body(data in raw plain text) and return it
		body, err := ioutil.ReadAll(response.Body)
		if err != nil {
			return "", err
		}
		return string(body), nil
	}
	return "", nil
}

func main() {

	mongoUri := flag.String("mongo", "mongodb://mongo-service:27017", "a string containing mongo uri")
	//initial setup

	sourceUrl := flag.String("url", "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/rok.txt", "an url containing data")
	fetchYear := flag.String("year", "2020", "a year")

	flag.Parse()

	//create mongo DB client to access the database
	access, err := internal.NewMongoDBAccess(*mongoUri, "upa")
	if err != nil {
		log.Fatalln(err)
	}

	defer access.Disconnect()

	//download the data to memory
	data, err := getDataFromSource(*sourceUrl + "?rok=" + *fetchYear)
	if err != nil {
		log.Fatalln(err)
	}

	//create parser to modify the raw plain text into structured data which can be stored in documents
	parser, err := internal.NewParser(data)
	if err != nil {
		log.Fatalln(err)
	}
	records, err := parser.Parse()
	if err != nil {
		log.Fatalln(err)
	}

	//save each parsed record
	for _, r := range records {
		err := access.SaveRecord(r)
		if err != nil {
			log.Fatalln(err)
		}
	}
	log.Println(strconv.Itoa(len(records))+" records saved.")
}
