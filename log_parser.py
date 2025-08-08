import json
from datetime import datetime
from typing import List, Dict, Optional

def parse_logs(file_paths: List[str], schema: Dict, filter_date_str: Optional[str] = None) -> List[Dict]:
    parsed_entries = []
    timestamp_key = schema['timestamp']
    
    filter_date = None
    if filter_date_str:
        try:
            filter_date = datetime.strptime(filter_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD.")

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    log_entry = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Предупреждение: Пропущена невалидная JSON-строка в файле {file_path}, строка {i}")
                    continue

                if filter_date:
                    if timestamp_key in log_entry:
                        ts_val = log_entry[timestamp_key]
                        if ts_val:
                            log_timestamp = datetime.fromisoformat(ts_val).date()
                            if log_timestamp != filter_date:
                                continue
                        else: 
                            continue #игнор если значение None
                    else: 
                        continue #если нет клоюча тоже игнор
                
                parsed_entries.append(log_entry)
                
    return parsed_entries