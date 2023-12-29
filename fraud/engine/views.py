from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Request, Whitelist, Blacklist ,Rule
from .serializers import RequestSerializer
from django.shortcuts import render

def index(request):
    return render(request , 'engine\index.html')



class RequestValidation(APIView):
    serializer_class = RequestSerializer 

    def post(self, request):
      
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            card_number = serializer.validated_data.get('card_number')
            ip_address = serializer.validated_data.get('ip_address')
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            datetime = serializer.validated_data.get('datetime')
            country=serializer.validated_data.get('country')
            amount=serializer.validated_data.get('amount')
            currency=serializer.validated_data.get('currency')
            transaction_type=serializer.validated_data.get('transaction_type') 



          
            whitelist_conditions = {
                'type__in': ['Card Number', 'Phone Number', 'Email Address'],
                'value__in': [card_number, phone, email]
            }
            whitelist_entries = Whitelist.objects.filter(**whitelist_conditions)

            if whitelist_entries.exists():
                
                Request.objects.create(
                    card_number=card_number,
                    ip_address=ip_address,
                    email=email,
                    phone=phone,
                    datetime=datetime,
                    country=country,
                    amount=amount,
                    transaction_type=transaction_type,
                    currency=currency,
                    status="accepted",
                    fraud_details="no fraud detected (whitelist)"
                )

              
                response_data = {"message": "Request accepted (whitelist)"}
                context = {'message': response_data}
                return render(request, 'engine/index.html', context)

           
            blacklist_conditions = {
                'type__in': ['Card Number', 'Phone Number', 'Email Address'],
                'value__in': [card_number, phone, email]
            }
            blacklist_entries = Blacklist.objects.filter(**blacklist_conditions)

            if blacklist_entries.exists():
                
                Request.objects.create(
                    card_number=card_number,
                    ip_address=ip_address,
                    email=email,
                    phone=phone,
                    datetime=datetime,
                    country=country,
                    amount=amount,
                    transaction_type=transaction_type,
                    currency=currency,
                    status="Rejected",
                    fraud_details="fraud detected (blacklist)"
                ) 
                response_data =  "Request rejected (blacklist)"
                context = {'message': response_data}
                return render(request, 'engine/index.html', context)

           
            new_request = Request.objects.create(
                card_number=card_number,
                ip_address=ip_address,
                email=email,
                phone=phone,
             datetime=datetime,
                    country=country,
                    amount=amount,
                    transaction_type=transaction_type,
                    currency=currency,
                    
                   
            )
            rules = Rule.objects.all().order_by('priority')

            for rule in rules:
                conditions = rule.condition.all()

             
                conditions_satisfied = all(
                  self.check_condition(condition,validated_data)
                    for condition in conditions
                )

                if conditions_satisfied:
                  
                    for action in rule.actions.all(): 
                        if action.action == 'Blacklist Email':
        
                           Blacklist.objects.create(type='Email Address', value=email)
                        elif action.action == 'Blacklist Phone':
           
                           Blacklist.objects.create(type='Phone Number', value=phone)
                        elif action.action == 'Blacklist Card Number':
           
                           Blacklist.objects.create(type='Card Number', value=card_number)
                              

                      
                    new_request.status = 'Rejected'
                    new_request.fraud_details = 'fraud detected '
                    new_request.save()
                    response_data = {"message": "Request rejected "}
                    context = {'message': response_data}
                    return render(request, 'engine/index.html', context)

            
            response_data = {"message": "Request created (no fraud detected)"}
            context = {'message': response_data}
            return render(request, 'engine/index.html', context)

          
        

       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def check_condition(self, condition, data):
        variable = condition.variable
        operator = condition.operator
        if condition.type=="Numeric":
         value = int(condition.value)
        else:
          value = condition.value    



      
        actual_value = data.get(variable)

       
        if operator == 'GreaterThan':
            return actual_value > value
        elif operator == 'SmallerThan':
            return actual_value < value
        elif operator == 'IsEqual':
            return actual_value == value
        elif operator == 'IsNotEqual':
            return actual_value != value
        elif operator == 'Contains':
            return value in actual_value
        else:
            return False
