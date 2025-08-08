import pytest
import json

@pytest.fixture
def create_log_file(tmp_path):
    """Фикстура для создания временного лог-файла с данными."""
    log_content = [
        {"timestamp": "2025-06-22T10:00:00.123Z", "endpoint": "/api/v1/users", "response_time": 120.5},
        {"timestamp": "2025-06-22T10:01:00.456Z", "endpoint": "/api/v1/products", "response_time": 80.0},
        {"timestamp": "2025-06-22T10:02:00.789Z", "endpoint": "/api/v1/users", "response_time": 150.0},
        {"timestamp": "2025-06-23T11:00:00.000Z", "endpoint": "/api/v1/users", "response_time": 100.0},
    ]
    
    file_path = tmp_path / "test.log"
    with open(file_path, 'w') as f:
        for entry in log_content:
            f.write(json.dumps(entry) + '\n')
            
    return str(file_path)