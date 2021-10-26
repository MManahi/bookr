from django.db import models
from django.contrib import auth


# Create your models here.

class Publisher(models.Model):
    """A model for the company that publishes books"""
    name = models.CharField(max_length=50, help_text="The publisher's name")
    website = models.URLField(help_text="The publisher website")
    email = models.EmailField(help_text="The publisher's email")

    def __str__(self):
        return self.name


class Book(models.Model):
    """A model for the published book"""
    title = models.CharField(max_length=70, help_text="The title of the book")
    publication_date = models.DateField(verbose_name="Date of book publication")
    isbn = models.CharField(max_length=20, verbose_name="ISBN identifier of the book")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor', through='BookContributor')

    def __str__(self):
        return "{} {}".format(self.title, self.isbn)


class Contributor(models.Model):
    """A model for any contributor to the book (e.g. author, co-author, editor)"""
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names")
    last_names = models.CharField(max_length=50, help_text="The contributor's last name or names")
    email = models.EmailField(help_text="The contact email for the contributor")

    def __str__(self):
        return "{} {}".format(self.first_names, self.last_names)


class BookContributor(models.Model):
    """ A model to manage the manage many-to-many relationship between Book and Contributor"""

    class ContributionRole(models.TextChoices):
        AUTHOR = 'AUTHOR', 'Author'
        CO_AUTHOR = 'CO-AUTHOR', 'Co-Author'
        EDITOR = "EDITOR", 'Editor'

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name='The role this contributor had in the book.',
                            choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    """ A model for the book reviews """
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review was created.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book that this review is for.")

    def __str__(self):
        return self.content
