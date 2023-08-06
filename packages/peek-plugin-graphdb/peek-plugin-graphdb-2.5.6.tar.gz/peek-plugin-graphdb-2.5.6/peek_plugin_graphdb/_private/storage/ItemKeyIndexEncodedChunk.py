import logging

from sqlalchemy import Column, LargeBinary, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index
from vortex.Tuple import Tuple, addTupleType

from peek_abstract_chunked_index.private.tuples.ACIEncodedChunkTupleABC import \
    ACIEncodedChunkTupleABC
from peek_plugin_graphdb._private.PluginNames import graphDbTuplePrefix
from peek_plugin_graphdb._private.storage.GraphDbModelSet import GraphDbModelSet
from .DeclarativeBase import DeclarativeBase

logger = logging.getLogger(__name__)


@addTupleType
class ItemKeyIndexEncodedChunk(Tuple, DeclarativeBase,
                               ACIEncodedChunkTupleABC):

    __tablename__ = 'ItemKeyIndexEncodedChunk'
    __tupleType__ = graphDbTuplePrefix + 'ItemKeyIndexEncodedChunkTable'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    modelSetId = Column(Integer,
                        ForeignKey('GraphDbModelSet.id', ondelete='CASCADE'),
                        nullable=False)
    modelSet = relationship(GraphDbModelSet)

    chunkKey = Column(String, nullable=False)
    encodedData = Column(LargeBinary, nullable=False)
    encodedHash = Column(String, nullable=False)
    lastUpdate = Column(String, nullable=False)

    __table_args__ = (
        Index("idx_ItemKeyIndexEnc_modelSetId_chunkKey", modelSetId, chunkKey,
              unique=False),
    )

    @property
    def ckiChunkKey(self):
        return self.chunkKey

    @property
    def ckiLastUpdate(self):
        return self.lastUpdate

    @property
    def ckiHasEncodedData(self) -> bool:
        return bool(self.encodedData)

    @classmethod
    def ckiCreateDeleteEncodedChunk(cls, chunkKey: str):
        return ItemKeyIndexEncodedChunk(chunkKey=chunkKey)

    @classmethod
    def sqlCoreChunkKeyColumn(cls):
        return cls.__table__.c.chunkKey

    @classmethod
    def sqlCoreLoad(cls, row):
        return ItemKeyIndexEncodedChunk(id=row.id,
                                        chunkKey=row.chunkKey,
                                        encodedData=row.encodedData,
                                        encodedHash=row.encodedHash,
                                        lastUpdate=row.lastUpdate)
