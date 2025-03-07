from motor.motor_asyncio import AsyncIOMotorClient
import logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_mongodb(self):
        """连接到MongoDB"""
        logger.info("正在连接到MongoDB...")
        try:
            self.client = AsyncIOMotorClient(settings.mongo_uri)
            self.db = self.client.get_database()
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {e}")
            raise

    async def close_mongodb_connection(self):
        """关闭MongoDB连接"""
        logger.info("正在关闭MongoDB连接...")
        if self.client:
            self.client.close()
            logger.info("MongoDB连接已关闭")

    def get_db(self):
        """获取数据库实例"""
        return self.db

# 创建MongoDB实例
mongodb = MongoDB() 