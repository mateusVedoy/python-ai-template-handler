
import re
import time

from src.infraestructure.mongo.mongo import ReportRepository
from src.domain.report import Report
from src.application.dto import ResolveDTO


class ResolveTemplate:

    report_repository: ReportRepository

    def __init__(self, report_repository: ReportRepository):
        self.report_repository = report_repository

    def _augmented_retrieval(
            self,
            prompt,
            relevant_chunks
    ):
        context = "\n\n".join(relevant_chunks)
        augmented_prompt = f"""
        Use as informações do contexto abaixo para responder à pergunta.
        Se a resposta não estiver no contexto, use sua própria base de conhecimento.

        Contexto:
        ---
        {context}
        ---

        Pergunta: {prompt}
        """
        return augmented_prompt

    def _normalize_json(
            self,
            json_puro: str
    ) -> str:

        clean_text = json_puro.strip()
        pattern_inicio = r'^```[a-zA-Z]*\s*'
        prefix = re.sub(pattern_inicio, '', clean_text)
        sufix = r'```$'
        final = re.sub(sufix, '', prefix)
        return final.strip()

    def set_information(self, dto: ResolveDTO) -> str:

        entry = {
            "input": dto.input,
            "output": dto.output
        }

        information = f"""
        Dadas as informações de input e seu respectivo output, use seus conhecimentos para gerar um template handlebars válido para resolver o problema. Abaixo está o seu problema:

        problema:

        {entry}

        Importante: Retorne apenas o template para economizarmos tokens e processamento.
        """

        return information

    def set_prompt_instruction(self) -> str:
        return "Você é um agente especializado em handlebars e tem acesso à documentação de handlebars existente https://handlebarsjs.com/guide/ . Use também possíveis documentos de treinamento para combinar seus conhecimentos. Sempre teste seu template usando o input para que o resultado seja exatamente igual ao output passado"

    def _generateProcessingTime(self, start_processing: float) -> float:
        end_processing = time.perf_counter()
        return end_processing - start_processing

    def _generateReport(self, processing_id: str, start_time: float, status: str, message: str, template: str):

        processing_time = self._generateProcessingTime(start_time)

        report = Report(processing_id, processing_time,
                        status, message, template)

        self.report_repository.save(report)
