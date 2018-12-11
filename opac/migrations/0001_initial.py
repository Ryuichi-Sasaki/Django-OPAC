# Generated by Django 2.1.2 on 2018-12-11 07:36

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('name', models.CharField(max_length=100, verbose_name='氏名')),
            ],
            options={
                'verbose_name': '著者',
                'verbose_name_plural': '著者',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('name', models.CharField(max_length=100, verbose_name='書名')),
                ('publication_date', models.DateField(blank=True, null=True, verbose_name='出版日')),
                ('size', models.CharField(blank=True, max_length=20, null=True, verbose_name='大きさ')),
                ('page', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='ページ数')),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(regex='^(97(8|9))?\\d{9}(\\d|X)$')], verbose_name='ISBN')),
            ],
            options={
                'verbose_name': '書籍',
                'verbose_name_plural': '書籍',
            },
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('expiration_date', models.DateField(verbose_name='有効期限')),
            ],
            options={
                'verbose_name': '取置',
                'verbose_name_plural': '取置',
            },
        ),
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('due_date', models.DateField(verbose_name='返却期限')),
            ],
            options={
                'verbose_name': '貸出',
                'verbose_name_plural': '貸出',
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='館名')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='所在地')),
            ],
            options={
                'verbose_name': '図書館',
                'verbose_name_plural': '図書館',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='所在地')),
            ],
            options={
                'verbose_name': '出版者',
                'verbose_name_plural': '出版者',
            },
        ),
        migrations.CreateModel(
            name='Renewing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('due_date', models.DateField(verbose_name='延長期限')),
                ('lending', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='renewing', to='opac.Lending', verbose_name='貸出')),
            ],
            options={
                'verbose_name': '貸出延長',
                'verbose_name_plural': '貸出延長',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '取置予約',
                'verbose_name_plural': '取置予約',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stocks', to='opac.Book', verbose_name='書籍')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stocks', to='opac.Library', verbose_name='配架先')),
            ],
            options={
                'verbose_name': '蔵書',
                'verbose_name_plural': '蔵書',
            },
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('name', models.CharField(max_length=100, verbose_name='氏名')),
                ('books', models.ManyToManyField(related_name='translators', to='opac.Book', verbose_name='訳書リスト')),
            ],
            options={
                'verbose_name': '訳者',
                'verbose_name_plural': '訳者',
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='opac.Stock', verbose_name='蔵書'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='lending',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lending', to='opac.Stock', verbose_name='蔵書'),
        ),
        migrations.AddField(
            model_name='lending',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lendings', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='holding',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='holding', to='opac.Stock', verbose_name='蔵書'),
        ),
        migrations.AddField(
            model_name='holding',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='opac.Publisher', verbose_name='出版者'),
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(related_name='authors', to='opac.Book', verbose_name='著書リスト'),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('stock', 'user')},
        ),
    ]
