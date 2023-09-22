from datadog_checks.base import AgentCheck
import socket
import json

class UWSGIStatusCheck(AgentCheck):
    def check(self, instance):
        active_workers = self.get_active_workers()
        total_workers = self.get_total_workers()
        self.gauge('uwsgi.workers.active', active_workers)
        self.gauge('uwsgi.workers.total', total_workers)

    def get_uwsgi_stats(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 1718))
            chunks = []
            while True:
                chunk = s.recv(8192)
                if not chunk:
                    break
                chunks.append(chunk)
            s.close()
            raw_data = b''.join(chunks)
            return json.loads(raw_data)
        except Exception as e:
            self.log.error(f"Error retrieving uWSGI stats: {e}")
            return None

    def get_active_workers(self):
        try:
            data = self.get_uwsgi_stats()
            if data:
                return len([w for w in data["workers"] if not w["status"] == "idle"])
        except Exception as e:
            self.log.error(f"Error retrieving active workers: {e}")
        return 0

    def get_total_workers(self):
        try:
            data = self.get_uwsgi_stats()
            if data:
                return len(data["workers"])
        except Exception as e:
            self.log.error(f"Error retrieving total workers: {e}")
        return 0


# For testing purposes
# if __name__ == '__main__':
#     check = UWSGIStatusCheck()
#     active_workers = check.get_active_workers()
#     total_workers = check.get_total_workers()
#     print(f"Active Workers: {active_workers}")
#     print(f"Total Workers: {total_workers}")
