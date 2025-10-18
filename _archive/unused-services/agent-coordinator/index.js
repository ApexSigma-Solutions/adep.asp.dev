const express = require('express');
const WebSocket = require('ws');
const { createClient } = require('redis');
const { v4: uuidv4 } = require('uuid');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 8084;

app.use(express.json());

// Create HTTP server and WebSocket server
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Redis client for agent communication
const redis = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

// Agent registry
const agents = new Map();

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'agent-coordinator' });
});

// Register agent
app.post('/agents/register', async (req, res) => {
  try {
    const { name, capabilities, endpoint } = req.body;
    const agentId = uuidv4();
    
    const agent = {
      id: agentId,
      name,
      capabilities: capabilities || [],
      endpoint,
      status: 'available',
      lastHeartbeat: new Date(),
      createdAt: new Date()
    };
    
    agents.set(agentId, agent);
    
    // Store in Redis for persistence
    await redis.hset('agents', agentId, JSON.stringify(agent));
    
    res.json({ agentId, status: 'registered' });
  } catch (error) {
    console.error('Agent registration error:', error);
    res.status(500).json({ error: 'Failed to register agent' });
  }
});

// List agents
app.get('/agents', (req, res) => {
  const agentList = Array.from(agents.values());
  res.json({ agents: agentList });
});

// Get agent details
app.get('/agents/:id', (req, res) => {
  const { id } = req.params;
  const agent = agents.get(id);
  
  if (!agent) {
    return res.status(404).json({ error: 'Agent not found' });
  }
  
  res.json(agent);
});

// Assign task to agent
app.post('/agents/:id/tasks', async (req, res) => {
  try {
    const { id } = req.params;
    const { task, priority = 'normal' } = req.body;
    const agent = agents.get(id);
    
    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    
    if (agent.status !== 'available') {
      return res.status(409).json({ error: 'Agent is not available' });
    }
    
    const taskId = uuidv4();
    const taskData = {
      id: taskId,
      agentId: id,
      task,
      priority,
      status: 'assigned',
      createdAt: new Date()
    };
    
    // Update agent status
    agent.status = 'busy';
    agents.set(id, agent);
    
    // Store task in Redis
    await redis.hset('tasks', taskId, JSON.stringify(taskData));
    
    // Notify agent via WebSocket if connected
    notifyAgent(id, { type: 'task_assigned', task: taskData });
    
    res.json({ taskId, status: 'assigned' });
  } catch (error) {
    console.error('Task assignment error:', error);
    res.status(500).json({ error: 'Failed to assign task' });
  }
});

// Get agent tasks
app.get('/agents/:id/tasks', async (req, res) => {
  try {
    const { id } = req.params;
    const tasks = await redis.hgetall('tasks');
    
    const agentTasks = Object.values(tasks)
      .map(task => JSON.parse(task))
      .filter(task => task.agentId === id);
    
    res.json({ tasks: agentTasks });
  } catch (error) {
    console.error('Fetch tasks error:', error);
    res.status(500).json({ error: 'Failed to fetch tasks' });
  }
});

// Update agent heartbeat
app.post('/agents/:id/heartbeat', (req, res) => {
  const { id } = req.params;
  const agent = agents.get(id);
  
  if (!agent) {
    return res.status(404).json({ error: 'Agent not found' });
  }
  
  agent.lastHeartbeat = new Date();
  agents.set(id, agent);
  
  res.json({ status: 'heartbeat_received' });
});

// WebSocket connection handling
wss.on('connection', (ws, req) => {
  console.log('New WebSocket connection');
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      
      switch (data.type) {
        case 'agent_connect':
          ws.agentId = data.agentId;
          console.log(`Agent ${data.agentId} connected via WebSocket`);
          break;
          
        case 'task_completed':
          await handleTaskCompletion(data);
          break;
          
        case 'task_failed':
          await handleTaskFailure(data);
          break;
          
        default:
          console.log('Unknown message type:', data.type);
      }
    } catch (error) {
      console.error('WebSocket message error:', error);
    }
  });
  
  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});

function notifyAgent(agentId, message) {
  wss.clients.forEach(client => {
    if (client.agentId === agentId && client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message));
    }
  });
}

async function handleTaskCompletion(data) {
  const { taskId, result } = data;
  
  // Update task status
  const taskData = await redis.hget('tasks', taskId);
  if (taskData) {
    const task = JSON.parse(taskData);
    task.status = 'completed';
    task.result = result;
    task.completedAt = new Date();
    
    await redis.hset('tasks', taskId, JSON.stringify(task));
    
    // Update agent status
    const agent = agents.get(task.agentId);
    if (agent) {
      agent.status = 'available';
      agents.set(task.agentId, agent);
    }
  }
}

async function handleTaskFailure(data) {
  const { taskId, error } = data;
  
  // Update task status
  const taskData = await redis.hget('tasks', taskId);
  if (taskData) {
    const task = JSON.parse(taskData);
    task.status = 'failed';
    task.error = error;
    task.failedAt = new Date();
    
    await redis.hset('tasks', taskId, JSON.stringify(task));
    
    // Update agent status
    const agent = agents.get(task.agentId);
    if (agent) {
      agent.status = 'available';
      agents.set(task.agentId, agent);
    }
  }
}

// Initialize Redis connection
async function init() {
  try {
    await redis.connect();
    console.log('Connected to Redis');
    
    // Load existing agents from Redis
    const existingAgents = await redis.hgetall('agents');
    Object.entries(existingAgents).forEach(([id, data]) => {
      agents.set(id, JSON.parse(data));
    });
    
    console.log(`Loaded ${agents.size} existing agents`);
  } catch (error) {
    console.error('Initialization error:', error);
  }
}

server.listen(PORT, () => {
  console.log(`Agent Coordinator running on port ${PORT}`);
  init();
});

module.exports = app;