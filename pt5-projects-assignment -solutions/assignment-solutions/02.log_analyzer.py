import re
from datetime import datetime
from collections import Counter

class LogAnalyzer:
    def __init__(self):
        self.logs = []

    def read_log_file(self, file_path):
        """Reads the log file and stores each entry in the logs list."""
        try:
            with open(file_path, 'r') as file:
                self.logs = file.readlines()
        except (FileNotFoundError, IOError) as e:
            print(f"Error reading file {file_path}: {e}")

    def filter_logs(self, level=None, keyword=None):
        """
        Filters the logs based on the specified log level and keyword.
        :param level: Log level to filter (ERROR, WARNING, INFO)
        :param keyword: Keyword to search in the log message
        :return: Filtered logs list
        """
        filtered_logs = []
        for log in self.logs:
            if (level is None or f"{level}:" in log) and (keyword is None or re.search(keyword, log, re.IGNORECASE)):
                filtered_logs.append(log)
        return filtered_logs

    def generate_summary(self):
        """
        Generates a summary report from the logs.
        :return: A dictionary containing the summary report
        """
        if not self.logs:
            print("No logs available to generate a summary.")
            return {}

        counts = Counter(log.split()[2][:-1] for log in self.logs)  # Extracts log level from each log entry
        error_messages = [log for log in self.logs if "ERROR:" in log]
        most_common_error = Counter(error_messages).most_common(1)
        time_range = self._calculate_time_range()

        return {
            'total_entries': len(self.logs),
            'error_count': counts.get('ERROR', 0),
            'warning_count': counts.get('WARNING', 0),
            'info_count': counts.get('INFO', 0),
            'most_common_error': most_common_error[0][0].strip() if most_common_error else None,
            'time_range': time_range
        }

    def _calculate_time_range(self):
        """Calculates the time range from the log entries."""
        times = []
        for log in self.logs:
            match = re.search(r"\[(.*?)\]", log)
            if match:
                try:
                    times.append(datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S"))
                except ValueError as e:
                    print(f"Error parsing date from log entry: {e}")
        if times:
            return f"{min(times).strftime('%Y-%m-%d %H:%M:%S')} to {max(times).strftime('%Y-%m-%d %H:%M:%S')}"
        return None

if __name__ == "__main__":
    analyzer = LogAnalyzer()
    analyzer.read_log_file('system_logs.txt')
    
    summary = analyzer.generate_summary()
    print("Summary Report:", summary)
