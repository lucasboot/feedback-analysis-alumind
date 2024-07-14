import redis

# Conecte-se ao Redis
client = redis.StrictRedis(
    host='redis-10690.c251.east-us-mz.azure.redns.redis-cloud.com',
    port=10690,
    password='STOwRijujbtHO0jnftiuaGcQKxYBwEcq',
    decode_responses=True
)

try:
    # Teste a conexão
    response = client.ping()
    print("Redis está funcionando:", response)

    # Teste SET e GET
    client.set('test_key', 'Hello, Redis!')
    value = client.get('test_key')
    print("Valor da chave 'test_key':", value)

except redis.ConnectionError:
    print("Não foi possível conectar ao Redis.")
