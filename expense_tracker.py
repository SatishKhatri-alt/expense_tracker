from pymongo import MongoClient
from dotenv import load_dotenv
import os
from fastmcp import FastMCP
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
DB_NAME = os.getenv("DB_NAME")
DB_COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME")

client = MongoClient(MONGO_DB_URL)
db = client[DB_NAME]
expenses_collection = db[DB_COLLECTION_NAME]

mcp = FastMCP(name="Expense Tracker")

@mcp.tool
def add_expense(data,amount,category,date,description,notes):
    """ Function to add a new expense entry to the database."""
    expesense_data ={
        "data":data,
        "amount":amount,
        "category":category,
        "date":date,
        "description":description,
        "notes":notes
    }
    return expenses_collection.insert_one(expesense_data)

@mcp.tool
def get_expenses_by_category(category,start_date,end_date):
    """Function to retrieve expenses by category."""
    query = {
        "category":category,
        "date":{"$gte":start_date,"$lte":end_date}
    }
    return list(expenses_collection.find(query))

@mcp.tool
def get_total_expenses(start_date,end_date):
    """Function to calculate total expenses within a date range."""
    pipeline = [
        {
            "$match":{
                "date":{"$gte":start_date,"$lte":end_date}
            }
        },
        {
            "$group":{
                "_id":None,
                "total_amount":{"$sum":"$amount"}
            }
        }
    ]
    result = list(expenses_collection.aggregate(pipeline))
    return result[0]["total_amount"] if result else 0


@mcp.tool
def delete_expense(start_date,end_date):
    """Function to delete expenses within a date range."""
    query = {
        "date":{"$gte":start_date,"$lte":end_date}
    }
    result = expenses_collection.delete_many(query)
    return result.deleted_count

@mcp.tool
def update_expense(expense_id,update_fields):
    """Function to update an existing expense entry."""
    query = {"_id":expense_id}
    update = {"$set":update_fields}
    result = expenses_collection.update_one(query,update)
    return result.modified_count

if __name__ =="__main__":
    mcp.run()