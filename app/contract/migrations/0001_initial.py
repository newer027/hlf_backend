# Generated by Django 2.2.3 on 2019-09-20 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashcode',
            fields=[
                ('serial_id', models.CharField(max_length=100)),
                ('order_info', models.CharField(max_length=800)),
                ('order_hash', models.CharField(max_length=100)),
                ('txid', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('serial_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('vendor', models.CharField(max_length=100)),
                ('invoice_org', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hash_value', models.BooleanField(default=False)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderEnd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_id', models.CharField(max_length=100)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('end_loc', models.CharField(max_length=100)),
                ('gps_time', models.DateTimeField(blank=True, null=True)),
                ('gps_loc', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('loc_source', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hash_value', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=True)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderStart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_id', models.CharField(max_length=100)),
                ('item_id', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('start_loc', models.CharField(max_length=100)),
                ('start_short', models.CharField(max_length=20)),
                ('end_short', models.CharField(max_length=20)),
                ('vendor', models.CharField(max_length=100)),
                ('invoice_org', models.CharField(max_length=100)),
                ('palate', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('gps_time', models.DateTimeField(blank=True, null=True)),
                ('gps_loc', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('loc_source', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'No_Status'), (1, 'Normal'), (2, 'Start_Ng'), (3, 'End_Ng'), (4, 'StartEnd_Ng')], default='0')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hash_value', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=True)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='StatusDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('velocity', models.DecimalField(decimal_places=2, default=70.0, max_digits=5)),
                ('distance', models.DecimalField(decimal_places=2, default=70.0, max_digits=5)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=100)),
                ('serial_id', models.CharField(max_length=100, null=True)),
                ('vendor', models.CharField(max_length=100)),
                ('invoice_org', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(max_length=100)),
                ('start_short', models.CharField(max_length=20)),
                ('end_short', models.CharField(max_length=20)),
                ('palate', models.CharField(max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hash_value', models.BooleanField(default=False)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
                ('ledger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_to_ledger', to='contract.Ledger')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Abnormal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_id', models.CharField(max_length=100)),
                ('item_id', models.CharField(max_length=100)),
                ('ngText', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('orderStart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abnormal', to='contract.OrderStart')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
