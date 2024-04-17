from google.cloud import vision
from google.protobuf.json_format import MessageToJson

def detect_text(path):
    """Detects text in the file."""
    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    # json_response = MessageToJson(response._pb)

    # # save response_json as a .json file
    # with open('response.json', 'w') as json_file:
    #     json_file.write(json_response)
        
    texts = response.text_annotations

    texts = texts[0].description
    texts = texts.split('\n')
    print(texts)

    text_list = []
    for text in texts:
        print("text: ", text)
        text_list.append(text)
        #print(". ", text.description)
        #text_list.append(text.description)
        #print(f'\n"{text.description}"')
        
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return text_list

def prepare_data(text_list):

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

        if "DOB " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    dob = text_split[1]
                    card_data['data_of_birth'] = dob
                    adress_index.append(i)
            except Exception as e:
                print(str(e))

        if "DL " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    id_number = text_split[1]
                    card_data['id_number'] = id_number
            except Exception as e:
                print(str(e))
        
        if "EXP " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    expiration_date = text_split[1]
                    card_data['expiration_date'] = expiration_date
            except Exception as e:
                print(str(e))

        if "SEX " in text:
            try:
                text_split = text.split(" ")
                if len(text_split) == 2:
                    sex = text_split[1]
                    card_data['sex'] = sex
            except Exception as e:
                print(str(e))

        if "HAIR " in text:
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

    try:
        card_data['address'] = address
        card_data['state'] = state
        card_data['country'] = country
    except Exception as e:
        print(str(e))

    return card_data

if __name__ == "__main__":
    image_path = 'real_id.jpg'
    #image_path = '5.jpg'
    #image_path = "cam_license.jpg"

    text_list = detect_text(image_path)

    print("\nText list: ", text_list)

    card_data = prepare_data(text_list)

    print("\nCard data: ", card_data)