from pydantic import BaseModel


class Topic(BaseModel):
    topicName: str
    allocatedSection: str
    inCharge: str


class College(BaseModel):
    collegeName: str
    collegeCode: str
    collegeAddress: str

