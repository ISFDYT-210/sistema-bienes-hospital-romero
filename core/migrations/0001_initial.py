# Generated manually to fix missing migration

from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.utils import timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=timezone.now, verbose_name='date joined')),
                ('tipo_usuario', models.CharField(choices=[('admin', 'Administrador'), ('operador', 'Operador'), ('supervisor', 'Supervisor')], default='empleado', max_length=10)),
                ('numero_doc', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Número de Documento')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ArchivoCargaMasiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='cargas_masivas/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('procesado', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_expediente', models.CharField(max_length=50, unique=True)),
                ('numero_compra', models.CharField(blank=True, max_length=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('leida', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='BienPatrimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('numero_serie', models.CharField(blank=True, max_length=100)),
                ('numero_identificacion', models.CharField(blank=True, max_length=100)),
                ('origen', models.CharField(choices=[('COMPRA', 'Compra'), ('DONACION', 'Donación'), ('TRANSFERENCIA', 'Transferencia'), ('OTRO', 'Otro')], max_length=20)),
                ('estado', models.CharField(choices=[('ACTIVO', 'Activo'), ('BAJA', 'Baja'), ('REPARACION', 'Reparación'), ('PRESTAMO', 'Préstamo')], max_length=20)),
                ('servicios', models.CharField(blank=True, max_length=200)),
                ('observaciones', models.TextField(blank=True)),
                ('fecha_adquisicion', models.DateField()),
                ('fecha_baja', models.DateField(blank=True, null=True)),
                ('siem', models.DateField(blank=True, null=True)),
                ('valor_adquisicion', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cuenta_codigo', models.CharField(blank=True, max_length=50)),
                ('nomenclatura_bienes', models.CharField(blank=True, max_length=100)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('expediente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.expediente')),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=200)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=300)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('dni', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Operador',
                'verbose_name_plural': 'Operadores',
                'ordering': ['nombre_completo'],
            },
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='usuarios_custom', related_query_name='usuario_custom', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='usuarios_custom', related_query_name='usuario_custom', to='auth.permission', verbose_name='user permissions'),
        ),
    ]