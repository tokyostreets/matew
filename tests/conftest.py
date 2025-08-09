import pytest
import json

@pytest.fixture
def create_log_file(tmp_path):
    log_content = [
        {"@timestamp": "2025-06-22T10:00:00.123Z", "url": "/api/v1/users", "response_time": 0.1205},
        {"@timestamp": "2025-06-22T10:01:00.456Z", "url": "/api/v1/products", "response_time": 0.080},
        {"@timestamp": "2025-06-22T10:02:00.789Z", "url": "/api/v1/users", "response_time": 0.150},
        {"@timestamp": "2025-06-23T11:00:00.000Z", "url": "/api/v1/users", "response_time": 0.100},
    ]

    file_path = tmp_path / "test.log"
    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in log_content:
            f.write(json.dumps(entry) + '\n')

    return str(file_path)