import pytest
from log_parser import parse_logs
from report import AverageResponseReport, get_report_generator

def test_log_parsing(create_log_file):
    """Тест базового парсинга файла."""
    logs = parse_logs([create_log_file])
    assert len(logs) == 4
    assert logs[0]['endpoint'] == '/api/v1/users'

def test_log_parsing_with_date_filter(create_log_file):
    """Тест парсинга с фильтром по дате."""
    logs = parse_logs([create_log_file], filter_date_str="2025-06-22")
    assert len(logs) == 3
    for log in logs:
        assert log['timestamp'].startswith("2025-06-22")

def test_log_parsing_file_not_found():
    """Тест обработки несуществующего файла."""
    with pytest.raises(FileNotFoundError):
        parse_logs(["non_existent_file.log"])

def test_average_report_generation(create_log_file):
    """Тест логики отчета 'average'."""
    logs = parse_logs([create_log_file])
    report_generator = AverageResponseReport()
    report_data = report_generator.generate(logs)
    
    # Отчет отсортирован по количеству запросов
    # 1. /api/v1/users: 3 запроса, среднее (120.5 + 150.0 + 100.0) / 3 = 123.5
    # 2. /api/v1/products: 1 запрос, среднее 80.0
    
    assert len(report_data) == 2
    assert report_data[0] == ['/api/v1/users', 3, '123.500']
    assert report_data[1] == ['/api/v1/products', 1, '80.000']
    
def test_report_factory():
    """Тест фабрики отчетов."""
    generator = get_report_generator('average')
    assert isinstance(generator, AverageResponseReport)
    
    with pytest.raises(ValueError):
        get_report_generator('non_existent_report')