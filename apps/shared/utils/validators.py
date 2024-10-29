from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+(998|7|1|93|355|213|)\d{9,15}$',
    message="Phone number must be entered in the format: '+<country_code><number>'. The number must start with the appropriate country code followed by 9 to 15 digits."
)
