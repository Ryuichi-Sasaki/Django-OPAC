from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        '作成日時',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        '更新日時',
        auto_now=True
    )


class Publisher(TimeStampedModel):
    class Meta:
        verbose_name = '出版者'
        verbose_name_plural = '出版者'

    name = models.CharField(
        '名前',
        max_length=100
    )
    address = models.CharField(
        '所在地',
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    class Meta:
        verbose_name = '書籍'
        verbose_name_plural = '書籍'

    name = models.CharField(
        '書名',
        max_length=100
    )
    publisher = models.ForeignKey(
        Publisher,
        verbose_name='出版者',
        related_name='books',
        on_delete=models.PROTECT
    )
    publication_date = models.DateField(
        '出版日',
        blank=True,
        null=True
    )
    size = models.CharField(
        '大きさ',
        max_length=20,
        blank=True,
        null=True
    )
    page = models.IntegerField(
        'ページ数',
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        blank=True,
        null=True,
        validators=[
            # ISBN10 or ISBN13 without separators
            RegexValidator(regex=r'^(97(8|9))?\d{9}(\d|X)$')
        ]
    )

    def __str__(self):
        return self.name


class Author(TimeStampedModel):
    class Meta:
        verbose_name = '著者'
        verbose_name_plural = '著者'

    name = models.CharField(
        '氏名',
        max_length=100
    )
    books = models.ManyToManyField(
        Book,
        verbose_name='著書リスト',
        related_name='authors'
    )

    def __str__(self):
        return self.name


class Translator(TimeStampedModel):
    class Meta:
        verbose_name = '訳者'
        verbose_name_plural = '訳者'

    name = models.CharField(
        '氏名',
        max_length=100
    )
    books = models.ManyToManyField(
        Book,
        verbose_name='訳書リスト',
        related_name='translators'
    )

    def __str__(self):
        return self.name


class Library(TimeStampedModel):
    class Meta:
        verbose_name = '図書館'
        verbose_name_plural = '図書館'

    name = models.CharField(
        '館名',
        max_length=100,
        unique=True
    )
    address = models.CharField(
        '所在地',
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Stock(TimeStampedModel):
    class Meta:
        verbose_name = '蔵書'
        verbose_name_plural = '蔵書'

    book = models.ForeignKey(
        Book,
        verbose_name='書籍',
        related_name='stocks',
        on_delete=models.PROTECT
    )
    library = models.ForeignKey(
        Library,
        verbose_name='配架先',
        related_name='stocks',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return '蔵書番号{} : {}'.format(self.id, self.book.name)

    def is_lendable(self):
        return not self.is_lent() \
           and not self.is_held()

    def is_holdable(self):
        return self.is_lendable()

    def is_reservable(self):
        return not self.is_lendable()

    def is_lent(self):
        return hasattr(self, 'lending')

    def is_held(self):
        return hasattr(self, 'holding')

    def is_reserved(self):
        return self.reservations.exists()


class User(AbstractUser):
    pass


class Lending(TimeStampedModel):
    class Meta:
        verbose_name = '貸出'
        verbose_name_plural = '貸出'

    stock = models.OneToOneField(
        Stock,
        verbose_name='蔵書',
        related_name='lending',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='lendings',
        on_delete=models.PROTECT
    )
    due_date = models.DateField(
        '返却期限'
    )

    def __str__(self):
        return '{} : {}'.format(self.stock, self.user)

    def actual_due_date(self):
        return self.renewing.due_date if self.is_renewed() \
          else self.due_date

    def is_renewed(self):
        return hasattr(self, 'renewing')

    def is_overdue(self):
        return self.actual_due_date() < timezone.localdate()

    def is_renewable(self):
        return not self.is_renewed() \
           and not self.stock.is_reserved()
    is_renewable.boolean = True
    is_renewable.short_description = '延長可能？'


class Renewing(TimeStampedModel):
    class Meta:
        verbose_name = '貸出延長'
        verbose_name_plural = '貸出延長'

    lending = models.OneToOneField(
        Lending,
        verbose_name='貸出',
        related_name='renewing',
        on_delete=models.CASCADE
    )
    due_date = models.DateField(
        '延長期限'
    )

    def __str__(self):
        return str(self.lending)

    def is_overdue(self):
        return self.due_date < timezone.localdate()


class Holding(TimeStampedModel):
    class Meta:
        verbose_name = '取置'
        verbose_name_plural = '取置'

    stock = models.OneToOneField(
        Stock,
        verbose_name='蔵書',
        related_name='holding',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='holdings',
        on_delete=models.CASCADE
    )
    expiration_date = models.DateField(
        '有効期限'
    )

    def __str__(self):
        return '{} : {}'.format(self.stock, self.user)

    def is_expired(self):
        return self.expiration_date < timezone.localdate()


class Reservation(TimeStampedModel):
    class Meta:
        verbose_name = '取置予約'
        verbose_name_plural = '取置予約'
        unique_together = ('stock', 'user')

    stock = models.ForeignKey(
        Stock,
        verbose_name='蔵書',
        related_name='reservations',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='reservations',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{} : {}'.format(self.stock, self.user)

    def order(self):
        return Reservation.objects \
            .filter(stock__id=self.stock.id) \
            .filter(created_at__lt=self.created_at) \
            .count() + 1
    order.short_description = '予約順位'
