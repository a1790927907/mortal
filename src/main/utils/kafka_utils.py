from aiokafka import AIOKafkaClient
from aiokafka.cluster import ClusterMetadata


async def fetch_kafka_metadata(bootstrap_servers: str) -> ClusterMetadata:
    client = AIOKafkaClient(bootstrap_servers=bootstrap_servers)
    await client.bootstrap()
    metadata = await client.fetch_all_metadata()
    return metadata
