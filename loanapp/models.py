from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Address Model - Stores the physical address of an entity
class Address(models.Model):
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024, null=True, blank=True)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=3)

    def __str__(self):
        return self.address1


# Owner Model - Stores data related to a business owner/user
class Owner(models.Model):
    name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    home_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    home_phone = PhoneNumberField()
    ssn = models.IntegerField()

    def __str__(self):
        return self.name


# Business Model - Stores data related to a company/business
class Business(models.Model):
    name = models.CharField(max_length=20)
    tax_id = models.IntegerField()
    annual_revenue = models.FloatField()
    monthly_average_balance = models.FloatField()
    monthly_average_credit_card_volume = models.FloatField()
    phone = PhoneNumberField()
    naics = models.IntegerField()
    has_been_profitable = models.BooleanField()
    has_bunkrupted = models.BooleanField()
    inception_date = models.DateTimeField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Application Model - Stores data related to a loan application
class Application(models.Model):
    cf_request_id = models.IntegerField()
    request_date = models.DateTimeField()
    cf_api_user_id = models.CharField(max_length=20,null=True)
    cf_api_password = models.CharField(max_length=20,null=True)
    is_test_lead = models.BooleanField()
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    owners = models.ManyToManyField('Owner')
    owners_percentage = models.CharField(max_length=20)
    request_load_amount = models.FloatField()
    stated_credit_history = models.BooleanField()
    legal_entity_type = models.CharField(max_length=10)
    filter_id = models.IntegerField()
    status = models.CharField(max_length=10, default='processing')
    updated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cf_request_id)



