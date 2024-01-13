from typing import Union, Optional

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class Customer(BaseModel):
    customer_id: str
    country: str

class URLLink(BaseModel):
    url: str

class Invoice(BaseModel):
    invoice_no: int
    invoice_date: str
    customer: Optional[URLLink] = None

fakeInvoiceTable = dict()


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/customer")
async def create_customer(item: Customer):

    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data, status_code=201)



@app.get("/customer/{customer_id}")
def read_customer(customer_id: str):

    if customer_id == "12345":

        item = Customer(customer_id= "12345", country="Germany")

        json_compatible_item_data = jsonable_encoder(item)

        return JSONResponse(content=json_compatible_item_data)
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


@app.post("/customer/{customer_id}/invoice")
async def create_invoice(customer_id: str, invoice: Invoice):

    invoice.customer.url = "/customer/" + customer_id

    jsonInvoice = jsonable_encoder(invoice)
    fakeInvoiceTable[invoice.invoice_no] = jsonInvoice

    ex_invoice = fakeInvoiceTable[invoice.invoice_no.invoice_no]

    return JSONResponse(content=ex_invoice)


# Return all invoices for a customer
@app.get("/customer/{customer_id}/invoice")
async def get_invoices(customer_id: str):
    
    # Create Links to the actual invoice (get from DB)
    ex_json = { "id_123456" : "/invoice/123456",
                "id_789101" : "/invoice/789101" 
    }
    return JSONResponse(content=ex_json) 


# Return a specific invoice
@app.get("/invoice/{invnoice_no}")
async def read_invoice(invnoice_no: int):
    # Option to manually create an invoice
        #ex_inv = Invoice(invoice_no = invnoice_no, invoice_date= "2021-01-05", customer= URLLink(url = "/customer/12345"))
        #json_compatible_item_data = jsonable_encoder(ex_inv)
    
    # Read invoice from the dictionary
    ex_invoice = fakeInvoiceTable[invnoice_no]

    # Return the JSON that we stored
    return JSONResponse(content=ex_invoice)


#get a specific stock code on the invoice
@app.get("/invoice/{invnoice_no}/{stockcode}/")
async def read_item(invnoice_no: int,stockcode: str):
    return {"message": "Hello World"}

# Add a stockcode to the inovice
@app.post("/invoice/{invnoice_no}/{stockcode}/")
async def add_item(invnoice_no: int ,stockcode:str):
    return {"message": "Hello World"}