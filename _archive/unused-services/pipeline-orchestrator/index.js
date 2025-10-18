const express = require('express');
const { createClient } = require('redis');
const { Pool } = require('pg');
const cron = require('node-cron');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 8081;

app.use(express.json());

// Redis client
const redis = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

// PostgreSQL client
const pool = new Pool({
  user: process.env.POSTGRES_USER || 'adep_user',
  host: process.env.POSTGRES_HOST || 'postgres',
  database: process.env.POSTGRES_DB || 'adep',
  password: process.env.POSTGRES_PASSWORD || 'adep_password',
  port: process.env.POSTGRES_PORT || 5432,
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'pipeline-orchestrator' });
});

// Create new pipeline
app.post('/pipeline', async (req, res) => {
  try {
    const pipelineId = uuidv4();
    const { name, config } = req.body;
    
    // Store pipeline in database
    await pool.query(
      'INSERT INTO pipelines (id, name, config, status, created_at) VALUES ($1, $2, $3, $4, $5)',
      [pipelineId, name, JSON.stringify(config), 'created', new Date()]
    );
    
    // Queue pipeline for execution
    await redis.lpush('pipeline_queue', JSON.stringify({ id: pipelineId, name, config }));
    
    res.json({ pipelineId, status: 'queued' });
  } catch (error) {
    console.error('Error creating pipeline:', error);
    res.status(500).json({ error: 'Failed to create pipeline' });
  }
});

// Get pipeline status
app.get('/pipeline/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM pipelines WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Pipeline not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error fetching pipeline:', error);
    res.status(500).json({ error: 'Failed to fetch pipeline' });
  }
});

// Initialize connections
async function init() {
  try {
    await redis.connect();
    console.log('Connected to Redis');
    
    // Create pipelines table if it doesn't exist
    await pool.query(`
      CREATE TABLE IF NOT EXISTS pipelines (
        id UUID PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        config JSONB NOT NULL,
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      )
    `);
    console.log('Database initialized');
    
    // Start pipeline processor
    cron.schedule('*/10 * * * * *', processPipelines);
    
  } catch (error) {
    console.error('Initialization error:', error);
  }
}

async function processPipelines() {
  try {
    const pipeline = await redis.brpop('pipeline_queue', 1);
    if (pipeline) {
      const data = JSON.parse(pipeline.element);
      console.log('Processing pipeline:', data.id);
      
      // Update status to running
      await pool.query(
        'UPDATE pipelines SET status = $1, updated_at = $2 WHERE id = $3',
        ['running', new Date(), data.id]
      );
      
      // Simulate pipeline execution
      setTimeout(async () => {
        await pool.query(
          'UPDATE pipelines SET status = $1, updated_at = $2 WHERE id = $3',
          ['completed', new Date(), data.id]
        );
        console.log('Pipeline completed:', data.id);
      }, 5000);
    }
  } catch (error) {
    console.error('Pipeline processing error:', error);
  }
}

app.listen(PORT, () => {
  console.log(`Pipeline Orchestrator running on port ${PORT}`);
  init();
});

module.exports = app;