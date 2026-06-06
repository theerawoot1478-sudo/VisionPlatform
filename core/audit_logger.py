from datetime import datetime


class AuditLogger:

    def __init__(self):

        self.log_file = "audit_log.txt"

    def write(
        self,
        username,
        action
    ):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = (
            f"{now} | "
            f"{username} | "
            f"{action}\n"
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(line)