from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_cleint: object):
        super().__init__(db_client=db_cleint)
        self.collection = self.db_cleint[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

