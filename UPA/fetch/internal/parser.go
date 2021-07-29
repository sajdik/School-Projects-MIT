package internal

import (
	"strconv"
	"strings"
)

//
// Parser interface implementation to modify the input raw plain text into defined models which can be stored in mongo
//

type currency struct {
	amount int
	name   string
}

type ParseData struct {
	Currencies []currency
	lines      []string
}

type Parser interface {
	getCurrencies(line string) error
}

//
// Initialize the parser
// the first line of datasource defines the index of different currencies
// the rest of the lines is the desired data
//
func NewParser(data string) (*ParseData, error) {
	parser := ParseData{}
	lines := strings.Split(data, "\n")
	parser.lines = lines[1:]
	err := parser.getCurrencies(lines[0])
	if err != nil {
		return nil, err
	}
	return &parser, nil
}

//
// get the index of each currency defined in the first line
//
func (parser *ParseData) getCurrencies(line string) error {
	currencies := strings.Split(line, "|")
	for i := 1; i < len(currencies); i++ {
		split := strings.Split(currencies[i], " ")
		amount, err := strconv.Atoi(split[0])
		if err != nil {
			return err
		}

		parser.Currencies = append(parser.Currencies, currency{
			amount: amount,
			name:   split[1],
		})
	}
	return nil
}

//
// parse the body
//

func (parser *ParseData) Parse() ([]Record, error) {
	records := []Record{}
	for _, line := range parser.lines {
		currenciesArray := []Currency{}
		currencies := strings.Split(line, "|");
		date := currencies[0]
		currencies = currencies[1:]
		if len(currencies) == len(parser.Currencies) {
			for i, k := range parser.Currencies {

				currencies[i] = strings.Replace(currencies[i], ",", ".", -1)
				currencyFloat, err := strconv.ParseFloat(currencies[i], 64)
				if err != nil {
					return nil, err
				}
				currency := Currency{
					Name: k.name,
					Rate: currencyFloat / float64(k.amount),
				}
				currenciesArray = append(currenciesArray, currency)
			}
			record := Record{
				Currencies: currenciesArray,
				Date:       date,
			}
			records = append(records, record)
		}

	}
	return records, nil
}
