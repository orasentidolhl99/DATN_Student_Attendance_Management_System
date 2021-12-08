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


def datetime_counter(dict_check):
    	return [
		{	
			'student_id': str(key),
			'datetime': min(value) if len(value) > 0 else None,
			'counter': len(value) if len(value) > 0 else None
		} for key, value in dict_check.items()
	]