from django.core.validators import RegexValidator

class Validation:
    validate_item = RegexValidator(
        '^Fiji Water:[0-9]*;Campbell Soup:[0-9]*;First Aid Pouch:[0-9]*;AK47:[0-9]*$',
        "Correct stock declaration format: 'Fiji Water:x;Campbell Soup:x;First Aid Pouch:x;AK47:x'"
        "(include all fields even if you have 0)"
    )
    validate_gender = RegexValidator('[MFO]', 'M, F or O')
    validate_name = RegexValidator(
        '^[a-zA-Z ]{2,70}$',
        "Name must be 2 to 70 characters long and alphabetical"
    )
    validate_pk = RegexValidator('^[0-9]*', 'Value must be numeric')
    price_dict = {
        'Fiji Water': '14',
        'Campbell Soup': '12',
        'First Aid Pouch': '10',
        'AK47': '8',
    }