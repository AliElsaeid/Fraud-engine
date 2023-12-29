from django.db import models


class Request(models.Model):
    card_number = models.CharField(max_length=12)
    ip_address = models.GenericIPAddressField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    transaction_type = models.CharField(max_length=20)

  
    status = models.CharField(max_length=20, blank=True)

   
    fraud_details = models.TextField(blank=True)

    def __str__(self):
        return f"Request {self.id} from- {self.masked_card_number()}, {self.ip_address}"

    def masked_card_number(self):
        visible_digits = 6
        masked_digits = len(self.card_number) - visible_digits
        return self.card_number[:visible_digits] + '*' * masked_digits
    


class Blacklist(models.Model):
    TYPE_CHOICES = (
        ('Card Number', 'Card Number'),
        ('Phone Number', 'Phone Number'),
        ('Email Address', 'Email Address'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.type}: {self.value}"    
    
class Whitelist(models.Model):
    TYPE_CHOICES = (
        ('Card Number', 'Card Number'),
        ('Phone Number', 'Phone Number'),
        ('Email Address', 'Email Address'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.type}: {self.value}"      

class Condition(models.Model):
    TYPE_CHOICES = (
        ('Numeric', 'Numeric'),
        ('Boolean', 'Boolean'),
        ('String', 'String'),
    )

    VARIABLE_CHOICES = (
        ('card_number', 'Card Number'),
        ('ip_address', 'IP Address'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('country', 'Country'),
        ('datetime', 'Datetime'),
        ('amount', 'Amount'),
        ('currency', 'Currency'),
        ('transaction_type', 'Transaction Type'),
    )

    OPERATOR_CHOICES = (
        ('GreaterThan', 'Greater Than'),
        ('SmallerThan', 'Smaller Than'),
        ('IsEqual', 'Is Equal'),
        ('IsNotEqual', 'Is Not Equal'),
        ('Contains', 'Contains'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    variable = models.CharField(max_length=20, choices=VARIABLE_CHOICES)
    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"Condition {self.id}: {self.type} {self.variable} {self.operator} {self.value}"
class Action(models.Model):
    CHAR_CHOICES = (
        ('Blacklist Email', 'Blacklist Email'),
        ('Blacklist Phone', 'Blacklist Phone'),
        ('Blacklist Card Number', 'Blacklist Card Number'),
        ('Reject Transaction', 'Reject Transaction'),
        ('Blacklist IP Address', 'Blacklist IP Address'),
    )

    action = models.CharField(max_length=30, choices=CHAR_CHOICES)
    
    def __str__(self):
        return f" {self.action}"

        
class Rule(models.Model):
  

    condition = models.ManyToManyField(Condition, related_name='rules')
    priority = models.IntegerField()
    actions = models.ManyToManyField(Action)

    def __str__(self):
         return f"Rule {self.id}, Priority: {self.priority}"   
    
