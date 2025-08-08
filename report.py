from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseReport(ABC):
    def __init__(self, schema: Dict):
        self.schema = schema

    @abstractmethod
    def generate(self, data: List[Dict]) -> List[List[Any]]:
        pass

class AverageResponseReport(BaseReport):
    def generate(self, data: List[Dict]) -> List[List[Any]]:
        endpoint_key = self.schema['endpoint']
        time_key = self.schema['response_time']

        stats = {}
        for entry in data:
            try:
                endpoint = entry[endpoint_key]
                response_time_sec = entry[time_key]
                
                if not isinstance(response_time_sec, (int, float)):
                    continue

                response_time_ms = response_time_sec * 1000
                
                if endpoint not in stats:
                    stats[endpoint] = {'count': 0, 'total_time': 0.0}
                
                stats[endpoint]['count'] += 1
                stats[endpoint]['total_time'] += response_time_ms
            
            except (KeyError, TypeError):
                continue #игнор если не те ключи
            
        report_data = []
        for endpoint, values in stats.items():
            if values['count'] == 0:
                continue
            avg_time = values['total_time'] / values['count']
            report_data.append([endpoint, values['count'], f"{avg_time:.3f}"])
            
        report_data.sort(key=lambda row: row[1], reverse=True)
        return report_data

REPORTS = {
    'average': AverageResponseReport,
}

def get_report_generator(report_name: str, schema: Dict) -> BaseReport:
    report_class = REPORTS.get(report_name)
    if not report_class:
        raise ValueError(f"Отчет с именем '{report_name}' не найден.")
    
    return report_class(schema=schema)