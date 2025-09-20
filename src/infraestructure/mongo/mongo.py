
from pymongo import MongoClient

from src.domain.report import Report
from src.domain.mapping import Mapping


class MappingRepository:
    colletion: any

    def __init__(self):
        client = MongoClient(
            "mongodb://admin:admin@127.0.0.1:27017/?authSource=admin")
        db = client["template"]
        self.collection = db["mappings"]

    def save(self, map: Mapping) -> list[Mapping]:
        self.collection.insert_one(map.to_dict())

    def findAll(self):
        doc = self.collection.find({})

        if not doc:
            return []

        mappings = []

        for d in doc:
            mapping = Mapping(
                d['alias'],
                d['description'],
                d['input'],
                d['output'],
                d['template']
            )

            mappings.append(mapping)

        return mappings


class ReportRepository:
    colletion: any

    def __init__(self):
        client = MongoClient(
            "mongodb://admin:admin@127.0.0.1:27017/?authSource=admin")
        db = client["template"]
        self.collection = db["reports"]

    def save(self, report: Report) -> None:
        self.collection.insert_one(report.to_dict())
