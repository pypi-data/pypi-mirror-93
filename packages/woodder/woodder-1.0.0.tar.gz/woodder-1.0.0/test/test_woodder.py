import logging
from pathlib import Path
from src.woodder import Woodder


class TestWoodder(object):
    def test_logger_creates_correct_directory_and_file(self, tmpdir):
        project_name = "arshan123"
        log_dir_name = "some_logs"
        log_dir_path = tmpdir.join(log_dir_name)
        assert log_dir_path.exists() is False
        Woodder.configure_logging(project_name, log_dir=log_dir_path.strpath)
        assert log_dir_path.exists() is True
        assert len(log_dir_path.listdir()) > 0
        log_file = log_dir_path.listdir()[0]
        assert project_name in log_file.basename

    def test_configure_logging_logs_have_the_correct_format(self, tmpdir):
        (project_name, log_dir_name, logger_name) = ("arshan123", "some_logs", "arshanlogger")
        log_dir_path = tmpdir.join(log_dir_name)
        Woodder.configure_logging(project_name, log_dir=log_dir_path.strpath)
        log_file = log_dir_path.listdir()[0]
        logger = logging.getLogger(logger_name)

        logger.info("here's some info")
        logger.warning("here's some warning")
        logger.debug("here's some debug")
        logger.critical("critical stuff")
        logger.error("some error")

        lines = log_file.readlines()
        assert len(lines) == 5
        assert "INFO" in lines[0]
        assert "WARNING" in lines[1]
        assert "DEBUG" in lines[2]
        assert "CRITICAL" in lines[3]
        assert "ERROR" in lines[4]

        for line in lines:
            assert Path(__file__).name in line
