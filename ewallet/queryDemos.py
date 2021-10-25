from django.db import models
from ewallet.models import Parent, Student, ParentWallet, StudentWallet
from django.contrib.auth.models import User

user = User.objects.get(username="Abu")


#***(1)Returns all customers from customer table
customers = Parent.objects.all()

#(2)Returns first customer in table
p = Parent.objects.first()
user.parent.name == p.user.username

user.parent.parentwallet.balance

#(3)Returns last customer in table
lastCustomer = Parent.objects.last()

#(4)Returns single customer by name
customerByName = Parent.objects.get(name='Peter Piper')

#***(5)Returns single customer by name
customerById = Parent.objects.get(id=4)

pw = ParentWallet.objects.get(pk=1)
pw.parent.name
p.parentwallet.balance

#***(6)Returns all orders related to customer (firstCustomer variable set above)
p.order_set.all()
p.studentwallet_set.all()

#(7)***Returns orders customer name: (Query parent model values)
order = StudentWallet.objects.first() 
parentName = order.customer.name

#(8)***Returns products from products table with value of "Out Door" in category attribute
# products = Product.objects.filter(category="Out Door")

#(9)***Order/Sort Objects by id
# leastToGreatest = Product.objects.all().order_by('id') 
# greatestToLeast = Product.objects.all().order_by('-id') 


#(10) Returns all products with tag of "Sports": (Query Many to Many Fields)
# productsFiltered = Product.objects.filter(tags__name="Sports")

'''
(11)Bonus
Q: If the customer has more than 1 ball, how would you reflect it in the database?
  
A: Because there are many different products and this value changes constantly you would most 
likly not want to store the value in the database but rather just make this a function we can run
each time we load the customers profile
'''

#Returns the total count for number of time a "Ball" was ordered by the first customer
ballOrders = p.order_set.filter(product__name="Ball").count()

#Returns total count for each product orderd
allOrders = {}

for order in p.order_set.all():
	if order.product.name in allOrders:
		allOrders[order.product.name] += 1
	else:
		allOrders[order.product.name] = 1

#Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}


#RELATED SET EXAMPLE
# class ParentModel(models.Model):
# 	name = models.CharField(max_length=200, null=True)

# class ChildModel(models.Model):
# 	parent = models.ForeignKey(ParentModel)
# 	name = models.CharField(max_length=200, null=True)

# parent = ParentModel.objects.first()
# #Returns all child models related to parent
# parent.childmodel_set.all()