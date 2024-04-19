import json
import easyocr
from fastapi import FastAPI
app = FastAPI()

@app.get("/get-card-data")
def card_ocr(image: str):

    reader = easyocr.Reader(['en'])
    
    results = reader.readtext(image, detail=1)

    text_list = []
    
    for (bbox, text, prob) in results:
        print(text)
        text_list.append(text)

    card_data = {}
    first_name = None
    last_name = None
    full_name = None
    sex = None
    expiration_date = None
    hair_color = None
    id_number = None
    city = None
    zip_code = None
    state = None
    country = None
    address = None
    dob = None

    adress_index = []

    for i, text in enumerate(text_list):
        if "LN" in text:
            try:
                last_name = text[2:]
            except Exception as e:
                print(str(e))

        if "FN" in text:
            try:
                first_name = text[2:]
                adress_index.append(i)
            except Exception as e:
                print(str(e))

        if "DOB" in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    dob = text_split[1]
                    card_data['data_of_birth'] = dob
                    
                adress_index.append(i)
            except Exception as e:
                print(str(e))

        if text == "DL":
            try:
                id_number = text_list[i+1]
                card_data['id_number'] = id_number
            except Exception as e:
                print(str(e))

        elif "DL " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    id_number = text_split[1]
                    card_data['id_number'] = id_number
            except Exception as e:
                print(str(e))
        
        if text == "EXP":
            try:
                expiration_date = text_list[i+1]
                card_data['expiration_date'] = expiration_date
            except Exception as e:
                print(str(e))

        elif "EXP " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    expiration_date = text_split[1]
                    card_data['expiration_date'] = expiration_date
            except Exception as e:
                print(str(e))

        if "SEX" in text:
            try:
                sex = text_list[i+1]
                card_data['sex'] = sex
            except Exception as e:
                print(str(e))

        if "HAIR" in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    hair_color = text_split[1]
                    card_data['hair_color'] = hair_color
            except Exception as e:
                print(str(e))

        if "CA " in text:
            try:
                state = "California"
                text_split = text.split(", ")
                if len(text_split) == 2:
                    city = text_split[0]
                    zip_code = text_split[1].split("CA ")[1]
                    card_data['city'] = city
                    card_data['zip_code'] = zip_code
            except Exception as e:
                print(str(e))

        if "California" in text:
            state = "California"

        if "USA" in text:
            country = "USA"

    if first_name is not None and last_name is not None:
        full_name = first_name + " " + last_name
        card_data['full_name'] = full_name
    if len(adress_index) >= 1:
        try:
            address = text_list[adress_index[0] + 1 ]
        except Exception as e:
            print(str(e))
    if len(adress_index) >= 2:
        try:
            address = address + " " + text_list[adress_index[1] -1]
        except Exception as e:
            print(str(e))

    #state = "California"
    #country = "USA"
    try:
        card_data['address'] = address
        card_data['state'] = state
        card_data['country'] = country
    except Exception as e:
        print(str(e))
        
    data_json = json.dumps(card_data, indent = 2) 

    return data_json