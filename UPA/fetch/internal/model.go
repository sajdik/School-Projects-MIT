package internal

//
// Model definition and structure of data/document to be stored in mongodb
//

type Currency struct {
	Name string  `json:"name, omitempty"`
	Rate float64 `json:"rate, omitempty"`
}

type Record struct {
	Currencies []Currency `json:"currencies, omitempty"`
	Date       string     `json:"date, omitempty"`
}
