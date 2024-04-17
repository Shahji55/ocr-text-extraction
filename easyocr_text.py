import cv2
import easyocr
import json


def draw_approx_char_boxes(image_path):
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English language
    
    image = cv2.imread(image_path)  # Load the image with OpenCV
    
    results = reader.readtext(image_path, detail=1)  # Perform OCR

    text_list = []
    
    for (bbox, text, prob) in results:
      
        text_list.append(text)
        
        # Optionally print detected text and its confidence score
        print(f"Detected text: {text}, Confidence: {prob:.2f}")
    
    # Display the image with approximated character bounding boxes
    #cv2.imshow("Detected Text Characters", image)
    #cv2.waitKey(0)  # Wait for a key press to close the displayed image
    #cv2.destroyAllWindows()

    return text_list

def draw_boxes_and_extract_text_easyocr(image_path):
    # Create a reader to do OCR.
    reader = easyocr.Reader(['en'])  # 'en' for English, add more languages as needed
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Use EasyOCR to detect text and bounding boxes
    results = reader.readtext(image_path)
    text_list = []
    text_id = ""
    words = ["California","USA","DL","EXP","DOB 08/3101977","RSTR NONE","SEX","F","CLASS €","08311977"]
   
    # Loop through the results
    for (bbox, text, prob) in results:
        # bbox is a list of four points (top-left, top-right, bottom-right, bottom-left) for the bounding box
        # Draw the bounding box on the image
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        
        if text in words:
            text_list.append(top_left)
            text_id+=text

        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        
        # Optionally, you can also display the detected text and its confidence level
        #print(f"Detected text: {text}, Confidence: {prob:.2f}")
   
    # Show the output image
    cv2.imshow("Image with Text Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return text_list,text_id

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

    adress_index = []

    for i, text in enumerate(text_list):
        #print(i, text)

        if "LN" in text:
            last_name = text[2:]
            print(last_name)

        if "FN" in text:
            first_name = text[2:]
            print(first_name)
            adress_index.append(i)

        if "DOB" in text:
            adress_index.append(i)

        if text == "DL":
            id_number = text_list[i+1]
            print(id_number)

            card_data['id_number'] = id_number

        elif "DL " in text:
            id_number = text.split(" ")[1]
            print(id_number)

            card_data['id_number'] = id_number
        
        if text == "EXP":
            expiration_date = text_list[i+1]
            print(expiration_date)

            card_data['expiration_date'] = expiration_date

        elif "EXP " in text:
            expiration_date = text.split(" ")[1]
            print(expiration_date)

            card_data['expiration_date'] = expiration_date

        if "SEX" in text:
            sex = text_list[i+1]
            print(sex)

            card_data['sex'] = sex

        if "HAIR" in text:
            hair_color = text.split(" ")[1]
            print(hair_color)

            card_data['hair_color'] = hair_color

        if "CA " in text:
            print(text)

            text_split = text.split(", ")
            print(text_split)

            city = text_split[0]
            print(city)

            zip_code = text_split[1].split("CA ")[1]
            print(zip_code)

            card_data['city'] = city
            card_data['zip_code'] = zip_code

    if first_name is not None and last_name is not None:
        full_name = first_name + " " + last_name
        print(full_name)

        card_data['full_name'] = full_name

    print("Adress index: ", adress_index)
    address = text_list[adress_index[0] + 1 ] + " " + text_list[adress_index[1] -1]
    print(address)

    state = "California"
    country = "USA"

    card_data['address'] = address
    card_data['state'] = state
    card_data['country'] = country

    #print(card_data)

    return card_data


if __name__ == "__main__":
    #image_path = 'real_id.jpg'
    #image_path = 'real_id_2.jpg'
    image_path = '4.jpg'

    #text_list,text_id = draw_boxes_and_extract_text_easyocr(image_path)

    text_list = draw_approx_char_boxes(image_path)

    #print(text_list)

    # for text in text_list:
    #     print(text, type(text))

    final_card_data = prepare_data(text_list)
    print(final_card_data)

    #data_json = json.dumps(final_card_data, indent = 2) 
    #print(data_json) 