from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models import (
    Author,
    Book,
    Holding,
    Lending,
    Library,
    Publisher,
    Renewing,
    Reservation,
    Stock,
    Translator,
    User
)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('get_publisher_number', 'name', 'address')
    list_display_links = ('get_publisher_number', 'name')
    search_fields = ('name', 'address')

    def get_publisher_number(self, publisher):
        return publisher.id
    get_publisher_number.admin_order_field = 'id'
    get_publisher_number.short_description = '出版者番号'


class BookAdmin(admin.ModelAdmin):
    class AuthorsInline(admin.TabularInline):
        model = Book.authors.through
        verbose_name = '著者'
        raw_id_fields = ('author', )
        extra = 1

    class TranslatorsInline(admin.TabularInline):
        model = Book.translators.through
        verbose_name = '訳者'
        raw_id_fields = ('translator', )
        extra = 1

    list_display = (
        'get_book_number',
        'name',
        'get_authors',
        'get_translators',
        'get_publisher_name',
        'publication_date',
        'size',
        'page',
        'isbn'
    )
    list_display_links = ('get_book_number', 'name')
    search_fields = ('name', 'publisher', 'isbn')
    raw_id_fields = ('publisher', )
    inlines = (AuthorsInline, TranslatorsInline)

    def get_book_number(self, book):
        return book.id
    get_book_number.admin_order_field = 'id'
    get_book_number.short_description = ' 書籍番号'

    def get_authors(self, book):
        return ', '.join(author.name for author in book.authors.all())
    get_authors.short_description = '著者'

    def get_translators(self, book):
        return ', '.join(
            translator.name for translator in book.translators.all()
        )
    get_translators.short_description = '訳者'

    def get_publisher_name(self, book):
        return book.publisher.name
    get_publisher_name.admin_order_field = 'publisher__name'
    get_publisher_name.short_description = '出版者'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('get_author_number', 'name', 'get_authed_books')
    list_display_links = ('get_author_number', 'name')
    search_fields = ('name', )
    exclude = ('books', )

    def get_author_number(self, author):
        return author.id
    get_author_number.admin_order_field = 'id'
    get_author_number.short_description = '著者番号'

    def get_authed_books(self, author):
        return None if not author.books.exists() \
          else ', '.join(book.name for book in author.books.all()[:5])
    get_authed_books.short_description = '著書 (5冊まで)'


class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('get_translator_number', 'name', 'get_translated_books')
    list_display_links = ('get_translator_number', 'name')
    search_fields = ('name', )
    exclude = ('books', )

    def get_translator_number(self, translator):
        return translator.id
    get_translator_number.admin_order_field = 'id'
    get_translator_number.short_description = '訳者番号'

    def get_translated_books(self, translator):
        return None if not translator.books.exists() \
          else ', '.join(book.name for book in translator.books.all()[:5])
    get_translated_books.short_description = '訳書 (5冊まで)'


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('get_library_number', 'name', 'address')
    list_display_links = ('get_library_number', 'name')
    search_fields = ('name', 'address')

    def get_library_number(self, library):
        return library.id
    get_library_number.admin_order_field = 'id'
    get_library_number.short_description = '図書館番号'


class StockAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_number',
        'get_book_name',
        'get_book_isbn',
        'get_library_name',
        'get_lending_actual_due_date',
        'get_holding_expiration_date',
        'get_reservations_count'
    )
    list_filter = ('library__name', )
    search_fields = ('id', 'book__name', 'book__isbn')
    raw_id_fields = ('book', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reservations_count=Count('reservations')
        )
        return queryset

    def get_readonly_fields(self, request, obj=None):
        return ('book', ) if obj \
          else ()

    def get_stock_number(self, stock):
        return stock.id
    get_stock_number.admin_order_field = 'id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, stock):
        return stock.book.name
    get_book_name.admin_order_field = 'book__name'
    get_book_name.short_description = '書名'

    def get_book_isbn(self, stock):
        return stock.book.isbn
    get_book_isbn.admin_order_field = 'book__isbn'
    get_book_isbn.short_description = 'ISBN'

    def get_library_name(self, stock):
        return stock.library.name
    get_library_name.admin_order_field = 'library__name'
    get_library_name.short_description = '配架先'

    def get_lending_actual_due_date(self, stock):
        return stock.lending.actual_due_date()
    get_lending_actual_due_date.short_description = '返却期限 (延長含む)'

    def get_holding_expiration_date(self, stock):
        return stock.holding.expiration_date
    get_holding_expiration_date.admin_order_field = 'holding__expiration_date'
    get_holding_expiration_date.short_description = '取置期限'

    def get_reservations_count(self, stock):
        return stock._reservations_count
    get_reservations_count.admin_order_field = '_reservations_count'
    get_reservations_count.short_description = '予約数'


class LendingAdmin(admin.ModelAdmin):
    list_display = (
        'get_lending_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_lent_at',
        'due_date',
        'get_renewed_due_date',
        'get_is_not_overdue',
        'get_is_stock_reserved',
        'get_is_renewed',
        'is_renewable'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_lending_number(self, lending):
        return lending.id
    get_lending_number.admin_order_field = 'id'
    get_lending_number.short_description = '貸出番号'

    def get_stock_number(self, lending):
        return lending.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, lending):
        return lending.stock.book.name
    get_book_name.admin_order_field = 'stock__book__name'
    get_book_name.short_description = '書名'

    def get_lent_at(self, lending):
        return lending.created_at.date()
    get_lent_at.admin_order_field = 'created_at'
    get_lent_at.short_description = '貸出日'

    def get_renewed_due_date(self, lending):
        return lending.renewing.due_date
    get_renewed_due_date.admin_order_field = 'renewing__due_date'
    get_renewed_due_date.short_description = '延長期限'

    def get_is_not_overdue(self, lending):
        return not lending.is_overdue()
    get_is_not_overdue.boolean = True
    get_is_not_overdue.short_description = '返却期限内？'

    def get_is_stock_reserved(self, lending):
        return 'Yes' if lending.stock.is_reserved() else 'No'
    get_is_stock_reserved.short_description = '予約有り？'

    def get_is_renewed(self, lending):
        return 'Yes' if lending.is_renewed() else 'No'
    get_is_renewed.short_description = '延長済み？'


class RenewingAdmin(admin.ModelAdmin):
    list_display = (
        'get_renewing_number',
        'get_lending_number',
        'get_stock_number',
        'get_book_name',
        'get_user',
        'due_date'
    )
    search_fields = (
        'id',
        'lending__id',
        'lending__stock__id',
        'lending__stock__book__name',
        'lending__user__username'
    )
    raw_id_fields = ('lending', )

    def has_change_permission(self, request, obj=None):
        return False

    def get_renewing_number(self, renewing):
        return renewing.id
    get_renewing_number.admin_order_field = 'id'
    get_renewing_number.short_description = '延長番号'

    def get_lending_number(self, renewing):
        return renewing.lending.id
    get_lending_number.admin_order_field = 'lending__id'
    get_lending_number.short_description = '貸出番号'

    def get_stock_number(self, renewing):
        return renewing.lending.stock.id
    get_stock_number.admin_order_field = 'lending__stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, renewing):
        return renewing.lending.stock.book.name
    get_book_name.admin_order_field = 'lending__stock__book__name'
    get_book_name.short_description = '書名'

    def get_user(self, renewing):
        return renewing.lending.user
    get_user.admin_order_field = 'lending__user'
    get_user.short_description = 'ユーザー'


class HoldingAdmin(admin.ModelAdmin):
    list_display = (
        'get_holding_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_held_at',
        'expiration_date',
        'get_is_not_expired'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_holding_number(self, holding):
        return holding.id
    get_holding_number.admin_order_field = 'id'
    get_holding_number.short_description = '取置番号'

    def get_stock_number(self, holding):
        return holding.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, holding):
        return holding.stock.book.name
    get_book_name.admin_order_field = 'stock__book__name'
    get_book_name.short_description = '書名'

    def get_held_at(self, holding):
        return holding.created_at.date()
    get_held_at.admin_order_field = 'created_at'
    get_held_at.short_description = '取置日'

    def get_is_not_expired(self, holding):
        return not holding.is_expired()
    get_is_not_expired.admin_order_field = 'expiration_date'
    get_is_not_expired.boolean = True
    get_is_not_expired.short_description = '有効期限内？'


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'get_reservation_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_reserved_at',
        'order'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_reservation_number(self, reservation):
        return reservation.id
    get_reservation_number.admin_order_field = 'id'
    get_reservation_number.short_description = '予約番号'

    def get_stock_number(self, reservation):
        return reservation.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, reservation):
        return reservation.stock.book.name
    get_book_name.admin_order_field = 'stock__book__id'
    get_book_name.short_description = '書名'

    def get_reserved_at(self, reservation):
        return reservation.created_at
    get_reserved_at.admin_order_field = 'created_at'
    get_reserved_at.short_description = '予約日時'


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Lending, LendingAdmin)
admin.site.register(Renewing, RenewingAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Reservation, ReservationAdmin)
