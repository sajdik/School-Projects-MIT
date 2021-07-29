package internal

import (
	"context"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"time"
)

//
// Database accessor interface implementation to stored the structured data in mongoDB
//

type Accessor interface {
	SaveRecord(record Record) error
	Disconnect() error
	GetAll() ([]Record, error)
}

type MongoDBAccess struct {
	client   *mongo.Client
	database string
}

//creates the mongoDB client to access mongoDB by provided connection URI and name of the database
func NewMongoDBAccess(URI, db string) (*MongoDBAccess, error) {
	client, err := mongo.NewClient(options.Client().ApplyURI(URI))
	if err != nil {
		return nil, err
	}
	log.Println("Connecting to mongoDB: ", URI)
	//make the client timeout after 5 seconds of waiting
	ctx, _ := context.WithTimeout(context.Background(), time.Second*5)
	err = client.Connect(ctx)
	if err != nil {
		return nil, err
	}
	return &MongoDBAccess{
		client:   client,
		database: db,
	}, nil
}

// save the provided record to collection "days" in mongoDB database
func (db *MongoDBAccess) SaveRecord(record Record) error {
	collection := db.client.Database(db.database).Collection("days")
	cursor := collection.FindOne(context.Background(), bson.M{"date": record.Date})
	var r bson.M
	err := cursor.Decode(&r)
	if err == mongo.ErrNoDocuments {
		_, err := collection.InsertOne(context.Background(), record)
		if err != nil {
			return err
		}

		return nil
	}
	if err != nil {
		return err
	}
	return nil
}

func (db *MongoDBAccess) Disconnect() error {
	return db.client.Disconnect(context.Background())
}

// get all records stored in "days" collection
// for debug purposes
func (db *MongoDBAccess) GetAll() ([]Record, error) {
	var records []Record
	cursor, err := db.client.Database(db.database).Collection("days").Find(context.Background(), bson.D{})
	if err != nil {
		return []Record{}, err
	}
	defer cursor.Close(context.Background())
	for cursor.Next(context.Background()) {
		var record Record
		if err = cursor.Decode(&record); err != nil {
			return []Record{}, err
		}
		records = append(records, record)
	}
	return records, nil
}
