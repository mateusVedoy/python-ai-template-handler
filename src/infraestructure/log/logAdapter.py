

import datetime


class LogHeader:
    processing_time: float
    template_alias: str
    processing_id: str
    stack: str
    status: str
    reprocessing_attempt: int

    def __init__(
            self,
            processingTime: float,
            status: str,
            templateAlias: str = "",
            processingId: str = "",
            stack: str = "",
            reprocessing_attempt=0
    ):
        self.processing_time = processingTime
        self.template_alias = templateAlias
        self.processing_id = processingId
        self.stack = stack
        self.status = status
        self.reprocessing_attempt = reprocessing_attempt

    def to_dict(self):
        return {
            "processing_time": self.processing_time,
            "template_alias": self.template_alias,
            "processing_id": self.processing_id,
            "stack": self.stack,
            "status": self.status,
            "reprocessing_attempt": self.reprocessing_attempt
        }


class Log:
    ts: str
    header: LogHeader
    message: str

    def __init__(
            self,
            header: LogHeader,
            message: str
    ):
        self.ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.header = header
        self.message = message

    def to_dict(self):
        return {
            "ts": self.ts,
            "header": self.header.to_dict(),
            "message": self.message
        }


class LogAdapter:

    def _logger(self, log: Log):
        print(log.to_dict())

    # logs da etapa de gerar exemplos

    def template_example_generated(self, template_alias: str, message: str, processingTime: float):
        header = LogHeader(
            processingTime,
            "TEMPLATE_EXAMPLE_GENERATED",
            template_alias)
        log = Log(header, message)
        self._logger(log)

    def template_example_generation_error(self, template_alias: str, message: str, processingTime: float):
        header = LogHeader(
            processingTime,
            "TEMPLATE_EXAMPLE_GENERATION_ERROR",
            template_alias)
        log = Log(header, message)
        self._logger(log)

    # logs da etapa de compilar report

    def template_compiled_successfully_sync(self, processingTime: float, processingId: str, message: str):
        header = LogHeader(
            processingTime,
            "TEMPLATE_COMPILED_SUCCESSFULLY_SYNC",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def template_compiled_successfully_async(self, processingTime: float, processingId: str, message: str):
        header = LogHeader(
            processingTime,
            "TEMPLATE_COMPILED_SUCCESSFULLY_ASYNC",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def report_compiled_successfully(self, processing_id: str, message: str, processingTime: float):
        header = LogHeader(
            processingTime,
            "REPORT_COMPILED_SUCCESSFULLY",
            "",
            processing_id
        )
        log = Log(header, message)
        self._logger(log)

    # logs de processamento de template

    def starting_resolve_template(self, processingId: str, message: str):
        header = LogHeader(
            0,
            "RESOLVE_TEMPLATE_STARTED",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def starting_processing_template(self, processingId: str, message: str):
        header = LogHeader(
            0,
            "PROCESSING_TEMPLATE",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def starting_reprocessing_template(self, processingId: str, attempt: int, message: str):
        header = LogHeader(
            0,
            "REPROCESSING_TEMPLATE_ATTEMPT",
            "",
            processingId,
            "",
            attempt)
        log = Log(header, message)
        self._logger(log)

    def resolve_template_async_retry(self, processingId: str, message: str):
        header = LogHeader(
            0,
            "RESOLVE_TEMPLATE_ASYNC_RETRY",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def finish_resolve_template(self, processingId: str, message: str):
        header = LogHeader(
            0,
            "RESOLVE_TEMPLATE_FINISHED",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def retries_exceeded(self, processingTime: float, processingId: str, message: str):
        header = LogHeader(
            processingTime,
            "TEMPLATE_COMPILATION_RETRIES_EXCEEDED",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    def template_generation_async_aborted(self, processingTime: float, processingId: str, message: str):
        header = LogHeader(
            processingTime,
            "TEMPLATE_GENERATION_ASYNC_ERROR",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)

    # logs da etapa de geração do report sync

    def template_generation_sync_error(self, processingTime: float, processingId: str, message: str):
        header = LogHeader(
            processingTime,
            "TEMPLATE_GENERATION_SYNC_ERROR",
            "",
            processingId)
        log = Log(header, message)
        self._logger(log)
