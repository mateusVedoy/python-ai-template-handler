
from fastapi.responses import JSONResponse
from src.application.dto import ApiResponse
from src.infraestructure.mongo.mongo import ReportRepository


class GetTemplateString:
    report_repository: ReportRepository

    def __init__(self, report_repository: ReportRepository):
        self.report_repository = report_repository

    def get(self, reportId) -> ApiResponse:

        report = self.report_repository.findByIdentifier(reportId)

        if report is None:

            err = ApiResponse(
                statusCode=404,
                message="no template was found",
                template=""
            )

            return JSONResponse(
                status_code=err.statusCode,
                content={
                    "statusCode": err.statusCode,
                    "message": err.message,
                    "template": err.template
                }
            )

        return ApiResponse(
            statusCode=200,
            message="template fetched bellow",
            template=report.template)
