from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


### Apply the changes made to this file to the database

# python manage.py makemigrations
# python manage.py migrate


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
        )
    author = models.CharField(null=True, max_length=100)
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, db_index=True) # harry-potter-1
    # Creating an index will make searching for that field faster
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.rating})"


### Creating the Books

# >>> from book_outlet.models import Book
# >>> harry_potter = Book(title="Harry Potter 1", rating=5)
# >>> harry_potter.save()
# >>> lord_of_the_rings = Book(title="Loard of the Rings", rating=4)
# >>> lord_of_the_rings.save()
# >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>
# >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>


### Getting the Books

# >>> from book_outlet.models import Book
# >>> Book.objects.all()
# <QuerySet [<Book: Harry Potter 1 (5)>, <Book: Loard of the Rings (4)>]>
# >>> Book.objects.all()[1].author
# >>> Book.objects.all()[1].is_bestselling
# False


### Update the data in the Database

# >>> harry_potter.author = "J.K. Rowling"
# >>> harry_potter.is_bestselling = True
# >>> harry_potter.save()


### Delete an Object

# >>> harry = Book.objects.all()[0]
# >>> harry.delete()
# (1, {'book_outlet.Book': 1})


### Create Data without saving (Quickly)

# >>> Book.objects.create(title="Harry Potter 1", rating=5, author="J.K. Rowling", is_bestselling=True)
# <Book: Harry Potter 1 (5)>
# >>> Book.objects.create(title="My Story", rating=2, author="X", is_bestselling=False)
# <Book: My Story (2)>
# >>> Book.objects.create(title="Some Random Book", rating=1, author="Some Random Dude", is_bestselling=False)
# <Book: Some Random Book (1)>
# >>> Book.objects.all()
# <QuerySet [<Book: Loard of the Rings (4)>, <Book: Harry Potter 1 (5)>, <Book: My Story (2)>, <Book: Some Random Book (1)>]>


### Querying the Data

# >>> Book.objects.get(id=3)
# <Book: Harry Potter 1 (5)>

# >>> Book.objects.get(is_bestselling=True)
# <Book: Harry Potter 1 (5)>

# >>> Book.objects.filter(is_bestselling=False)
# <QuerySet [<Book: Loard of the Rings (4)>, <Book: My Story (2)>, <Book: Some Random Book (1)>]>


### Querying the data with > < ...

# >>> Book.objects.filter(rating__lt=3)
# <QuerySet [<Book: My Story (2)>, <Book: Some Random Book (1)>]>

# >>> Book.objects.filter(rating__lt=3, title__contains="story")
# <QuerySet [<Book: My Story (2)>]>


### Using the OR in queries

# >>> from django.db.models import Q
# >>> Book.objects.filter(Q(rating__lt=3) | Q(is_bestselling=True))
# <QuerySet [<Book: Harry Potter 1 (5)>, <Book: My Story (2)>, <Book: Some Random Book (1)>]>
## Combine with AND
# >>> Book.objects.filter(Q(rating__lt=3) | Q(is_bestselling=True), Q(author="J.K. Rowling"))
# <QuerySet [<Book: Harry Potter 1 (5)>]>


### Performance!!

# bestseller = Book.objects.filter(...) ## Stored
# Amazing_bestseller = bestseller.objects.filter(...) ## Stored
# print(Amazing_bestseller)
## Only when print is called, it will actually go to the database and fetch the result
## Also the DB will cache the results of the stored queries!!! 
## (It will also cache bestseller before amazing_bestseller is called too)


### You can also bulk update, create and delete
## Check Doc



