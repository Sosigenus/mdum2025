from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
from django.contrib import messages
from .models import Record
from django.utils.dateparse import parse_datetime
from django.db import transaction

def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        file = request.FILES['json_file']
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            messages.error(request, 'Файл не является корректным JSON.')
            return render(request, 'upload.html')

        errors = []
        valid_records = []

        for i, item in enumerate(data):
            name = item.get('name')
            date_str = item.get('date')

            if not name or not date_str:
                errors.append(f"[#{i}] Отсутствует ключ name или date")
                continue

            if len(name) >= 50:
                errors.append(f"[#{i}] 'name' должен быть короче 50 символов")
                continue

            # преобразуем YYYY-MM-DD_HH:mm → datetime
            try:
                date_str = date_str.replace('_', 'T')
                date = parse_datetime(date_str)
                if not date:
                    raise ValueError
            except:
                errors.append(f"[#{i}] Некорректный формат даты")
                continue

            valid_records.append(Record(name=name, date=date))

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            with transaction.atomic():
                Record.objects.bulk_create(valid_records)
            messages.success(request, f"Загружено {len(valid_records)} записей")

    return render(request, 'upload.html')

#DataTables
def records_table(request):
    records = Record.objects.all()
    return render(request, 'records.html', {'records': records})

#Leaflet
def leaflet_map(request):
    return render(request, 'leaflet.html')
