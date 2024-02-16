from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

class Discount(models.Model):

    percentage = models.IntegerField(help_text='Percentage of discount')
    # product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True, help_text='Start date of the discount')
    end_date = models.DateField(null=True, blank=True, help_text='End date of the discount')



class Product(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the medication')
    generic_name = models.CharField(max_length=255, help_text='Generic name of the medication')
    form = models.CharField(max_length=255, help_text='Form of the medication (e.g., tablet, capsule, liquid)')
    strength = models.CharField(max_length=255, help_text='Strength of the medication (e.g., 500mg)')
    factory_company = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    pharmacy = models.ForeignKey('pharmacy.Pharmacy', on_delete=models.CASCADE)
    quentity = models.IntegerField(null=True, blank=True)   
    image = models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return self.name



