
class Report:
    """
    Representa o relatório do processamento de template
    """
    identifier: str
    processingTime: float
    template: str
    status: str
    message: str

    def __init__(self, identifier: str, processingTime: float, status: str, message: str, template: str):
        self.identifier = identifier
        self.processingTime = processingTime
        self.template = template
        self.status = status
        self.message = message

    # adicionar validação depois
    def _validate(self):
        pass

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "processingTime": self.processingTime,
            "template": self.template,
            "status": self.status,
            "message": self.message
        }
