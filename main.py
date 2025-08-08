import argparse
from tabulate import tabulate
from log_parser import parse_logs
from report import get_report_generator, REPORTS

LOG_SCHEMA = {
    'endpoint': 'url',
    'response_time': 'response_time',
    'timestamp': '@timestamp'
}


def main():

    parser = argparse.ArgumentParser(description="Анализатор лог-файлов.")
    parser.add_argument(
        '--file',
        type=str,
        nargs='+',
        required=True,
        help="Путь к одному или нескольким лог-файлам."
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=list(REPORTS.keys()),
        help="Название отчета для формирования."
    )
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help="Фильтровать логи по дате в формате YYYY-MM-DD."
    )

    args = parser.parse_args()

    try:
        log_data = parse_logs(args.file, LOG_SCHEMA, args.date)

        if not log_data:
            print("Не найдено записей для анализа (возможно, из-за фильтра по дате).")
            return
            
        report_generator = get_report_generator(args.report, schema=LOG_SCHEMA)
        
        report_table_data = report_generator.generate(log_data)
        
        headers = ["Эндпоинт", "Количество запросов", "Среднее время ответа (ms)"]
        print(f"\nОтчет '{args.report}':")
        print(tabulate(report_table_data, headers=headers, tablefmt="grid"))

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()
