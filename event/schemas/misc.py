from pydantic import BaseModel


class Topic(BaseModel):
    topicName = str
    allocatedSection = str
    inCharge = str

