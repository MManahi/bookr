# default admin site
from django.contrib import admin

# custom admin site
from django.contrib.admin import AdminSite
from reviews.models import Review, Publisher, Book, Contributor, BookContributor


class BookAdmin(admin.ModelAdmin):
    # adds custom date hierarchy to the admin panel
    date_hierarchy = 'publication_date'

    # list attributes for admin panel
    list_display = ('title', 'isbn13')

    # display isbn format
    def isbn13(self, obj):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4],
                                       obj.isbn[4:6], obj.isbn[6:12],
                                       obj.isbn[12:13])

    # list filters for admin panel
    list_filter = ('publisher', 'publication_date')

    # adds search fields to the admin panel
    search_fields = ('title', 'isbn', 'publisher__name')


class ReviewAdmin(admin.ModelAdmin):
    # excludes field in the admin panel
    exclude = ('date_edited',)

    # splits fields in the admin ui
    fieldsets = (('Linkage', {'fields': ('creator', 'book')}),
                 ('Review content',
                  {'fields': ('content', 'rating')}))


class ContributorAdmin(admin.ModelAdmin):
    # list attributes for admin panel
    list_display = ('last_names', 'first_names')

    # list filters for admin panel
    list_filter = ('last_names',)

    # adds search fields to the admin panel
    search_fields = ('first_names__startswith', 'last_names')


# default registration of models here.
admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
