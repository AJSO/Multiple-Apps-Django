from django.db import models
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel
import datetime
from django.contrib.auth.models import User


from mybudget.models import MonthlyBudget, Budget
from accounts.models import Account

class Transaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=65, decimal_places=2)
    balance = models.DecimalField(max_digits=65, decimal_places=2)
    beneficiary = models.CharField(max_length=50)
    budget = models.ForeignKey(MonthlyBudget, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE)
    debit = models.BooleanField(default=True)
    transfer = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    transaction_author = models.ForeignKey(User, on_delete=models.CASCADE) #User

    def __str__(self):
        return self.slug
    
    def save(self, *args, **kwargs):
        time = datetime.datetime.now().time().strftime("%H%M%S") #Add the hour, min, and second to the slug to avoid Unique constraint conflicts
        forslug = "{0.date}-{1}-{0.account}-{0.amount}".format(self, time)
        self.slug = slugify(forslug)
        super(Transaction, self).save()

class Category(models.Model):
    name = models.CharField(max_length=50)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #User

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.slug