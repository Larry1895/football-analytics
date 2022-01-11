# coding=utf-8

from sqlalchemy import Column, Integer, Date, DateTime

from src.scrapper.base import Base


class FifaScrapperExecution(Base):
    __tablename__ = 'fifa_scrapper_execution'

    fifa_scrapper_execution_id = Column(Integer, primary_key=True)
    year_of_fifa = Column(Integer)
    data_from_timestamp = Column(Date)
    executed_at = Column(DateTime)

    def __init__(self, year_of_fifa, data_from_timestamp, executed_at):
        self.year_of_fifa = year_of_fifa
        self.data_from_timestamp = data_from_timestamp
        self.executed_at = executed_at
