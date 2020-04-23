from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


#setting the intended budget
class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    budget_author = models.ForeignKey(User, on_delete=models.CASCADE) #User
    

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save()

# amount being spent
class MonthlyBudget(models.Model):
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE)
    month = models.DateField()
    planned = models.DecimalField(max_digits=65, decimal_places=2)
    actual = models.DecimalField(max_digits=65, decimal_places=2)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    budget_author = models.ForeignKey(User, on_delete=models.CASCADE) #User

    def __str__(self):
        return self.slug
    
    def save(self, *args, **kwargs):
        forslug = "{0.budget}-{0.month}".format(self)
        self.slug = slugify(forslug)
        super(MonthlyBudget, self).save()
