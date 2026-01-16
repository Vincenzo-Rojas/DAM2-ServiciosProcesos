import { createClient } from 'redis';

const redis = await createClient({
  url: "redis://localhost:6379"
}).on("error", (err) => {
  console.error('Redis Error:', err);
}).connect();

redis.on('connect', () => {
  console.log('Conectado a Redis');
});

export default redis;
