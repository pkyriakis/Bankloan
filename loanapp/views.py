from rest_framework.response import Response
from rest_framework.views import APIView
import json
from loanapp.models import Application, Business, Owner, Address


# View for the loanapp/ endpoint
class LoanAppView(APIView):
    def get(self, request, format=None):
        return Response({'error': 'Cannot handle request'})

    # Helper function that updates an address object from the given JSON
    def _get_addr(self, addr, addr_json):
        addr.address1 = addr_json["Address1"]
        addr.address2 = addr_json["Address2"]
        addr.state = addr_json["State"]
        addr.city = addr_json["City"]
        addr.zip_code = addr_json["Zip"]
        addr.save()

    def post(self, request, format=None):
        # Get json data
        json_data = json.loads(request.body)
        req_header_json = json_data["RequestHeader"]
        business_json = json_data["Business"]
        owners_json = json_data["Owners"]
        app_data_json = json_data["CFApplicationData"]
        business_addr_json = business_json["Address"]

        # Find database entries with same tax id
        # We use tax id to detect multiple applications
        application_updated = False # True if application already existed
        bus_query = Business.objects.filter(tax_id=business_json["TaxID"])
        if bus_query.count() > 0:
            # Application exists; retrieve it
            business = bus_query[0]
            app = Application.objects.filter(business_id=business.id)[0]
            business_addr = business.address
            application_updated = True
        else:
            # Does not exist; create new application
            business = Business()
            app = Application()
            business_addr = Address()

        # Set/update business address
        self._get_addr(business_addr, business_addr_json)

        # Set/update business model
        business.name = business_json["Name"]
        business.annual_revenue = business_json["SelfReportedCashFlow"]["AnnualRevenue"]
        business.monthly_average_balance = business_json["SelfReportedCashFlow"]["MonthlyAverageBankBalance"]
        business.monthly_average_credit_card_volume = business_json["SelfReportedCashFlow"][
            "MonthlyAverageCreditCardVolume"]
        business.address = business_addr
        business.tax_id = business_json["TaxID"]
        business.phone = business_json["Phone"]
        business.naics = business_json["NAICS"]
        business.has_been_profitable = business_json["HasBeenProfitable"]
        business.has_bunkrupted = business_json["HasBankruptedInLast7Years"]
        business.inception_date = business_json["InceptionDate"]
        business.save()

        # Set up owners models
        owners = []
        owners_perc = []
        for owner_json in owners_json:
            if application_updated:
                owner = app.owners.get_queryset().filter(email=owner_json["Email"])
                if owner.count() < 1:
                    owner = Owner()
                else:
                    owner = owner[0]
            else:
                owner = Owner()
            owner.name = owner_json["Name"]
            owner.first_name = owner_json["FirstName"]
            owner.last_name = owner_json["LastName"]
            owner.email = owner_json["Email"]
            home_addr_json = owner_json["HomeAddress"]
            if application_updated:
                home_addr = owner.home_address
            else:
                home_addr = Address()
            self._get_addr(home_addr, home_addr_json)
            owner.home_address = home_addr
            owner.date_of_birth = owner_json["DateOfBirth"]
            owner.home_phone = owner_json["HomePhone"]
            owner.ssn = owner_json["SSN"]
            owner.save()
            owners.append(owner)
            owners_perc.append(owner_json["PercentageOfOwnership"])

        # Set up application model
        app.cf_request_id = req_header_json["CFRequestId"]
        app.request_date = req_header_json["RequestDate"]
        app.cf_api_user_id = req_header_json["CFApiUserId"]
        app.cf_api_password = req_header_json["CFApiPassword"]
        app.is_test_lead = req_header_json["IsTestLead"]
        app.request_load_amount = app_data_json["RequestedLoanAmount"]
        app.stated_credit_history = app_data_json["StatedCreditHistory"]
        app.legal_entity_type = app_data_json["LegalEntityType"]
        app.filter_id = app_data_json["FilterID"]
        app.business = business
        app.owners_percentage = owners_perc.__str__()
        app.application_updated = application_updated
        app.save()
        # Add onwers
        for owner in owners:
            app.owners.add(owner)
        app.save()


        res = "received"
        if application_updated :
            res = "updated"
        return Response({'application-id': app.cf_request_id, 'application-status': 'application_' + res})


# View for the status/ endpoint
class StatusView(APIView):

    def get(self, request, cf_request_id):
        app = Application.objects.filter(cf_request_id=cf_request_id)
        if app.count() > 0:
            return Response({'application-id': cf_request_id, 'application-status': app[0].status})
        else:
            return Response({'error': 'application not found'})
