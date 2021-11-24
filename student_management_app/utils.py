import unidecode
 
def remove_accent(text):
    return unidecode.unidecode(text)

def ten_image_students(argument):
    number_image = int(argument)
    if number_image < 10:
        number = 10 - number_image
        return f"You add less than {number} images!"
    elif number_image > 10:
        number = number_image - 10
        return f"You add more than {number} images"
    return ""